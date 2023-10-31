from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../frontend')

@app.route("/")
def index():
    return render_template('templates/index.html')

@app.route("/main")
def main():
    return render_template('templates/main.html')

@app.route("/search",  methods=['GET', 'POST'])
def search():
    ipaddr=""
    if request.method == 'POST':
        data = request.get_json()
        ipaddr = {'ip':data['ip']}
        return jsonify(ipaddr)

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port=80)

