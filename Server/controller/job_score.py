import re

def extract_experience(description):
    matches = re.findall(r'(\d+)\+?\s+years? of experience', description)
    if matches:
        return int(matches[0])
    else:
        return None  

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
        'job_title': 0.20,
        'location': 0.20,
        'type_of_work': 0.15,
        'work_preference': 0.15,
        'experience': 0.15,
        'degree': 0.15
    }
    
    
    job_title = job_data.get('title', '')
    location = job_data.get('location', '')
    job_type = job_data.get('job_type', '')
    description = str(job_data.get('description', '')).lower()
    job_preference = job_data.get('job_preference', '')
    experience_required = extract_experience(description)
    degree_fields_required = extract_degree_fields(description)
    
    
    job_title_score = calculate_job_title_score(job_title, candidate_profile.get("job"))
    location_score = calculate_location_score(location, candidate_profile.get("location"))
    type_of_work_score = calculate_type_of_work_score(job_type, candidate_profile.get("job_type"))
    work_preference_score = calculate_work_preference_score(job_preference, candidate_profile.get("job_preference"))
    experience_score = calculate_experience_score(experience_required, candidate_profile.get("experience"))
    degree_score = calculate_degree_score(degree_fields_required, candidate_profile.get("degree_field"))
    
    
    total_score = 0
    total_score += job_title_score * weights['job_title']
    total_score += location_score * weights['location']
    total_score += type_of_work_score * weights['type_of_work']
    total_score += work_preference_score * weights['work_preference']
    total_score += experience_score * weights['experience']
    total_score += degree_score * weights['degree']

    return int(total_score * 100)

def calculate_job_title_score(job_title, candidate_job_title):
   
    job_title = job_title.lower()
    candidate_job_title = candidate_job_title.lower()
    
    
    job_title_words = set(job_title.split())
    candidate_job_title_words = set(candidate_job_title.split())
    

    common_words = job_title_words.intersection(candidate_job_title_words)
    
    
    if not job_title_words:
        return 0
    else:
        score = len(common_words) / len(job_title_words)
        return score 

def calculate_location_score(job_location, candidate_location):
    
    job_location = job_location.lower()
    candidate_location = candidate_location.lower()
    
    if candidate_location in job_location or job_location in candidate_location:
        return 1.0
    else:
        return 0.0  

def calculate_type_of_work_score(job_type, candidate_job_type):
    job_type = job_type.lower()
    candidate_job_type = candidate_job_type.lower()
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
        return max_score

# candidate_profile = {
#     'job': 'Software Engineer',
#     'location': 'New York',
#     'job_type': 'Full-time',
#     'job_preference': 'Remote',
#     'experience': '4',
#     'degree_field': 'Computer Science'
# }

# job_data = {
#     'title': "Staff Full Stack Engineer",
#     'job_type': "Full-time",
#     'location': "San Jose, CA 95110",
#     'url': "https://www.indeed.com/applystart?jk=8e448e208480d912&from=vj&pos=bott…",
#     'description': "Our Company  Changing the world through digital experiences is what Adobe's all about. We give everyone—from emerging artists to global brands—everything they need to design and deliver exceptional digital experiences! We're passionate about empowering people to create beautiful and powerful images, videos, and apps, and transforming how companies interact with customers across every screen.  We're on a mission to hire the very best and are committed to creating exceptional employee experiences where everyone is respected and has access to equal opportunity. We realize that new ideas can come from everywhere in the organization, and we know the next big idea could be yours!  The Opportunity  Adobe is seeking a Staff Full Stack Engineer to help build the next generation of marketing cloud products. Working with data scientists, architects, product managers, and other engineers, you will have an immediate impact on our platform and help the company in its journey to become an Experience Business.  What you’ll Do  Build highly scalable, highly available, performant web applications Work on full stack development (JS frameworks, Java) Build Restful API's in Java or Node.js Work with data store technologies (NoSQL, RDBMS) Write unit tests, integration tests, and functional tests Automate deployment, monitoring, and other production tasks Participate in Agile development methodologies and practices What you need to succeed  Bachelor’s or Master’s degree in Computer Science, Engineering, or a related field 7+ years of experience building web applications Strong JavaScript and Node.js development skills Experience with modern JS frameworks (e.g., React, Angular, Vue.js) Solid understanding of web technologies, including HTTP, HTML, CSS, and RESTful APIs Experience with Java and Spring Boot Knowledge of database systems (NoSQL and RDBMS) Experience with containerization technologies (Docker, Kubernetes) Strong problem-solving skills and attention to detail Excellent communication and collaboration skills",
#     'organization': "Adobe",
#     'job_preference': "Onsite",
# }


# total_score = calculate_total_score(candidate_profile, job_data)
# print(f"Total Score: {total_score:.2f}")
