from flask import jsonify, request, Blueprint
from db import db
from utils import bcrypt, insert_new_user

app = Blueprint('routes', __name__)

@app.route('/', methods=['GET'])
def handle_get():
    return '<h1> Exemple  </h1>'

@app.route('/register', methods=['POST'])
def handle_post():
    data = request.json
    if insert_new_user(data, db.users):
        return 'User successfully added to the database', 200
    else:
        return 'Failed to add user to the database', 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = db.users.find_one({"username": username})
    if user:
        hashed_password = user.get("password")
        if bcrypt.check_password_hash(hashed_password, password):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid password"}), 401
    else:
        return jsonify({"message": "User not found"}), 404
