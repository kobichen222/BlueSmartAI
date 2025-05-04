from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow CORS from any origin for /api/* routes (can be restricted to 'https://bluegun.co.il' if needed)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"status": "error", "error": "לא נשלחה תמונה"}), 400

    image = request.files['image']
    filename = image.filename

    # Simulated AI analysis result
    result = {
        "status": "success",
        "message": "הנשק זוהה בהצלחה",
        "filename": filename
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run()