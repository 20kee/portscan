from flask import Flask, render_template

app = Flask(__name__, template_folder='../frontend')

@app.route('/')
def index():
    return render_template('templates/index.html')



if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port=80)

