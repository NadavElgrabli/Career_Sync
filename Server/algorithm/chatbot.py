import spacy

class Chatbot:
    def __init__(self):
        self.user_data = {}
        self.nlp = spacy.load('en_core_web_sm')  # Load the spaCy model

    def ask_question(self, message):
        # Process the user's message and return a response
        doc = self.nlp(message)
        if self.contains_job(doc):
            job_title = self.extract_job(doc)
            if job_title != "No job title found":
                self.user_data['job'] = job_title
                return f"Great! I see you're interested in {job_title}. What is your preferred location?"
            else:
                return "I couldn't identify the job title. Could you try rephrasing it?"

        elif self.contains_location(doc):
            location = self.extract_location(doc)
            self.user_data['location'] = location
            return f"Got it! You're interested in {location}. Are you looking for full-time or part-time work?"

        elif self.contains_full_time_or_part_time(doc):
            job_type = self.extract_full_time(doc)
            self.user_data['full_time'] = job_type
            return "Would you prefer hybrid, on-site, or remote work?"

        elif self.contains_work_preference(doc):
            work_preference = self.extract_work_preference(doc)
            self.user_data['work_preference'] = work_preference
            return "How many years of experience do you have?"

        elif self.contains_experience(doc):
            experience = self.extract_experience(doc)
            self.user_data['experience'] = experience
            return "Thanks for sharing your details. Let's move forward with the next steps."

        else:
            return "I didn't quite understand that. Could you provide more details?"

    def contains_job(self, doc):
        for ent in doc.ents:
            if ent.label_ == 'WORK_OF_ART' or ent.label_ == 'ORG':
                return True
        return False

    def contains_location(self, doc):
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                return True
        return False

    def contains_full_time_or_part_time(self, doc):
        if "full" in doc.text.lower() or "part" in doc.text.lower():
            return True
        return False

    def contains_work_preference(self, doc):
        if "remote" in doc.text.lower() or "on-site" in doc.text.lower() or "hybrid" in doc.text.lower():
            return True
        return False

    def contains_experience(self, doc):
        for token in doc:
            if token.like_num:
                return True
        return False

    def extract_job(self, doc):
        for ent in doc.ents:
            if ent.label_ == 'WORK_OF_ART' or ent.label_ == 'ORG':
                return ent.text
        return "No job title found"

    def extract_location(self, doc):
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                return ent.text
        return "Unknown location"

    def extract_full_time(self, doc):
        if "full" in doc.text.lower():
            return "Full-time"
        elif "part" in doc.text.lower():
            return "Part-time"
        return "Unknown employment type"

    def extract_work_preference(self, doc):
        if "remote" in doc.text.lower():
            return "Remote"
        elif "on-site" in doc.text.lower() or "on site" in doc.text.lower():
            return "On-site"
        elif "hybrid" in doc.text.lower():
            return "Hybrid"
        return "Unknown preference"

    def extract_experience(self, doc):
        for token in doc:
            if token.like_num:
                return f"{token.text} years"
        return "Unknown experience"