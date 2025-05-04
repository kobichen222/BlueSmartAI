from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://bluegun.co.il"}})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    result = {
        "status": "success",
        "weapon_type": "אקדח",
        "manufacturer": "גלוק",
        "model": "43"
    }
    return jsonify(result), 200
