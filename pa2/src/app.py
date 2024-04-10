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
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    user_id = DB.insert_user_table(name, username)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "Task not Found"}), 400
    return json.dumps(user), 201









if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
