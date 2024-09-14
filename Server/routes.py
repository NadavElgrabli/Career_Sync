from flask import jsonify, request, Blueprint,session
from algorithm.chatbot import Chatbot
from token_utils import generate_token
from utils import insert_new_user, login_user
from flask_cors import CORS
app = Blueprint('routes', __name__)
CORS(app)

@app.route('/', methods=['GET'])
def handle_get():
    return '<h1> Exemple  </h1>'

@app.route('/signup', methods=['POST'])
def handle_post():
    data = request.json
    newUser = insert_new_user(data)
    if newUser:
        return jsonify(data), 200
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

chatbot = Chatbot()


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")

        if user_message == "start":
            bot_response = "Hello! Welcome to Career Sync. What job are you looking for?"
        else:
            bot_response = chatbot.ask_question(user_message)

        return jsonify({"response": bot_response}), 200
    except Exception as e:
        print(f"Error during chatbot conversation: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
