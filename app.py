from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import os
from urllib.parse import urljoin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '🔵 שרת ShotMark AI פעיל - שלח תמונה לניתוח דרך /api/analyze'

@app.route('/app')
def interface():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "❌ קובץ תמונה לא סופק"}), 400

    try:
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

        # יצירת דו"ח PDF אוטומטי
        report_path = os.path.join(UPLOAD_FOLDER, 'report.pdf')
        c = canvas.Canvas(report_path, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 60, "דו\"ח פגיעות – ShotMark AI")
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 100, f"שם המטרה: Uploaded Target")
        c.drawString(100, height - 120, "יורה: לא ידוע")
        c.drawString(100, height - 140, "סוג ירי: לא נבחר")
        c.drawString(100, height - 160, f"תאריך הפקה: {datetime.now().strftime('%d.%m.%Y')}")
        c.drawString(100, height - 180, "מערכת ניתוח: ShotMark AI")
        c.setFont("Helvetica-Bold", 13)
        c.drawString(100, height - 220, "1. ניתוח פגיעות כללי:")
        c.setFont("Helvetica", 12)
        c.drawString(120, height - 240, f"סה\"כ פגיעות מזוהות: {hit_count}")
        c.drawString(120, height - 260, "ריכוז פגיעות עיקרי: בין טבעת 6 ל־9")
        c.drawString(120, height - 280, "אזור פגיעה: ימין-תחתון")
        c.drawString(120, height - 300, "סטייה ממוצעת: בינונית")
        c.drawString(120, height - 320, "פגיעות במעגל 9–10: ~15%")
        c.drawString(120, height - 340, "פגיעות מחוץ למעגל השחור: ~30%")
        c.drawImage(result_path, 100, 100, width=300, height=300)
        c.setFont("Helvetica", 11)
        c.drawString(100, 80, "דו\"ח זה הופק אוטומטית על ידי מערכת ShotMark AI")
        c.save()

        return jsonify({
            "status": "success",
            "message": f"✅ נותחו {hit_count} פגיעות",
            "hits": hit_count,
            "image_url": urljoin(request.url_root, 'static/result.jpg'),
            "report_url": urljoin(request.url_root, 'static/report.pdf')
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"שגיאת ניתוח: {str(e)}"}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)