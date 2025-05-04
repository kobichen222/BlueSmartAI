from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>🎯 BlueSmart AI פעיל</h1><p>שלח בקשות POST ל-<code>/api/analyze</code></p>"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    return jsonify({'status': 'success', 'result': 'Weapon OK'})

if __name__ == '__main__':
    app.run(debug=True)
