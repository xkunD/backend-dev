from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("task_id", db.Integer, db.ForeignKey("tasks.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id"))
)


# implement database model classes
class Task(db.Model):
    """
    Task Model
    """
    
    __tablename__ = "tasks"
    id = db.Column (db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    subtasks = db.relationship("Subtask", cascade="delete")
    categories = db.relationship("Category", secondary=association_table, back_populates="taskss")

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
            "done": self.done,
            "subtasks": [s.serialize() for s in self.subtasks],
            "categories": [c.simple_serialize() for c in self.categories]
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
        
class Category(db.Model):
    """
    Category Model
    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable =False)
    color = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task",secondary=association_table, back_populates="categories")

    def __init__(self, **kwargs):
        """
        Initialize a category object
        """
        self.description = kwargs.get("description")
        self.color = kwargs.get("color")

    def serialize(self):
        """
        Serialize a category object
        """
        return{
            "id": self.id,
            "description": self.description,
            "color": self.color,
            "tasks": [t.serialize() for t in self.tasks]
        }
    
    def simple_serialize(self):
        return{
            "id": self.id,
            "description": self.description,
            "color": self.color,
        }
    