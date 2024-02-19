import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY

def generate_token(username):
    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=10)},
        JWT_SECRET_KEY,
        algorithm='HS256')
    return token

def verify_token(token):
    try:
        decoded_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
