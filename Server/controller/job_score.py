import re



def extract_degree_fields(description):
    
    pattern = r"(?:bachelor's|master's|phd|doctorate)?\s*(?:degree)?\s*(?:in|of)\s+([\w\s&\-,]+)"
    matches = re.findall(pattern, description.lower())
    if matches:
       
        fields = []
        for match in matches:
          
            subfields = re.split(r',|\bor\b', match)
            for field in subfields:
                field = field.strip().strip('.').strip(',')
                if field:
                    fields.append(field)
        return fields
    else:
        return []  

def calculate_total_score(candidate_profile, job_data):

    weights = {
        'job_title': 0.25,
        'location': 0.25,
        'type_of_work': 0.10,
        'work_preference': 0.10,
        'experience': 0.15,
        'degree': 0.15
    }
    
    location = job_data.get('location', '')
    job_type = job_data.get('job_type', '')
    description = str(job_data.get('description', '')).lower()
    job_preference = job_data.get('job_preference', '')
    experience_required = job_data.get('experience', None)
    degree_fields_required = extract_degree_fields(description)
    
    
    location_score = calculate_location_score(location, candidate_profile.get("location"))
    type_of_work_score = calculate_type_of_work_score(job_type, candidate_profile.get("job_type"))
    work_preference_score = calculate_work_preference_score(job_preference, candidate_profile.get("job_preference"))
    experience_score = calculate_experience_score(experience_required, candidate_profile.get("experience"))
    degree_score = calculate_degree_score(degree_fields_required, candidate_profile.get("degree_field"))
    
    total_score = 0
    total_score += weights['job_title']
    total_score += location_score * weights['location']
    total_score += type_of_work_score * weights['type_of_work']
    total_score += work_preference_score * weights['work_preference']
    total_score += experience_score * weights['experience']
    total_score += degree_score * weights['degree']

    return int(total_score * 100)



def calculate_location_score(job_location, candidate_location):
    
    job_location = job_location.lower()
    candidate_location = candidate_location.lower()
    
    if candidate_location in job_location or job_location in candidate_location:
        return 1.0
    else:
        return 0.8  

def calculate_type_of_work_score(job_type : str, candidate_job_type : str):
    job_type = job_type.lower().replace('- ',' ')
    candidate_job_type = candidate_job_type.lower().replace('-',' ')
    if job_type == candidate_job_type:
        return 1.0
    else:
        return 0.0

def calculate_work_preference_score(job_preference, candidate_job_preference):
    job_preference = job_preference.lower()
    candidate_job_preference = candidate_job_preference.lower()
    if job_preference == candidate_job_preference:
        return 1.0
    else:
        return 0.0

def calculate_experience_score(experience_required, candidate_experience):
    candidate_experience = int(candidate_experience)
    
    if experience_required is None:
        return 1.0  
    elif candidate_experience >= experience_required:
        return 1.0
    else:
        return candidate_experience / experience_required

def calculate_degree_score(degree_fields_required, candidate_degree_field):
    candidate_degree_field = candidate_degree_field.lower()
    degree_fields_required = [field.lower() for field in degree_fields_required]
    if not degree_fields_required:
        return 1.0  
    elif candidate_degree_field in degree_fields_required:
        return 1.0
    else:
        
        candidate_words = set(candidate_degree_field.split())
        scores = []
        for field in degree_fields_required:
            field_words = set(field.split())
            common_words = candidate_words.intersection(field_words)
            score = len(common_words) / len(field_words)
            scores.append(score)
        max_score = max(scores) if scores else 0
        return max_score if max_score > 0.5 else 0.5
    
    
def main():
    candidate_profile = {
        'job': 'Software Engineer',
        'location': 'New York',
        'job_type': 'Full-time',
        'job_preference': 'Remote',
        'experience': '4',
        'degree_field': 'Computer Science'
    }

    job_data = {
        'title': "Staff Full Stack Engineer",
        'job_type': "Full time",
        'location': "Brooklyn, NY, US",
        'url': "https://www.indeed.com/applystart?jk=8e448e208480d912&from=vj&pos=bott…",
        'description': "Our Company  Changing the world through digital experiences is what Adobe's all about. ...",
        'organization': "Adobe",
        'job_preference': "onsite",
        'experience': 4,
    }

    total_score = calculate_total_score(candidate_profile, job_data)
    print(f"Total Score: {total_score:.2f}")


if __name__ == "__main__":
    main()