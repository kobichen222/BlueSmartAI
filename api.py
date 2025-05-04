
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # מאפשר CORS לכל המקורות

@app.route('/')
def index():
    return 'BlueSmart AI API is running!'

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image'}), 400
    image = request.files['image']
    # כאן תוכל להוסיף לוגיקת ניתוח עתידית
    return jsonify({'result': 'Image received successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
