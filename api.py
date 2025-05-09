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
def analyze():
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

        # מסכת עיגול מטרה
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (cx, cy), radius, 255, -1)

        # עיבוד תמונה
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # זיהוי חורי ירי
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
            param1=50, param2=25, minRadius=4, maxRadius=12
        )

        output = image_np.copy()
        hit_count = 0
        hit_coords = []

        if circles is not None:
            for x, y, r in np.uint16(np.around(circles[0])):
                distance = np.sqrt((x - cx)**2 + (y - cy)**2)
                if distance < radius and mask[y, x] == 255:
                    hit_count += 1
                    hit_coords.append({ "x": int(x), "y": int(y) })
                    cv2.circle(output, (x, y), r, (0, 255, 0), 2)

        # ניתוח AI
        if hit_count >= 15:
            summary = "רמת ירי יוצאת דופן – צלף מקצועי עם ריכוז גבוה ואפס סטייה."
            score = 98
        elif hit_count >= 10:
            summary = "רמה גבוהה מאוד – ריכוז טוב, סטייה מינימלית, שליטה טובה."
            score = 92
        elif hit_count >= 5:
            summary = "ירי בינוני – פגיעות סבירות אך דרוש תרגול לשיפור ריכוז."
            score = 75
        elif hit_count > 0:
            summary = "פגיעות בודדות – מומלץ אימון בסיסי נוסף על מיקוד ואחיזה."
            score = 55
        else:
            summary = "לא זוהו פגיעות חוקיות – יש לבדוק תנוחת ירי ולחזור על האימון."
            score = 30

        # שמירה
        result_filename = f'result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        result_path = os.path.join(UPLOAD_FOLDER, result_filename)
        cv2.imwrite(result_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{shooter},{weapon},{distance},{hit_count},{now}\n")

        return jsonify({
            "status": "success",
            "message": f"✅ זוהו {hit_count} פגיעות חוקיות במטרה",
            "hits": hit_count,
            "hit_coords": hit_coords,
            "image_url": urljoin(request.url_root, 'static/' + result_filename),
            "shooter": shooter,
            "weapon": weapon,
            "distance": distance,
            "timestamp": now,
            "ai_score": score,
            "analysis_summary": summary
        })

    except Exception as e:
        return jsonify({ "status": "error", "message": f"שגיאת ניתוח: {str(e)}" }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)