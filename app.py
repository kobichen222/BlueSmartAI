from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import os
from urllib.parse import urljoin
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static'
HISTORY_FILE = 'history.csv'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '🔵 ShotMark AI פעיל - שלח תמונה לניתוח דרך /api/analyze'

@app.route('/app')
def interface():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_view():
    if 'image' not in request.files:
        return jsonify({ "status": "error", "message": "❌ קובץ תמונה לא סופק" }), 400

    try:
        shooter = request.form.get('shooter', 'לא ידוע')
        weapon = request.form.get('weapon', 'לא צויין')
        distance = request.form.get('distance', 'לא ידוע')

        file = request.files['image']
        image = Image.open(file.stream).convert('RGB')
        image_np = np.array(image)

        h, w = image_np.shape[:2]
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 3
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (cx, cy), radius, 255, -1)

        target_area = cv2.bitwise_and(image_np, image_np, mask=mask)
        gray = cv2.cvtColor(target_area, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 30, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output = image_np.copy()
        hit_count = 0
        miss_count = 0

        for c in contours:
            area = cv2.contourArea(c)
            if 50 < area < 300:
                x, y, w2, h2 = cv2.boundingRect(c)
                cx2, cy2 = x + w2 // 2, y + h2 // 2
                distance_from_center = np.sqrt((cx - cx2)**2 + (cy - cy2)**2)
                if distance_from_center < radius:
                    cv2.circle(output, (cx2, cy2), 10, (255, 0, 0), 2)  # Blue for hit
                    hit_count += 1
                else:
                    cv2.circle(output, (cx2, cy2), 10, (0, 0, 255), 2)  # Red for miss
                    miss_count += 1

        result_filename = f'result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        result_path = os.path.join(UPLOAD_FOLDER, result_filename)
        cv2.imwrite(result_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{shooter},{weapon},{distance},{hit_count},{miss_count},{now}\n")

        return jsonify({
            "status": "success",
            "message": f"✅ זוהו {hit_count} פגיעות בתוך עיגול המטרה ו-{miss_count} מחוץ",
            "hits": hit_count,
            "misses": miss_count,
            "image_url": urljoin(request.url_root, 'static/' + result_filename),
            "shooter": shooter,
            "weapon": weapon,
            "distance": distance,
            "timestamp": now
        })

    except Exception as e:
        return jsonify({ "status": "error", "message": f"שגיאת ניתוח: {str(e)}" }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
}
@app.route('/api/analyze', methods=['POST'])
def analyze_view():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "❌ קובץ תמונה לא סופק"}), 400

    try:
        shooter = request.form.get('shooter', 'לא ידוע')
        weapon = request.form.get('weapon', 'לא צויין')
        distance = request.form.get('distance', 'לא ידוע')

        file = request.files['image']
        image = Image.open(file.stream).convert('RGB')
        image_np = np.array(image)

        h, w = image_np.shape[:2]
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 3

        # Blob Detector parameters
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 30
        params.maxArea = 300
        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False

        detector = cv2.SimpleBlobDetector_create(params)

        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        keypoints = detector.detect(blurred)

        output = cv2.drawKeypoints(
            image_np, keypoints, np.array([]),
            (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )

        hit_count = 0
        miss_count = 0

        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            distance_from_center = np.sqrt((cx - x) ** 2 + (cy - y) ** 2)
            if distance_from_center < radius:
                hit_count += 1
            else:
                miss_count += 1

        result_filename = f'result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        result_path = os.path.join(UPLOAD_FOLDER, result_filename)
        cv2.imwrite(result_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{shooter},{weapon},{distance},{hit_count},{miss_count},{now}\n")

        return jsonify({
            "status": "success",
            "message": f"✅ זוהו {hit_count} פגיעות במטרה ו-{miss_count} מחוץ",
            "hits": hit_count,
            "misses": miss_count,
            "image_url": urljoin(request.url_root, 'static/' + result_filename),
            "shooter": shooter,
            "weapon": weapon,
            "distance": distance,
            "timestamp": now
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"שגיאת ניתוח: {str(e)}"}), 500