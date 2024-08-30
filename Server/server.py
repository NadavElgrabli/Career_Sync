from flask import Flask
from routes import app as routes_app
from config import JWT_SECRET_KEY
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = JWT_SECRET_KEY
CORS(app)


app.register_blueprint(routes_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
