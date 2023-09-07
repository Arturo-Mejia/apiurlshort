from flask import Flask, render_template
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route("/page/notfound")
def notfound():
    return render_template('notfound.html')

@app.route("/")
def index():
    return render_template('notfound.html')

if __name__ == '__main__':
     app.run(port=8080)