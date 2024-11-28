from flask import Flask, request, jsonify
from encryption import encrypt_video
from cloud_upload import upload_to_s3
from tampering_detection import detect_tampering
from tampering_localization import localize_tampering

app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    video_path = request.json['video_path']
    encrypted_path = "encrypted_video.mp4"
    hash_path = "hash_file.txt"

    key = encrypt_video(video_path, encrypted_path, hash_path)
    upload_to_s3(encrypted_path)
    upload_to_s3(hash_path)

    return jsonify({"message": "Video encrypted and uploaded", "key": key.hex()})

@app.route('/detect-tampering', methods=['POST'])
def detect():
    video_path = request.json['video_path']
    hash_path = request.json['hash_path']

    tampered_frames = detect_tampering(video_path, hash_path)
    return jsonify({"tampered_frames": tampered_frames})

@app.route('/localize-tampering', methods=['POST'])
def localize():
    video_path = request.json['video_path']
    tampered_frames = request.json['tampered_frames']

    localized_changes = localize_tampering(video_path, tampered_frames)
    return jsonify({"localized_changes": localized_changes})

if __name__ == "__main__":
    app.run(debug=True)
