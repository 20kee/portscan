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
        minport=0
        maxport=65535
        try:
            minport = int(data['minPort'])
            maxport = int(data['maxPort'])
        except:
            return jsonify({'error': '포트에 숫자만 입력하세요^^'})

        if maxport>65535:
            maxport=65535
        if minport<0:
            minport=0
        if minport>maxport:
            return jsonify({'error': '최소 포트가 더 크잖아'})
        
        if '스캐너' == '스캐너':
            results = scanner.scan(data['ip'], int(data['minPort']), int(data['maxPort']))
        elif '하프오픈' == '하프오픈':
            results = scanner.scan(data['ip'], int(data['minPort']), int(data['maxPort']))

        return results
    else:
        return jsonify({'error': 'Method not allowed'})

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.1.169', port=80)

