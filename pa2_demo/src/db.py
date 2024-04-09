import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection with the database and stores it into the instance variable conn.
        """
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        
    def create_task_table(self):
        '''
        Using SQL, creates a task table
        '''
        self.conn.execute("""
        CREATE TABLE IF NOT EXIST task(
                          id INTEGER PRIMARY KEY AUTOINCREMENT
                          description TEXT NOT NULL
                          done BOOLEAN NOT NULL
        );""")
    
    def delete_task_table(self):
        """
        Using SQL, delete a task table
        """
        self.conn.execute("""
""")


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
