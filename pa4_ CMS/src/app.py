import json
from flask import Flask, request, jsonify
from db import db, Course, User, Assignment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return jsonify(data), code

def failure_response(message, code=400):
    return jsonify({"error": message}), code

# ------------------- Course Routes -------------------
@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/courses/")
def get_all_courses():
    """
    Endpoint for getting all courses
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})

@app.route("/api/courses/", methods=["POST"])
def create_course():
    data = json.loads(request.data)
    if not data.get("code") or not data.get("name"):
        return failure_response("Missing course code or name", 400)
    course = Course(code=data["code"], name=data["name"])
    db.session.add(course)
    db.session.commit()
    return success_response(course.serialize(), 201)

@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return failure_response("Course not found", 404)
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.filter_by(id = course_id).first()
    if course is None:
        return failure_response("Course not found!")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


# ------------------- User Routes -------------------

@app.route("/api/users/", methods=["POST"])
def create_user():
    data = json.loads(request.data)
    if not data.get("name") or not data.get("netid"):
        return failure_response("Missing user name or netid", 400)
    user = User(name=data["name"], netid=data["netid"])
    db.session.add(user)
    db.session.commit()
    return success_response(user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return failure_response("User not found", 404)
    return success_response(user.serialize())

# ------------------- Assignment and Enrollment Routes -------------------
@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return failure_response("Course not found", 404)

    data = json.loads(request.data)
    user_id = data.get("user_id")
    type_ = data.get("type")
    
    if not user_id or not type_:
        return failure_response("Missing user ID or type", 400)

    user = User.query.get(user_id)
    if user is None:
        return failure_response("User not found", 404)

    if type_ == "student":
        if user in course.instructors:
            course.instructors.remove(user)
        if user not in course.students:
            course.students.append(user)
    elif type_ == "instructor":
        if user in course.students:
            course.students.remove(user)
        if user not in course.instructors:
            course.instructors.append(user)
    else:
        return failure_response("Invalid type specified. Choose 'student' or 'instructor'.", 400)

    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    course = Course.query.get(course_id)
    if not course:
        return failure_response("Course not found", 404)  

    data = json.loads(request.data)
    if not data or 'title' not in data or 'due_date' not in data:
        return failure_response("Missing title or due date for assignment", 400)

    assignment = Assignment(title=data["title"], due_date=data["due_date"], course_id=course_id)
    db.session.add(assignment)
    db.session.commit()
    return success_response(assignment.serialize_for_creation(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
