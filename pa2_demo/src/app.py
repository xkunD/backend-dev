import json
from flask import Flask, request

app = Flask(__name__)



@app.route("/")
@app.route("/tasks/")
def get_tasks():
    pass


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
