from flask_bcrypt import Bcrypt
from db import db,insert_one
from bson.objectid import ObjectId

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
        "jobs": [],
        "last_search":{}
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
    
    
def get_job_from_user(username, job_id):
    user = db.users.find_one({"username": username})
    if user is None:
        return None 
    jobs = user.get("jobs", [])
    for job in jobs:
        if job.get("job_id") == job_id:
            return job
    return None

def update_job_in_user(username, job):
    """
    Updates a job in the user's list of jobs.

    Parameters:
    - username (str): The username of the user.
    - job (dict): The job data to update, which must include a 'job_id' key.

    Returns:
    - bool: True if the job was updated successfully, False otherwise.
    """
    if "job_id" not in job:
        raise ValueError("The job must contain a 'job_id' key.")

    result = db.users.update_one(
        {"username": username, "jobs.job_id": job["job_id"]},
        {"$set": {"jobs.$": job}}
    )

    if result.modified_count > 0:
        return True  
    else:
        return False  



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




def convert_objectids_to_strings(obj):
    if isinstance(obj, list):
        return [convert_objectids_to_strings(item) for item in obj]
    elif isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                new_obj[k] = str(v)
            else:
                new_obj[k] = convert_objectids_to_strings(v)
        return new_obj
    else:
        return obj



def get_user_jobs(username):
    user = db.users.find_one({"username": username})
    if user is None:
        return None  
    jobs = user.get("jobs", [])
    sorted_jobs = sorted(jobs, key=lambda x: x.get('score', 0), reverse=True)
    
    job_ids = []
    for job in sorted_jobs:
        job_id_str = job.get('job_id')
        if job_id_str:
            try:
                job_ids.append(ObjectId(job_id_str))
            except Exception:
                continue  
    
    if not job_ids:
        return sorted_jobs  # No job_ids to process
    
    jobs_data_cursor = db.jobs.find({"_id": {"$in": job_ids}})
    jobs_data = list(jobs_data_cursor)
    
    # Create a mapping from job_id (string) to job data
    jobs_data_dict = {str(job['_id']): job for job in jobs_data}
    
    # Attach full job data to each job in sorted_jobs
    for job in sorted_jobs:
        job_id_str = job.get('job_id')
        job_data = jobs_data_dict.get(job_id_str)
        if job_data:
            # Convert ObjectId in job_data to string
            job_data_processed = convert_objectids_to_strings(job_data)
            job["job"] = job_data_processed
        else:
            job["job"] = None  # Handle missing job data as needed
    
    # Convert any remaining ObjectId instances in sorted_jobs
    sorted_jobs_processed = convert_objectids_to_strings(sorted_jobs)
    return sorted_jobs_processed



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