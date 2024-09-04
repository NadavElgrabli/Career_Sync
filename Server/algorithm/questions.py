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




# import spacy
# from spacy import displacy

# test_answers = [
#     "I'm passionate about data analysis and want to become a Data Engineer.",
#     "I love creating interactive user interfaces and aspire to work as a Frontend Developer.",
#     "I have a knack for designing mechanical systems and am looking for a position as a Mechanical Engineer.",
#     "I have a keen eye for aesthetics and want to shape products as a Product Designer.",
#     "I excel in building brand identity and am seeking a position as a Brand Manager.",
#     "I have a passion for user experience and want to specialize as a UX/UI Designer.",
#     "I thrive in identifying growth opportunities and am looking for a role as a Business Development Specialist.",
#     "I enjoy uncovering market insights and am interested in pursuing a role in Market Research.",
#     "I have a strong financial acumen and am aiming to be a Financial Planner.",
#     "I have a passion for healthcare management and am seeking a position as a Health Services Administrator.",
#     "I'm skilled in crafting compelling narratives and want to work as a Copywriter.",
#     "I'm committed to cybersecurity and am looking for a role as a Network Security Engineer.",
#     "I'm enthusiastic about full-stack development and want to become a Full Stack Developer.",
#     "I have a talent for building client relationships and am seeking a position as an Account Manager.",
#     "I'm passionate about sustainable energy and am interested in pursuing a role in Renewable Energy Engineering.",
#     "I'm fascinated by data analysis and am aiming for a position as a Data Scientist.",
#     "I excel in project management and am seeking a position as a Project Manager.",
#     "I'm creative in digital marketing strategies and want to be a Digital Marketing Specialist.",
#     "I have a knack for system optimization and am looking for a role as a Systems Engineer.",
#     "I thrive in customer success roles and am interested in becoming a Customer Success Manager.",
#     "I have a passion for optimizing supply chains and am aiming for a position as a Supply Chain Analyst.",
#     "I excel in providing executive support and am seeking a position as an Executive Assistant.",
#     "I'm skilled in mobile app development and want to work as a Mobile App Developer.",
#     "I have a keen interest in user behavior research and am looking for a role as a User Researcher.",
#     "I'm passionate about environmental health and safety and am interested in pursuing a role in that field.",
#     "I'm analytical and strategic and am aiming for a position as a Business Intelligence Analyst.",
#     "I excel in content marketing strategies and am seeking a position as a Content Marketing Manager.",
#     "I have expertise in cloud solutions and want to be a Cloud Solutions Architect.",
#     "I have strong analytical skills and am looking for a role as a Systems Analyst.",
#     "I have a passion for ensuring software quality and am interested in becoming a Software Engineer in Test.",
#     "I'm strategic in shaping brand identities and am aiming for a position as a Brand Strategist.",
#     "I excel in managing technical projects and am seeking a position as a Technical Project Manager.",
#     "I'm creative in mobile user experience design and want to work as a Mobile UX Designer.",
#     "I have a strong financial background and am looking for a role as a Financial Analyst.",
#     "I'm passionate about urban development and am interested in pursuing a role in Urban Planning.",
#     "I have a product-focused mindset and am aiming for a position as a Product Owner.",
#     "I'm dedicated to enhancing customer experiences and am seeking a position as a Customer Experience Specialist.",
#     "I have an eye for detail and am looking for a role as a Data Quality Analyst.",
#     "I'm experienced in software architecture and want to become a Software Architect.",
#     "I'm passionate about digital product management and am aiming for a position as a Digital Product Manager.",
#     "I excel in analyzing business processes and am seeking a position as a Business Process Analyst.",
#     "I have a passion for sustainable agriculture and am interested in pursuing a role in that field.",
#     "I have a strong financial background and am aiming for a position as a Financial Controller.",
#     "I excel in representing brands and am seeking a position as a Brand Ambassador.",
#     "I have expertise in providing solutions and want to be a Solutions Consultant."
# ]

# nlp = spacy.load("en_core_web_lg")
# doc1 = nlp("I have a strong financial background and am aiming for a position as a Financial Controller.")
# displacy.serve(doc1, style="dep", host="127.0.0.1")

# def print_tokens(doc):
#     for token in doc:
#         print('TEXT:', token.text, " | ", 'POS:', token.pos_, " | ", 'DEP:', token.dep_, " | ", 'HEAD:', token.head)
#     return "No role found"

# def extract_job(doc):
#     for index, token in enumerate(doc):
#         if (token.pos_ == "PROPN" and token.dep_ == "compound") and \
#               (doc[index + 1].pos_ == "PROPN" and doc[index + 1].dep_ == "compound") and \
#               (doc[index + 2].pos_ == "PROPN" and (doc[index + 2].dep_ == "pobj" or doc[index + 2].dep_ == "attr")):
#             return print("possible job:", token.text, doc[index + 1].text, doc[index + 2].text)

#         elif (token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "compound" and \
#               (token.head.text == doc[index + 1].text or token.head.text == doc[index + 2].text) and \
#               ((doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and doc[index + 1].dep_ == "compound") and \
#               (doc[index + 1].head.text == doc[index + 2].text) and \
#               ((doc[index + 2].pos_ == "PROPN" or doc[index + 2].pos_ == "NOUN") and \
#                (doc[index + 2].dep_ == "ROOT" and doc[index + 2].head.text == doc[index + 2].text)):
#             return print("possible job:", token.text, doc[index + 1].text, doc[index + 2].text)

#         elif ((token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "compound") and \
#                 (token.head.text == doc[index + 1].text and (doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and \
#                  doc[index + 1].dep_ == "ROOT") and \
#                  (doc[index + 1].head.text == doc[index + 1].text):
#             return print("possible job:", token.text, doc[index + 1].text)

#         elif token.pos_ == "PROPN" and \
#               (token.dep_ == "compound" or token.dep_ == "pobj") and \
#               (token.head.text == doc[index + 1].text):
#             return print("possible job:", token.text, doc[index + 1].text)

#         elif token.pos_ == "PROPN" and (token.dep_ == "compound" or token.dep_ == "pobj"):
#             return print("possible job:", token.text)

#         elif token.pos_ == "NOUN" and token.dep_ == "attr":
#             return print("possible job:", token.text)

#     return print("No role found")

# def extract_location(doc):
#     num_tokens = len(doc)
#     for index, token in enumerate(doc):
#         if index + 4 < num_tokens and token.ent_type_ == "GPE" and \
#             (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and \
#             (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT") and \
#             (doc[index + 3].ent_type_ == "GPE" or doc[index + 3].pos_ == "PUNCT") and \
#             (doc[index + 4].ent_type_ == "GPE" or doc[index + 4].pos_ == "PUNCT"):
#             return print("possible location:", token.text, doc[index + 1].text, doc[index + 2].text, doc[index + 3].text, doc[index + 4].text)

#         elif index + 3 < num_tokens and token.ent_type_ == "GPE" and \
#               (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and \
#               (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT") and \
#               (doc[index + 3].ent_type_ == "GPE" or doc[index + 3].pos_ == "PUNCT"):
#             return print("possible location:", token.text, doc[index + 1].text, doc[index + 2].text, doc[index + 3].text)

#         elif index + 2 < num_tokens and token.ent_type_ == "GPE" and \
#               (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and \
#               (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT"):
#             return print("possible location:", token.text, doc[index + 1].text, doc[index + 2].text)

#         elif index + 1 < num_tokens and token.ent_type_ == "GPE" and doc[index + 1].ent_type_ == "GPE":
#             return print("possible location:", token.text, doc[index + 1].text)

#         elif token.ent_type_ == "GPE":
#             return print("possible location:", token.text)

#     return print("No location found")

# def extract_type_of_job(doc):
#     num_tokens = len(doc)
#     for index, token in enumerate(doc):
#         if index + 2 < num_tokens and (token.pos_ == "ADJ" or token.pos_ == "NOUN") and (token.dep_ == "amod" or token.dep_ == "compound") and \
#             (doc[index + 1].pos_ == "NOUN" or doc[index + 1].pos_ == "PUNCT") and \
#             (doc[index + 2].pos_ == "NOUN" and (doc[index + 2].dep_ == "ROOT" or doc[index + 2].dep_ == "npadvmod")):
#             return print("possible type of job:", token.text, doc[index + 1].text, doc[index + 2].text)

#         elif index + 1 < num_tokens and (token.pos_ == "NOUN" or token.pos_ == "ADJ") and token.dep_ == "amod" and \
#                 (doc[index + 1].pos_ == "NOUN" and (doc[index + 1].dep_ == "ROOT" or doc[index + 1].dep_ == "compound")):
#             return print("possible type of job:", token.text, doc[index + 1].text)

#         elif token.text == "full" or token.text == "part":
#             return print("possible type of job:", token.text, "time")

#     return print("I am sorry I don't understand. Please write 'full time' or 'part time'")

# def extract_work_preference(doc):
#     num_tokens = len(doc)
#     for index, token in enumerate(doc):
#         if index + 2 < num_tokens and token.pos_ == "ADP" and (token.dep_ == "ROOT" or token.dep_ == "nmod" or token.dep_ == "prep") and \
#             doc[index + 1].pos_ == "PUNCT" and \
#             doc[index + 2].pos_ == "NOUN" and (doc[index + 2].dep_ == "pobj" or doc[index + 2].dep_ == "compound"):
#             return print("possible work preference:", token.text, doc[index + 1].text, doc[index + 2].text)

#         elif index + 1 < num_tokens and token.pos_ == "ADP" and token.dep_ == "ROOT" and \
#             doc[index + 1].pos_ == "NOUN" and doc[index + 1].dep_ == "pobj":
#             return print("possible work preference:", token.text, doc[index + 1].text)

#         elif index + 1 < num_tokens and token.pos_ == "ADJ" and \
#             (token.dep_ == "amod" or token.dep_ == "compound"):
#             return print("possible work preference:", token.text)

#         elif index + 1 < num_tokens and token.pos_ == "NOUN" and token.dep_ == "amod":
#             return print("possible work preference:", token.text)

#         elif (token.pos_ == "NOUN" or token.pos_ == "ADJ") and token.dep_ == "ROOT":
#             return print("possible work preference:", token.text)

#     return print("I am sorry I don't understand. Please write 'on-site', 'remote' or 'hybrid'")

# def text_to_digits(text):
#     word_to_digit = {
#         "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
#         "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
#         "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
#         "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
#         "eighteen": "18", "nineteen": "19", "twenty": "20"
#     }
#     return word_to_digit.get(text.lower(), None)

# def extract_experience(doc):
#     for token in doc:
#         if token.like_num:
#             if token.text.isdigit():
#                 return print("possible years of experience:", token.text)
#             else:
#                 digit = text_to_digits(token.text)
#                 if digit:
#                     return print("possible years of experience:", digit)

#     return print("I am sorry I don't understand. Please write the number of years of experience you have.")

# for answer in test_answers:
#     doc = nlp(answer)
#     print_tokens(doc)
#     print("--------------------------------------------------------------------------")
#     extract_job(doc)
#     print("--------------------------------------------------------------------------")
