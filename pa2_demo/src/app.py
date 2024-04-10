'''
notes:

    (terminal go to 'src')
    python3 -m venv venv
    . venv/bin/activate
    pip3 install -r requirements.txt
    python3 app.py
     
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
    return json.dumps({"tasks": DB.get_all_tasks()}), 200


@app.route("/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    description = body.get("description")
    done = body.get("done")
    task_id = DB.insert_task_table(description, done)
    task = DB.get_task_by_id(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 400
    return json.dumps(task), 201


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = DB.get_task_by_id(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 400
    return json.dumps(task), 200


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    """
    Endpoint for updating a task
    """
    body = json.loads(request.data)
    description = body.get("description")
    done = body.get("done")
    task = DB.get_task_by_id(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"})
    DB.update_task_by_id(description, done, task_id)
    task = DB.get_task_by_id(task_id)
    return json.dumps(task), 200 


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = DB.get_task_by_id(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"})
    DB.delete_task_by_id(task_id)
    return json.dumps(task), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
