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
        self.conn = sqlite3.connect("user.db", check_same_thread=False)
        self.create_user_table()

    def create_user_table(self):
        '''
        Using SQL, creates a user table
        '''
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          username TEXT NOT NULL,
                          balance INTEGER NOT NULL);""")

    def get_all_users(self):
        """
        Using SQL, return all the users in a table
        """
        cursor = self.conn.execute("SELECT * FROM user;")
        users = []
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users
    
    def insert_user_table(self, name, username, balance):
        '''
        Using SQL, inserts a user into a user table
        '''
        cursor = self.conn.execute("""
                                   INSERT INTO user(name, username, balance) VALUES (?, ?, ?);""", (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_by_id(self, user_id):
        """
        Using SQL, get a user by his ID
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?;", (user_id,))
        for row in cursor:
            return ({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})
        return None        

    def delete_user_by_id(self, id):
        """
        Using SQL, delete a user by his ID
        """
        self.conn.execute("""
                          DELETE FROM user WHERE id=?""", (id,))

    def get_balance_by_id(self, user_id):
        """
        Using SQL, get a user's balance by his iD
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?;", (user_id,))
        for row in cursor:
            return row[3]
        return None       
        



# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
