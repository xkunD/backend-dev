import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return json.dumps({"tasks": DB.get_all_users()}),200

@app.route("/api/users/")
def create_user():
    """
    """






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
