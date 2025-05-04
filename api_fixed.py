from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'status': 'BlueSmart AI is running'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image'}), 400
    image = request.files['image']
    # כאן מתבצע ניתוח התמונה - לצורך הדגמה נחזיר הצלחה
    return jsonify({
        'status': 'success',
        'filename': image.filename,
        'message': 'Image received and processed successfully'
    })

if __name__ == '__main__':
    app.run(debug=True)