from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import numpy as np
import cv2
import os
from PIL import Image
from urllib.parse import urljoin
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '🔵 ShotMark AI פעיל - העלה תמונה דרך /app או שלח לניתוח דרך /api/analyze'

@app.route('/app')
def interface():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({ "status": "error", "message": "לא נשלחה תמונה" }), 400

    try:
        file = request.files['image']
        image = Image.open(file.stream).convert('RGB')
        image_np = np.array(image)

        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

        # זיהוי קונטור של המטרה
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(gray)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 30000 < area < 3000000:
                cv2.drawContours(mask, [cnt], -1, 255, -1)

        # מציאת חורים (פגיעות ירי)
        edges = cv2.Canny(gray, 30, 150)
        holes, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        output = image_np.copy()
        hit_count = 0

        for c in holes:
            area = cv2.contourArea(c)
            if 40 < area < 200:
                x, y, w, h = cv2.boundingRect(c)
                cx, cy = x + w // 2, y + h // 2
                if mask[cy, cx] > 0:
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    hit_count += 1

        # שמירת התוצאה
        result_filename = f'result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        result_path = os.path.join(UPLOAD_FOLDER, result_filename)
        cv2.imwrite(result_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

        return jsonify({
            "status": "success",
            "hits": hit_count,
            "message": f"זוהו {hit_count} פגיעות חוקיות בתוך המטרה",
            "image_url": urljoin(request.url_root, 'static/' + result_filename)
        })

    except Exception as e:
        return jsonify({ "status": "error", "message": f"שגיאה פנימית: {str(e)}" }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)