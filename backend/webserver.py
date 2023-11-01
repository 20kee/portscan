from flask import Flask, render_template, request, jsonify
from leechangmin.scanner import NormalScanner

app = Flask(__name__,static_folder='../frontend/static', template_folder='../frontend')

@app.route("/")
def index():
    return render_template('templates/index.html')

@app.route("/main")
def main():
    return render_template('templates/main.html')

@app.route("/search",  methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.get_json()
        scanner = NormalScanner()
        results = scanner.scan(data['ip'], 1, 5000)
        return results
    else:
        return jsonify({'error': 'Method not allowed'})

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.1.169', port=80)

