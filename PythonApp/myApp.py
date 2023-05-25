from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user/<name>")
def hello_user(name):
    return f"<p>Hello, {escape(name)}!</p>"

if __name__ == "__main__":
    app.run(debug=True)