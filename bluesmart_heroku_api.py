from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    # This is just a simulation, it should be connected to a real model
    result = {
        "status": "success",
        "weapon_type": "אקדח",
        "manufacturer": "גלוק",
        "model": "43X",
        "condition": "תקין",
        "year": "2019"
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)