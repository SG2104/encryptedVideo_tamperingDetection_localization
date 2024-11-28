import cv2
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def encrypt_video(video_path, output_encrypted_path, hash_file_path):
    key = os.urandom(16)  # AES key
    cap = cv2.VideoCapture(video_path)
    frame_hashes = []

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_encrypted_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_bytes = frame.tobytes()
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted_frame = cipher.encrypt(pad(frame_bytes, AES.block_size))
        frame_hashes.append(hashlib.sha256(frame_bytes).hexdigest())

        # Visualization placeholder
        encrypted_visual_frame = frame.copy()
        out.write(encrypted_visual_frame)

    cap.release()
    out.release()

    # Write hash file
    with open(hash_file_path, 'w') as f:
        for i, h in enumerate(frame_hashes):
            f.write(f"Frame {i}: {h}\n")

    return key
