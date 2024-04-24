from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# implement database model classes
class Task(db.Model):
    """
    Task Model
    """
    
    __tablename__ = "tasks"
    id = db.Column (db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        """Initialize Task object/entry"""
        self.description = kwargs.get("description", "")
        self.done = kwargs.get ("done", False)

    def serialize(self):
        """
        Serialize a task object
        """
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done
        }

class Subtask(db.Model):
    """Subtask Model"""

    __tablemane__ = "subtasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"),nullable=False)

    def __init__(self, **kwargs) :

        """ 
        Initialize the subtask obiect
        """
        self.description = kwargs.get("description", "")
        self.done = kwargs.get("done", False)
        self.task_id = kwargs.get("task_id")

    def serialize(self):
        """
        Serialize a subtask object
        """
        return{
            "id": self.id,
            "description": self.description,
            "done": self.done,
            "task_id": self.task_id
        }
        