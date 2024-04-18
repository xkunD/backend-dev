import os
import sqlite3
import datetime

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
    Database driver for the app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection with the database and stores it into the instance variable conn.
        """
        self.conn = sqlite3.connect("user.db", check_same_thread=False)
        self.create_user_table()
        self.create_transaction_table()

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
        
    def create_transaction_table(self):
        """
        Using SQL, create a trasaction table
        """
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                          sender_id INTEGER NOT NULL,
                          receiver_id INTEGER NOT NULL,
                          amount INTEGER NOT NULL,
                          message TEXT NOT NULL,
                          accepted BOOLEAN,
                          FOREIGN KEY (sender_id) REFERENCES user(id),
                          FOREIGN KEY (receiver_id) REFERENCES user(id));""")
        
    def delete_user_table(self):
        """
        Using SQL, delete a user table
        """
        self.conn.execute("""
        DROP TABLE IF EXISTS user;
    """)
        
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
    

    def insert_transactions(self, sender_id, receiver_id, amount, message, accepted):
        """
        Using SQL, inserts a trasaction 
        """
        cursor = self.conn.execute("""
                                   INSERT INTO transactions(sender_id, receiver_id, amount, message, accepted) VALUES (?,?,?,?,?);
                                """, (sender_id, receiver_id, amount, message, accepted))
        self.conn.commit()
        transactions = []
        for row in cursor:
            transactions.append({
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": row[6]
            })  
        return cursor.lastrowid
    

    def get_transaction_by_id(self, tran_id):
        """
        Using SQL, get a transaction by its id
        """
        cursor = self.conn.execute("SELECT * FROM transactions WHERE id = ?;", (tran_id,))
        for row in cursor:
            return({
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": row[6]
            }) 
        return None
          
        
    
    def get_user_by_id(self, user_id):
        """
        Using SQL, get a user by his ID
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?;", (user_id,))
        for row in cursor:
            return ({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})
        return None      


    def get_transactions_of_user(self, user_id):
        """
        Using SQL, get the transactions of a user by its ID
        """
        cursor = self.conn.execute("""
                                   SELECT * FROM transactions WHERE sender_id=? OR receiver_id=?;""",
                                   (user_id, user_id,),
                                   )
        transactions = []
        for row in cursor:
            transactions.append({
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": row[6]
            })
        return transactions

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

    def update_balance_by_id(self, balance, id):
        """
        Using SQL, update the balance of a user
        """
        self.conn.execute("""
                          UPDATE user SET balance = ? WHERE id = ?""", (balance, id))
        self.conn.commit()     
        

    def get_transactioin_accepted_value(self, id):
        """
        Using SQL, get the accepted status of a transaction by its id
        """
        cursor = self.conn.execute("SELECT * FROM transactions WHERE id = ?;", (id,))
        for row in cursor:
            return row[6]
        return None
    
    def update_transaction_accepted_value(self, id, accepted):
        """
        Using SQL, update the accepted status of a transaction by its id
        """
        self.conn.execute("""
                          UPDATE transactions SET accepted = ? WHERE id = ?""", (accepted, id))
        self.conn.commit()   


        


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
