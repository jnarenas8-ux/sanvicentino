from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

if __name__ == '__main__':
    app.run(debug=True)
