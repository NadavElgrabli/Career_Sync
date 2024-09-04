import spacy

class Chatbot:
    def __init__(self):
        self.user_data = {}
        # Load the spaCy model (you need to have en_core_web_sm installed)
        self.nlp = spacy.load('en_core_web_sm')

    def ask_question(self, message):
        """
        Process the user's message and return an appropriate response based on the content.
        """
        doc = self.nlp(message)  # Process the message using spaCy

        # Check for job-related information
        if self.contains_job(doc):
            job_title = self.extract_job(doc)
            if job_title != "No job title found":
                self.user_data['job'] = job_title
                return f"Great! I see you're interested in {job_title}. What is your preferred location?"
            else:
                return "I couldn't identify the job title. Could you try rephrasing it?"

        # Check for location-related information
        elif self.contains_location(doc):
            location = self.extract_location(doc)
            self.user_data['location'] = location
            return f"Got it! You're interested in {location}. Are you looking for full-time or part-time work?"

        # Check for job type (full-time/part-time)
        elif self.contains_full_time_or_part_time(doc):
            job_type = self.extract_full_time(doc)
            self.user_data['full_time'] = job_type
            return "Would you prefer hybrid, on-site, or remote work?"

        # Check for work preference (hybrid/on-site/remote)
        elif self.contains_work_preference(doc):
            work_preference = self.extract_work_preference(doc)
            self.user_data['work_preference'] = work_preference
            return "How many years of experience do you have?"

        # Check for experience information (years of experience)
        elif self.contains_experience(doc):
            experience = self.extract_experience(doc)
            self.user_data['experience'] = experience
            return "Thanks for sharing your details. Let's move forward with the next steps."

        # If none of the above cases match, return a default response
        else:
            return "I didn't quite understand that. Could you provide more details?"

    # Helper methods to check if the message contains specific information

    def contains_job(self, doc):
        """Check if the message contains job-related entities."""
        for ent in doc.ents:
            if ent.label_ == 'WORK_OF_ART' or ent.label_ == 'ORG':  # Adjust based on your model
                return True
        return False

    def contains_location(self, doc):
        """Check if the message contains location-related entities."""
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # Geopolitical entity (like a country, city, etc.)
                return True
        return False

    def contains_full_time_or_part_time(self, doc):
        """Check if the message mentions full-time or part-time job preferences."""
        if "full" in doc.text.lower() or "part" in doc.text.lower():
            return True
        return False

    def contains_work_preference(self, doc):
        """Check if the message mentions work preference like hybrid, on-site, or remote."""
        if "remote" in doc.text.lower() or "on-site" in doc.text.lower() or "hybrid" in doc.text.lower():
            return True
        return False

    def contains_experience(self, doc):
        """Check if the message contains years of experience information."""
        for token in doc:
            if token.like_num:  # Checks if the token is a numeric-like value
                return True
        return False

    # Helper methods to extract specific information from the message

    def extract_job(self, doc):
        """Extract job titles from the text."""
        for ent in doc.ents:
            if ent.label_ == 'WORK_OF_ART' or ent.label_ == 'ORG':  # Adjust based on your model
                return ent.text
        return "No job title found"

    def extract_location(self, doc):
        """Extract location-related information from the text."""
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # Geopolitical entities (like countries, cities, states)
                return ent.text
        return "Unknown location"

    def extract_full_time(self, doc):
        """Extract whether the user is looking for full-time or part-time work."""
        if "full" in doc.text.lower():
            return "Full-time"
        elif "part" in doc.text.lower():
            return "Part-time"
        return "Unknown employment type"

    def extract_work_preference(self, doc):
        """Extract work preference (remote, on-site, hybrid) from the message."""
        if "remote" in doc.text.lower():
            return "Remote"
        elif "on-site" in doc.text.lower() or "on site" in doc.text.lower():
            return "On-site"
        elif "hybrid" in doc.text.lower():
            return "Hybrid"
        return "Unknown preference"

    def extract_experience(self, doc):
        """Extract years of experience from the user's message."""
        for token in doc:
            if token.like_num:
                return f"{token.text} years"
        return "Unknown experience"

    def get_user_data(self):
        """Return the collected user data."""
        return self.user_data
