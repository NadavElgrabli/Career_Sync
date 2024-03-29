from flask import jsonify, request, Blueprint,session
from token_utils import generate_token
from utils import insert_new_user, login_user

app = Blueprint('routes', __name__)

@app.route('/', methods=['GET'])
def handle_get():
    return '<h1> Exemple  </h1>'

@app.route('/register', methods=['POST'])
def handle_post():
    data = request.json
    if insert_new_user(data):
        return 'User successfully added to the database', 200
    else:
        return 'Failed to add user to the database', 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        user = login_user(username, password)
        if user:
            token = generate_token(username)
            if token:
                session['logged_in'] = True
                return jsonify({
                    "message": "Login successful!",
                    "token": token,
                    "user": user
                }), 200
            else:
                return jsonify({"message": "Failed to generate token"}), 500
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception:
        return jsonify({"message": "Internal Server Error"}), 500
