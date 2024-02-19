from flask_bcrypt import Bcrypt


def insert_new_user(data, collection):
    try:
        username = data.get("username")
        password = data.get("password")
        if not (username and password):
            raise ValueError("Both username and password are required.")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = {
            "username": username,
            "password": hashed_password
        }
        result = collection.insert_one(user)
        return bool(result.inserted_id)
    except Exception as e:
        raise ValueError(f"Failed to insert user: {str(e)}")


bcrypt = Bcrypt()


