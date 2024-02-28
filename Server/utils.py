from flask_bcrypt import Bcrypt
from db import db,insert_one

bcrypt = Bcrypt()

def insert_new_user(data):
    try:
       
        username = data.get("username")
        password = data.get("password")
        if not (username and password):
            raise ValueError("Both username and password are required.")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        job = data.get("job", None)
        location = data.get("location", None)
        full_job = data.get("full_job", None)
        work_preference = data.get("work_preference", None)
        experience = data.get("experience", None)
        degree = data.get("degree", None)

        
        user = {
            "username": username,
            "password": hashed_password,
            "job": job,
            "location": location,
            "full_job": full_job,
            "work_preference": work_preference,
            "experience": experience,
            "degree": degree
        }
        
        return insert_one(db.users, user)

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
        "degree": user.get("degree")
    }
def get_user(username):
    try:
        user = db.users.find_one({"username": username})
        return user
    except Exception as e:
        return None
    
def authenticate_user(user, password):
    hashed_password = user.get("password")
    return bcrypt.check_password_hash(hashed_password, password)

def login_user(username, password):
    user = get_user(username)
    if user:
        if authenticate_user(user, password):
            return get_user_data(user)
    return None