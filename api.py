from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import os
from urllib.parse import urljoin

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '🔵 ShotMark AI - ניתוח פגיעות'

@app.route('/app')
def interface():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "❌ לא נשלחה תמונה"}), 400

    try:
        file = request.files['image']
        image = Image.open(file.stream).convert('RGB')
        image_np = np.array(image)

        h, w = image_np.shape[:2]
        roi = image_np[h//5:h*4//5, w//6:w*5//6]
        gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hit_count = 0
        for c in contours:
            area = cv2.contourArea(c)
            if 30 < area < 300:
                x, y, w2, h2 = cv2.boundingRect(c)
                cv2.circle(roi, (x + w2//2, y + h2//2), 10, (255, 0, 0), 2)
                hit_count += 1

        image_np[h//5:h*4//5, w//6:w*5//6] = roi
        result_path = os.path.join(UPLOAD_FOLDER, 'result.jpg')
        cv2.imwrite(result_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

        return jsonify({
            "status": "success",
            "message": f"✅ זוהו {hit_count} פגיעות במטרה",
            "hits": hit_count,
            "image_url": urljoin(request.url_root, 'static/result.jpg')
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)