from functools import wraps
from flask import request, jsonify, session
from token_utils import verify_token

def token_required(f):
    
    '''Decorator function to secure Flask routes by requiring a valid token.
       Ensures that only authenticated users can access the wrapped endpoint.'''
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token_parts = auth_header.split()
            if len(token_parts) == 2 and token_parts[0].lower() == 'bearer':
                token = token_parts[1]

        # If no token is provided, clear session and respond with an error
        if not token:
            session.pop('username', None)
            session.pop('logged_in', None)
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify the token
            decoded_data = verify_token(token)
            if not decoded_data:
                # Clear session if token is invalid
                session.pop('username', None)
                session.pop('logged_in', None)
                return jsonify({'message': 'Token is invalid or expired!'}), 401
            
            request.user = decoded_data['username']
            
        except Exception as e:
            # Handle general token verification exceptions
            return jsonify({'message': 'Token is invalid!'}), 401

        # Proceed with the original function if token is valid
        return f(*args, **kwargs)

    return decorated
