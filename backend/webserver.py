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
        Stype = data['Stype']
        ip = data['ip']
        try:
            minport = int(data['minPort'])
            maxport = int(data['maxPort'])
        except:
            return jsonify({'error': '포트에 숫자만 입력하세요'})

        if maxport>65535:
            maxport=65535
        if minport<0:
            minport=0
        if minport>maxport:
            return jsonify({'error': '최소 포트가 더 큽니다.'})
        if ip=='127.0.0.1' or ip=='0.0.0.0':
            return jsonify({'error': '해당 아이피는 검색 할 수 없습니다..'})
        ips=ip.split('.')
        
        if ips[0]=='127' and ips[1]=='0'  and ips[2]=='0':
            return jsonify({'error': '해당 아이피는 검색 할 수 없습니다..'})

        if Stype == 's2':
            results = scanner.scan(data['ip'], int(data['minPort']), int(data['maxPort']))
        elif Stype == 's1':
            results = scanner.half_open_scan(ip, int(data['minPort']), int(data['maxPort']))
        else:   
            return jsonify({'error': '스캐너 선택이 잘못됨'})
        return results
    else:
        return jsonify({'error': 'Method not allowed'})

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=80)

