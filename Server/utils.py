from flask_bcrypt import Bcrypt
from db import db,insert_one

bcrypt = Bcrypt()

def _get_user_data(data):
    return {
        "first_name": data.get("firstName", None),
        "last_name": data.get("lastName", None),
        "username": data.get("username"),
        "password": data.get("password"),
        "job": data.get("job", None),
        "location": data.get("location", None),
        "full_job": data.get("full_job", None),
        "work_preference": data.get("work_preference", None),
        "experience": data.get("experience", None),
        "degree": data.get("degree", None),
        "skills": data.get("skills", None),
    }


def insert_new_user(data):
    try:
        user_data = _get_user_data(data)
        if not user_data.get("username") or not user_data.get("password"):
            raise ValueError("Both username and password are required.")

        user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')

        return insert_one(db.users, user_data)

    except ValueError as ve:
        raise ve 
    except Exception as e:
        raise ValueError(f"Failed to insert user: {str(e)}")

def get_user_data(user):
    return{
        "username": user.get("username"),
        "job": user.get("job"),
        "location": user.get("location"),
        "full_job": user.get("full_job"),
        "work_preference": user.get("work_preference"),
        "experience": user.get("experience"),
        "degree": user.get("degree"),
        "skills": user.get("skills"),
        "firstName": user.get("first_name"),
        "lastName": user.get("last_name"),
    }
def get_user(username):
    try:
        user = db.users.find_one({"username": username})
        print(user)
        return user
    except Exception as e:
        return None
    
def authenticate_user(user, password):
    hashed_password = user.get("password")
    ans = bcrypt.check_password_hash(hashed_password, password)
    return ans

def login_user(username, password):
    user = get_user(username)
    
    if user:
        if authenticate_user(user, password):
            return get_user_data(user)
    return None