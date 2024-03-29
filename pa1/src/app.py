import json

from flask import Flask
from flask import jsonify
from flask import request
 
app = Flask(__name__)

post_id_counter = 2
comment_id_counter = 0

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

comments = {
    0: [
        {"id": 0, "upvotes": 8, "text": "Wow, my first Reddit gold!", "username": "alicia98"},
        {"id": 1, "upvotes": 1, "text": "I want one!", "username": "dogperson"},
    ],
}

@app.route("/")
def hello_world():
    return "Hello world!"


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

@app.route("/api/posts/<int:post_id>/")
def get_post(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/", methods = ["DELETE"])
def delete_post(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    del posts[post_id]
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/comments/")
def get_comments(post_id):
    post_comments = comments.get(post_id)
    return json.dumps({"comments": post_comments}), 200

@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def create_comment(post_id):
    global comment_id_counter
    body = request.json
    comment = {"id": comment_id_counter, "upvotes": 1, **body}
    if post_id in comments:
        comments[post_id].append(comment)
    else:
        comments[post_id] = [comment]
    comment_id_counter += 1
    return json.dumps(comment), 201

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    body = request.json
    for comment in comments.get(post_id, []):
        if comment['id'] == comment_id:
            comment['text'] = body.get('text', comment['text'])
            return json.dumps(comment), 200
    return json.dumps({"error": "Comment not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
