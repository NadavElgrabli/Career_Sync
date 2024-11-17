from flask_bcrypt import Bcrypt
from db import db,insert_one

bcrypt = Bcrypt()

def get_user_data_from_request(data):
    """
    Extracts and returns user data from the provided data dictionary.

    Args:
        data (dict): Dictionary containing user data.

    Returns:
        dict: A dictionary with user data.
    """
    return {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "username": data.get("username"),
        "password": data.get("password"),
        "job": data.get("job"),
        "location": data.get("location"),
        "full_job": data.get("full_job"),
        "work_preference": data.get("work_preference"),
        "experience": data.get("experience"),
        "degree": data.get("degree"),
        "skills": data.get("skills"),
    }


def insert_new_user(data):
    
    """
    Inserts a new user into the database.

    Args:
        data (dict): Dictionary containing user data.

    Returns:
        dict or None: The inserted user data if successful, None otherwise.

    Raises:
        ValueError: If required fields are missing or user insertion fails.
    """
    
    user_data = get_user_data_from_request(data)
    username = user_data.get("username")
    password = user_data.get("password")
    if not username or not password:
        raise ValueError("Both username and password are required.")
    
    if get_user(username):
        raise ValueError("Username already exists.")

    user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')
    try:
        return insert_one(db.users, user_data)
    except ValueError as ve:
        raise ValueError("Failed to insert user.")
    except Exception as e:
        raise ValueError(f"Failed to insert user: {str(e)}")

def get_public_user_data(user):
    
    
    """
    Extracts public user data from the user document.

    Args:
        user (dict): The user data from the database.

    Returns:
        dict: A dictionary with public user data.
    """
    
    return{
        "username": user.get("username"),
        "job": user.get("job"),
        "location": user.get("location"),
        "full_job": user.get("full_job"),
        "work_preference": user.get("work_preference"),
        "experience": user.get("experience"),
        "degree": user.get("degree"),
        "skills": user.get("skills"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
    }
def get_user(username):
    
    """
    Retrieves a user from the database by username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        dict or None: The user data if found, None otherwise.
    """
    
    
    try:
        user = db.users.find_one({"username": username})
        return user
    except Exception as e:
        return None
    
def authenticate_user(user, password):
    
    """
    Authenticates a user by comparing the provided password with the stored hashed password.

    Args:
        user (dict): The user data from the database.
        password (str): The plaintext password to verify.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    
    hashed_password = user.get("password")
    if not hashed_password:
        return False
    return bcrypt.check_password_hash(hashed_password, password)


from bson import ObjectId

def get_user_jobs(username):
    """
    Retrieves all jobs associated with a user from the database by username,
    including job scores.

    Args:
        username (str): The username of the user whose jobs to retrieve.

    Returns:
        list or None: A list of job data with scores if found, None otherwise.
    """
    
    try:
        user = get_user(username)
        
        if not user or "jobs" not in user:
            return None
        
        job_ids = [ObjectId(job["id"]) for job in user["jobs"]]
        job_scores = {job["id"]: job["job_score"] for job in user["jobs"]}
        
        jobs = list(db.jobs.find({"_id": {"$in": job_ids}}))
        
        for job in jobs:
            job_id_str = str(job["_id"])
            job["job_score"] = job_scores.get(job_id_str, None)
        
        return jobs if jobs else None
    except Exception as e:
        return None

def login_user(username, password):
    
    
    """
    Attempts to log in a user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password of the user.

    Returns:
        dict or None: User data (excluding password) if login is successful, None otherwise.
    """
    
    user = get_user(username)
    
    if user:
        if authenticate_user(user, password):
            return get_public_user_data(user)
    return None