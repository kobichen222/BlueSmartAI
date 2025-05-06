from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '🔵 שרת ShotMark AI פועל! שלח תמונה לניתוח דרך /api/analyze'

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "קובץ תמונה לא סופק"}), 400

    file = request.files['image']
    image = Image.open(file.stream).convert('RGB')
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = image_np.copy()
    hit_count = 0

    for c in contours:
        area = cv2.contourArea(c)
        if 50 < area < 300:
            x, y, w, h = cv2.boundingRect(c)
            cv2.circle(output, (x + w//2, y + h//2), 10, (255, 0, 0), 2)
            hit_count += 1

    result_path = os.path.join(UPLOAD_FOLDER, 'result.jpg')
    cv2.imwrite(result_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

    return jsonify({
        "status": "success",
        "hits": hit_count,
        "image_url": request.url_root + 'static/result.jpg'
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)