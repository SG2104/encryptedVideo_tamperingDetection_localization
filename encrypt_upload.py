import cv2
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import boto3

# Function to generate a random AES key
def generate_aes_key():
    return os.urandom(16)  # 16 bytes for AES-128

# Function to encrypt data using AES
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data, cipher.iv

# Function to upload files to S3
def upload_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")

# Function to process video frames, encrypt, and hash them
def process_video(video_path, output_encrypted_video_path, hash_file_path, key):
    cap = cv2.VideoCapture(video_path)
    frame_hashes = []

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_encrypted_video_path, fourcc, fps, (width, height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_bytes = frame.tobytes()
        encrypted_frame, iv = encrypt_data(frame_bytes, key)
        frame_hash = hashlib.sha256(frame_bytes).hexdigest()
        frame_hashes.append(frame_hash)

        encrypted_frame_visual = frame.copy()
        encrypted_frame_visual[:, :, 0] = encrypted_frame[:frame.size // 3]
        out.write(encrypted_frame_visual)

        frame_count += 1

    cap.release()
    out.release()

    with open(hash_file_path, 'w') as f:
        for i, h in enumerate(frame_hashes):
            f.write(f"Frame {i}: {h}\n")

    print(f"Processed {frame_count} frames. Encrypted video saved at '{output_encrypted_video_path}' and hashes saved at '{hash_file_path}'.")

    # Call S3 upload function
    bucket_name = "your-s3-bucket-name"  # Replace with your actual bucket name
    upload_to_s3(output_encrypted_video_path, bucket_name)
    upload_to_s3(hash_file_path, bucket_name)

# Main function
if __name__ == "__main__":
    input_video_path = "input_video.mp4"
    encrypted_video_path = "encrypted_video.mp4"
    hash_file_path = "frame_hashes.txt"

    aes_key = generate_aes_key()
    print(f"Generated AES Key: {aes_key.hex()}")

    process_video(input_video_path, encrypted_video_path, hash_file_path, aes_key)
