from flask import Flask, request, jsonify
import os
import boto3
import hashlib
import cv2
import numpy as np  # Import numpy for array manipulation
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)

# S3 Configuration
BUCKET_NAME = "encrypted-video-storage-crypto"

# AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id="AKIAU6GD35VQLH463WPB",
    aws_secret_access_key="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",
    region_name="us-east-1"
)

# Function to encrypt video frames
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data, cipher.iv

# API Endpoint: Upload and Process Video
@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        # Get the uploaded file
        video = request.files.get('video')
        if not video:
            return jsonify({"error": "No video file uploaded"}), 400

        key = os.urandom(16)  # Generate AES Key

        # Create upload directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)

        # Save the file locally
        video_path = os.path.join("uploads", video.filename)
        video.save(video_path)

        # Process video
        encrypted_video_path = os.path.join("uploads", f"encrypted_{video.filename}")
        hash_file_path = os.path.join("uploads", f"{video.filename}_hashes.txt")
        process_video(video_path, encrypted_video_path, hash_file_path, key)

        # Upload encrypted video and hash file to S3
        upload_to_s3(encrypted_video_path, BUCKET_NAME, os.path.basename(encrypted_video_path))
        upload_to_s3(hash_file_path, BUCKET_NAME, os.path.basename(hash_file_path))

        return jsonify({"message": "Video uploaded and processed successfully", "key": key.hex()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_video(video_path, output_encrypted_video_path, hash_file_path, key):
    cap = cv2.VideoCapture(video_path)
    frame_hashes = []

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_encrypted_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Ensure frame is valid
        if frame is None or frame.size == 0:
            continue

        try:
            # Flatten the frame to bytes
            frame_bytes = frame.tobytes()

            # Encrypt the frame
            encrypted_frame, _ = encrypt_data(frame_bytes, key)

            # Calculate frame hash
            frame_hash = hashlib.sha256(frame_bytes).hexdigest()
            frame_hashes.append(frame_hash)

            # Restore encrypted frame to original shape
            encrypted_frame_array = np.frombuffer(encrypted_frame, dtype=np.uint8)
            if len(encrypted_frame_array) != frame.size:
                # Pad or trim to match frame size
                encrypted_frame_array = np.resize(encrypted_frame_array, frame.size)
            encrypted_frame_reshaped = encrypted_frame_array.reshape(frame.shape)

            # Replace one channel of the frame with encrypted data
            encrypted_frame_visual = frame.copy()
            encrypted_frame_visual[:, :, 0] = encrypted_frame_reshaped[:, :, 0]

            # Write the modified frame
            out.write(encrypted_frame_visual)

        except Exception as e:
            print(f"Error processing frame: {e}")

    cap.release()
    out.release()

    # Write frame hashes to a file
    with open(hash_file_path, 'w') as f:
        for i, h in enumerate(frame_hashes):
            f.write(f"Frame {i}: {h}\n")

def upload_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
