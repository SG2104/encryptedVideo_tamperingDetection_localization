import hashlib
import cv2

def detect_tampering(video_path, hash_file_path):
    with open(hash_file_path, 'r') as f:
        original_hashes = [line.strip().split(": ")[1] for line in f.readlines()]

    cap = cv2.VideoCapture(video_path)
    tampered_frames = []

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_bytes = frame.tobytes()
        recalculated_hash = hashlib.sha256(frame_bytes).hexdigest()

        if recalculated_hash != original_hashes[frame_count]:
            tampered_frames.append(frame_count)

        frame_count += 1

    cap.release()
    return tampered_frames
