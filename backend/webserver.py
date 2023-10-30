from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../frontend')

@app.route("/",  methods=['GET', 'POST'])
def index():
    ipaddr=""
 
    if request.method == 'POST':
        ipaddr = request.form.get("ip")
    return render_template('templates/index.html',ipaddr=ipaddr)

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.1.169', port=80)
