import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return json.dumps({"users": DB.get_all_users()}),200

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance", 0)
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    return json.dumps(user), 201

@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by its ID
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    transactions = DB.get_transactions_of_user(user_id)
    user["transactions"] = transactions
    return json.dumps(user), 200

@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user by his ID
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    transactions = DB.get_transactions_of_user(user_id)
    user["transactions"] = transactions
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200

@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Send money from one user to another
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    if sender_id is None or receiver_id is None or amount is None:
        return json.dumps({"error": "Invalid Input"}), 400
    sender_balance = DB.get_balance_by_id(sender_id)
    receiver_balance = DB.get_balance_by_id(receiver_id)
    if sender_balance is None or receiver_balance is None:
        return json.dumps({"error": "User not found"}), 400
    if sender_balance < amount:
        return json.dumps({"error": "User balance overdraft"}), 400
    sender_balance -= amount
    receiver_balance += amount
    DB.update_balance_by_id(sender_balance, sender_id)
    DB.update_balance_by_id(receiver_balance, receiver_id)
    return json.dumps({"sender_id": sender_id,
    "receiver_id": receiver_id,
    "amount": amount}), 200


@app.route("/api/transactions/", methods=["POST"])
def send_or_request_money():
    """
    Send money from one user to another, or request money from one user to another
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    message = body.get("message")
    accepted = body.get("accepted")
    
    sender = DB.get_user_by_id(sender_id)
    receiver = DB.get_user_by_id(receiver_id)
    if sender is None or receiver is None:
        return json.dumps({"error": "User not found"}), 400
    
    if accepted is None:
        DB.insert_transactions(sender_id, receiver_id, amount, message, accepted)
        




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
