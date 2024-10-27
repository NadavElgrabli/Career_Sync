import jwt
from datetime import datetime, timedelta, timezone
from config import JWT_SECRET_KEY

def generate_token(username, expiration_minutes=10):
    """
    Generates a JWT token for a given username.

    Args:
        username (str): The username for whom the token is generated.
        expiration_minutes (int, optional): Token expiration time in minutes. Defaults to 10.

    Returns:
        str: Encoded JWT token as a string.
    """
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    payload = {
        'username': username,
        'exp': expiration_time
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """
    Verifies a JWT token and returns the decoded data if valid.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict or None: Decoded token data if valid, None otherwise.
    """
    try:
        decoded_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
