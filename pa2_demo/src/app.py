'''
notes:

python3 -m venv venv
. venv/bin/activate

'''

import json
from flask import Flask, request
import db

app = Flask(__name__)

DB = db.DatabaseDriver()


@app.route("/")
@app.route("/tasks/")
def get_tasks():
    """
    Endpoint for getting all tasks
    """
    return json.dumpts({"tasks": DB.get_all_tasks()}),200


@app.route("/tasks/", methods=["POST"])
def create_task():
    pass


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    pass


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    pass


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
