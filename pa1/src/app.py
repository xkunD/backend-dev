import json

from flask import Flask
from flask import jsonify
from flask import request
 
app = Flask(__name__)

post_id_counter = 2

posts = {
    0: {"id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",},
    1: {"id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98"},
}


@app.route("/api/posts/")
def get_posts():
    res = {"posts" : list(posts.values())}
    return json.dumps(res), 200


@app.route("/api/posts/", methods = ["POST"])
def create_post():
    global post_id_counter
    body = json.loads(request.data)
    description = body.get("description")
    post = {
        "id": post_id_counter,
        "description": description,
        "done": False
    }
    posts[post_id_counter] = post
    post_id_counter += 1
    return json.dumps(post), 201

@app.route("/api/posts/<int:task_id>/")
def get_post(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

@app.route("/api/posts/<int:task_id>/", methods = ["DELETE"])
def delete_task(task_id):
    task = posts.get(task_id)
    if not task:
        return json.dumps({"error": "Task not found"}), 404
    del posts[task_id]
    return json.dumps(task), 200



@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
