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
@app.route("/tasks/", method = ["POST"])
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
