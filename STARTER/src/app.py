from flask import Flask
import json
from flask import request

app = Flask(__name__)

task_id_counter = 2

tasks = {
    0: {"id": 0, "description": "laundry", "done": False},
    1: {"id": 1, "description": "homework", "done": False},
}

@app.route("/backend")
def hello():
    return "Hello World!"

@app.route("/tasks/")
def get_tasks():
    res = {"tasks" : list(tasks.values())}
    return json.dumps(res), 200

@app.route("/tasks/", methods = ["POST"])
def create_task():
    global task_id_counter
    body = json.loads(request.data)
    description = body.get("description")
    task = {
        "id": task_id_counter,
        "description": description,
        "done": False
    }
    tasks[task_id_counter] = task
    task_id_counter += 1
    return json.dumps(task), 201

@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"error": "Task not found"}), 404
    return json.dumps(task), 200


@app.route("/tasks/<int:task_id>/", methods = ["POST"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"error": "Task not found"}), 404
    body = json.loads(request.data)
    tasks["description"] = body.description
    tasks["done"] = body.done
    return json.dumps(task), 200

@app.route("/tasks/<int:task_id>/", methods = ["DELETE"])
def delete_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"error": "Task not found"}), 404
    del tasks[task_id]
    return json.dumps(task), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
