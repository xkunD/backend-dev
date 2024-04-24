from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

instructor_course_table = db.Table('instructor_course',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

student_course_table = db.Table('student_course',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship('Assignment', back_populates='course', lazy='dynamic')
    instructors = db.relationship('User', secondary=instructor_course_table,
                                  back_populates='instructed_courses')
    students = db.relationship('User', secondary=student_course_table,
                               back_populates='studied_courses')

    def __init__(self, **kwargs):
        """Initialize Course object/entry"""
        self.code = kwargs.get("code", "")
        self.name = kwargs.get ("name", "")

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'assignments': [assignment.serialize_no_course() for assignment in self.assignments],
            'instructors': [instructor.serialize_no_courses() for instructor in self.instructors],
            'students': [student.serialize_no_courses() for student in self.students]
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    instructed_courses = db.relationship('Course',
                                         secondary=instructor_course_table,
                                         back_populates='instructors')
    studied_courses = db.relationship('Course',
                                      secondary=student_course_table,
                                      back_populates='students')

    def serialize(self):
        all_courses = set(self.instructed_courses + self.studied_courses)  # Remove duplicates by using a set
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            'courses': [course.serialize_no_people() for course in all_courses]
        }

    def serialize_no_courses(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.BigInteger, nullable=False)  # Unix timestamp
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', back_populates='assignments')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date,
            'course': self.course.serialize()
        }
    def serialize_for_creation(self):
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date,
            'course': {
                'id': self.course.id,
                'code': self.course.code,
                'name': self.course.name
            }
        }

    def serialize_no_course(self):
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date
        }


