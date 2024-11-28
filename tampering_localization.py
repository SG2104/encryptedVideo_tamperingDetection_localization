import cv2  
import hashlib  
import numpy as np  

def localize_tampering(video_path, tampered_frames):
    cap = cv2.VideoCapture(video_path)
    localized_changes = {}

    for frame_idx in tampered_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue

        block_size = 16
        height, width, _ = frame.shape
        tampered_blocks = []

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = frame[y:y+block_size, x:x+block_size].tobytes()
                block_hash = hashlib.sha256(block).hexdigest()

                # Check for tampering condition
                if block_hash == "some_expected_condition":  # Placeholder
                    tampered_blocks.append((x, y))

        localized_changes[frame_idx] = tampered_blocks

    cap.release()
    return localized_changes
