from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many relationship between Courses and Users
course_user_table = db.Table('course_user',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship('Assignment', back_populates='course', lazy='dynamic')
    instructors = db.relationship('User', secondary=course_user_table,
                                  back_populates='instructed_courses')
    students = db.relationship('User', secondary=course_user_table,
                               back_populates='studied_courses')

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
                                         secondary=course_user_table,
                                         back_populates='instructors')
    studied_courses = db.relationship('Course',
                                      secondary=course_user_table,
                                      back_populates='students')

    def serialize(self):
        all_courses = set(self.instructed_courses + self.studied_courses) 
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

    def serialize_no_course(self):
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date
        }

