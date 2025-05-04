from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    return jsonify({'status': 'success', 'result': 'Weapon OK'})

if __name__ == '__main__':
    app.run(debug=True)
