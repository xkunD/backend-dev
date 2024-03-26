import json

from flask import Flask
from flask import jsonify
from flask import request
 
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
