import re

# Function to extract work preference from job description
def extract_work_preference(description):
    
    if re.search(r'\b(remote|work from home|telecommute|fully remote|anywhere)\b', description):
        return 'Remote'
    elif re.search(r'\b(on-site|on site|office-based|in-office|in office)\b', description):
        return 'Onsite'
    elif re.search(r'\b(hybrid|flexible work|partially remote)\b', description):
        return 'Hybrid'
    else:
        return 'Not Specified'

# Function to extract required years of experience from job description
def extract_experience(description):
    matches = re.findall(r'(\d+)\+?\s+years? of experience', description)
    if matches:
        return int(matches[0])
    else:
        return None  # Experience not specified

# Function to extract required degree fields from job description
def extract_degree_fields(description):
    description = description
    # Pattern to match phrases like 'degree in computer science', 'bachelor's in computer science'
    pattern = r"(?:bachelor's|master's|phd|doctorate)?\s*(?:degree)?\s*(?:in|of)\s+([\w\s&\-,]+)"
    matches = re.findall(pattern, description)
    if matches:
        # Clean and return list of degree fields
        fields = [match.strip().strip('.').strip(',') for match in matches]
        return fields  # Return a list of fields
    else:
        return []  # Return empty list if no fields found

# Function to check if candidate's degree field is mentioned anywhere in the description
def is_degree_field_in_description(description, candidate_degree_field):
    
    candidate_field = candidate_degree_field.lower()
    # Use word boundaries to avoid partial matches
    pattern = r'\b' + re.escape(candidate_field) + r'\b'
    if re.search(pattern, description):
        return True
    else:
        return False

# Updated function to calculate job title score
def calculate_job_title_score(job_title, candidate_profile):
    preferred_titles = candidate_profile.get('preferred_job_titles', '')
    if isinstance(preferred_titles, str):
        preferred_titles = [preferred_titles]
    else:
        preferred_titles = list(preferred_titles)  # Ensure it's a list
    if job_title.lower() in [title.lower() for title in preferred_titles]:
        return 1.0  # Full score
    else:
        return 0.0  # No score

# Updated function to calculate location score
def calculate_location_score(location, candidate_profile):
    preferred_locations = candidate_profile.get('preferred_locations', '')
    if isinstance(preferred_locations, str):
        preferred_locations = [preferred_locations]
    else:
        preferred_locations = list(preferred_locations)
    if location.lower() in [loc.lower() for loc in preferred_locations]:
        return 1.0  # Full score
    else:
        return 0.0  # No score

# Updated function to calculate type of work score
def calculate_type_of_work_score(type_of_work, candidate_profile):
    preferred_types = candidate_profile.get('preferred_type_of_work', '')
    if isinstance(preferred_types, str):
        preferred_types = [preferred_types]
    else:
        preferred_types = list(preferred_types)
    if type_of_work.lower() in [typ.lower() for typ in preferred_types]:
        return 1.0  # Full score
    else:
        return 0.0  # No score

# Updated function to calculate work preference score
def calculate_work_preference_score(work_preference, candidate_profile):
    preferred_preferences = candidate_profile.get('preferred_work_preferences', '')
    if isinstance(preferred_preferences, str):
        preferred_preferences = [preferred_preferences]
    else:
        preferred_preferences = list(preferred_preferences)
    if work_preference == 'Not Specified':
        return 0.0  # No score if not specified
    elif work_preference.lower() in [pref.lower() for pref in preferred_preferences]:
        return 1.0  # Full score
    else:
        return 0.5  # Partial score for acceptable but not preferred options

# Function to calculate experience score
def calculate_experience_score(experience_required, candidate_experience):
    if experience_required is None:
        return 0.5  # Partial score if experience is not specified
    elif candidate_experience >= experience_required:
        return 1.0  # Full score if candidate has equal or more experience
    elif candidate_experience + 1 >= experience_required:
        return 0.75  # Near match
    else:
        return 0.0  # No score if underqualified

# Function to calculate degree score based on degree field
def calculate_degree_score(degree_fields_required, candidate_degree_field, description):
    # Check if the candidate's degree field matches the required degree fields
    candidate_field = candidate_degree_field.lower()
    required_fields = [field.lower() for field in degree_fields_required]
    in_required_fields = candidate_field in required_fields

    # Check if the candidate's degree field is mentioned anywhere in the description
    in_description = is_degree_field_in_description(description, candidate_degree_field)

    # Scoring logic
    if in_required_fields:
        return 1.0  # Full score if candidate's degree field is explicitly required
    elif in_description:
        return 0.75  # Partial score if candidate's degree field is mentioned elsewhere
    elif not degree_fields_required:
        return 0.5  # Partial score if degree field not specified
    else:
        return 0.0  # No score if candidate's degree field is not relevant

# Function to calculate the total score
def calculate_total_score(job_data, candidate_profile):
    # Weights for each parameter
    weights = {
        'job_title': 0.20,
        'location': 0.20,
        'type_of_work': 0.15,
        'work_preference': 0.15,
        'experience': 0.15,
        'degree': 0.15
    }

    # Extract parameters from job data
    job_title = job_data.get('job_title', '')
    location = job_data.get('location', '')
    type_of_work = job_data.get('type_of_work', '')
    description = str(job_data.get('description', '')).lower()
    
    # Extract parameters from description
    work_preference = extract_work_preference(description)
    experience_required = extract_experience(description)
    degree_fields_required = extract_degree_fields(description)

    # Candidate's qualifications
    candidate_experience = candidate_profile.get('experience', 0)
    candidate_degree_field = candidate_profile.get('degree_field', '')

    # Calculate individual scores
    job_title_score = calculate_job_title_score(job_title, candidate_profile)
    location_score = calculate_location_score(location, candidate_profile)
    type_of_work_score = calculate_type_of_work_score(type_of_work, candidate_profile)
    work_preference_score = calculate_work_preference_score(work_preference, candidate_profile)
    experience_score = calculate_experience_score(experience_required, candidate_experience)
    degree_score = calculate_degree_score(degree_fields_required, candidate_degree_field, description)

    # Calculate total weighted score
    total_score = 0
    total_score += job_title_score * weights['job_title']
    total_score += location_score * weights['location']
    total_score += type_of_work_score * weights['type_of_work']
    total_score += work_preference_score * weights['work_preference']
    total_score += experience_score * weights['experience']
    total_score += degree_score * weights['degree']

    return total_score

# Example usage
if __name__ == "__main__":
    # Example job data
    job_data = {
        'job_title': 'Software Engineer',
        'location': 'New York',
        'type_of_work': 'Full-time',
        'description': '''
            We are looking for a Software Engineer with at least 3 years of experience.
            This is a hybrid position requiring both in-office and remote work.
            Candidates with a degree in Computer Science, Engineering, or a related field are preferred.
            Knowledge in Computer Science principles is essential.
        '''
    }

    # Example candidate profile with strings instead of lists
    candidate_profile = {
        'preferred_job_titles': 'Software Engineer',
        'preferred_locations': 'New York',
        'preferred_type_of_work': 'Full-time',
        'preferred_work_preferences': 'Remote',
        'experience': 4,
        'degree_field': 'Computer Science'
    }

    # Calculate total score
    score = calculate_total_score(job_data, candidate_profile)
    print(f"Total Score: {score:.2f}")
