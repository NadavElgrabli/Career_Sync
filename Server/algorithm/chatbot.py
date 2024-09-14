import spacy

class Chatbot:
    def __init__(self):
        self.user_data = {}
        self.nlp = spacy.load('en_core_web_sm')

    def ask_question(self, message):
        doc = self.nlp(message)
        
        if 'job' not in self.user_data:
            job_title = self.extract_job(doc)
            if job_title != "No job title found":
                self.user_data['job'] = job_title
                return f"Great! I see you're interested in {job_title}. What is your preferred location?"
            else:
                return "I couldn't identify the job title. Could you try rephrasing it?"

        elif 'location' not in self.user_data:
            location = self.extract_location(doc)
            if location != "No location found":
                self.user_data['location'] = location
                return f"Got it! You're interested in {location}. Are you looking for full-time or part-time work?"
            else:
                return "I couldn't identify the location. Please try again."

        elif 'type_of_job' not in self.user_data:
            job_type = self.extract_type_of_job(doc)
            if job_type != "No job type found":
                self.user_data['type_of_job'] = job_type
                return "Would you prefer hybrid, on-site, or remote work?"
            else:
                return "I couldn't identify if you want full-time or part-time work. Could you specify?"

        elif 'work_preference' not in self.user_data:
            work_preference = self.extract_work_preference(doc)
            if work_preference != "No work preference found":
                self.user_data['work_preference'] = work_preference
                return "How many years of experience do you have?"
            else:
                return "I couldn't identify your work preference. Please specify if you want hybrid, on-site, or remote work."

        elif 'experience' not in self.user_data:
            experience = self.extract_experience(doc)
            if experience != "No experience found":
                self.user_data['experience'] = experience
                return "Thanks for sharing your details. Do you have a degree?"
            else:
                return "I couldn't understand the number of years of experience. Please provide a valid number."
    
        elif 'degree' not in self.user_data:
            has_degree = self.extract_if_has_degree(doc)
            if has_degree != "No degree found":
                self.user_data['degree'] = has_degree
                if self.user_data['degree'] == "User has a degree":
                    return "Could you please specify your field of study?"
                else:
                    return "Thank you! Let's move forward with the next step."
            else:
                return "I couldn't determine if you have a degree. Could you please provide a clear answer?"

        elif self.user_data['degree'] == "User has a degree":
            if 'degree_field' not in self.user_data:
                degree_field = self.extract_degree_field(doc)
                if degree_field != "No degree field found":
                    self.user_data['degree_field'] = degree_field
                    return "Thank you! Let's move forward with the next step."
                else:
                    return "I couldn't identify your field of study. Could you please provide a specific field?"
            
        return f"{self.user_data}" #TODO: Delete - For Debug


    def extract_job(self, doc):
        for index, token in enumerate(doc):
            #answers with full sentence where the job title consists of 3 words
            if (token.pos_ == "PROPN" and token.dep_ == "compound") and\
                (doc[index + 1].pos_ == "PROPN" and doc[index + 1].dep_ == "compound") and\
                    (doc[index + 2].pos_ == "PROPN" and (doc[index + 2].dep_ == "pobj" or doc[index + 2].dep_ == "attr")):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text
            # answers with just job title that consists of 3 words
            elif (token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "compound" and\
                (token.head.text == doc[index + 1].text or token.head.text == doc[index + 2].text) and\
                    ((doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and doc[index + 1].dep_ == "compound") and\
                        (doc[index + 1].head.text == doc[index + 2].text) and\
                            ((doc[index + 2].pos_ == "PROPN" or doc[index + 2].pos_ == "NOUN") and\
                                (doc[index + 2].dep_ == "ROOT" and doc[index + 2].head.text == doc[index + 2].text)):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text
            # answers with just job title thats consists of 2 words
            elif ((token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "compound") and\
                    (token.head.text == doc[index + 1].text and (doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and\
                    doc[index + 1].dep_ == "ROOT") and\
                        (doc[index + 1].head.text == doc[index + 1].text):
                return token.text + " " + doc[index + 1].text
            elif token.pos_ == "PROPN" and\
                (token.dep_ == "compound" or token.dep_ == "pobj") and\
                    (token.head.text ==doc[index +1].text):
                return token.text + " " + doc[index +1].text
            # One word job titles
            elif token.pos_ == "PROPN" and (token.dep_ == "compound" or token.dep_ == "pobj"):
                return token.text
            else:
                if token.pos_ == "NOUN" and token.dep_ == "attr": # and doc[index - 1].head == token:
                    return token.text
        return "No job title found"


    def extract_location(self, doc):
        num_tokens = len(doc)
        for index, token in enumerate(doc):
            # city, country country country
            if index + 4 < num_tokens and token.ent_type_ == "GPE" and\
                    (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and\
                        (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT") and\
                            (doc[index + 3].ent_type_ == "GPE" or doc[index + 3].pos_ == "PUNCT") and\
                                (doc[index + 4].ent_type_ == "GPE" or doc[index + 4].pos_ == "PUNCT"):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text + " " + doc[index + 3].text + " " + doc[index + 4].text
            elif index + 3 < num_tokens and token.ent_type_ == "GPE" and\
                (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and\
                    (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT") and\
                        (doc[index + 3].ent_type_ == "GPE" or doc[index + 3].pos_ == "PUNCT"):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text + " " + doc[index + 3].text
            elif index + 2 < num_tokens and token.ent_type_ == "GPE" and\
                (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and\
                    (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT"):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text
            # country country
            elif index + 1 < num_tokens and token.ent_type_ == "GPE" and doc[index + 1].ent_type_ == "GPE":
                return token.text + " " + doc[index + 1].text
            #One word (country or city)
            elif token.ent_type_ == "GPE":
                return token.text
        return "No location found"
    

    # type of job is either full-time or part-time
    def extract_type_of_job(self, doc):
        num_tokens = len(doc)
        for index, token in enumerate(doc):
            # answer is in form: "full - time" or "part - time"
            if index + 2 < num_tokens and (token.pos_ == "ADJ" or token.pos_ == "NOUN") and (token.dep_ == "amod" or token.dep_ == "compound") and\
                    (doc[index + 1].pos_ == "NOUN" or doc[index + 1].pos_ == "PUNCT") and\
                        (doc[index + 2].pos_ == "NOUN" and (doc[index + 2].dep_ == "ROOT" or doc[index + 2].dep_ == "npadvmod")):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text
            #answer consist of :"full time" or "part time"
            elif index + 1 < num_tokens and (token.pos_ == "NOUN" or token.pos_ == "ADJ") and token.dep_ == "amod" and\
                    (doc[index+1].pos_ == "NOUN" and (doc[index+1].dep_ == "ROOT" or doc[index+1].dep_ == "compound")):
                return token.text + " " + doc[index+1].text
            #answer is just: "full" or "part"
            elif token.text == "full" or token.text == "part":
                return token.text + "time"
        return "No job type found"


    #on site, remote or hybrid work preference
    def extract_work_preference(self, doc):
        num_tokens = len(doc)
        for index, token in enumerate(doc):
            # answer consists of: "on - site"
            if (index + 2 < num_tokens and token.pos_ == "ADP" and (token.dep_ == "ROOT" or token.dep_ == "nmod" or token.dep_ =="prep") and
                doc[index + 1].pos_ == "PUNCT" and
                    doc[index + 2].pos_ == "NOUN" and (doc[index + 2].dep_ == "pobj" or doc[index+2].dep_ =="compound")):
                return token.text + " " + doc[index+1].text + " " + doc[index + 2].text
            # answer consists of: "on site"
            elif (index + 1 < num_tokens and token.pos_ == "ADP" and token.dep_ == "ROOT" and
                doc[index + 1].pos_ == "NOUN" and doc[index + 1].dep_ == "pobj"):
                return token.text + " " + doc[index+1].text
            # answer consists of: "remote" or "hybrid"
            elif (index + 1 < num_tokens and token.pos_ == "ADJ" and
                    (token.dep_ == "amod" or token.dep_ == "compound")):
                return token.text
            # answer consists of "hybrid" i think
            elif (index + 1 < num_tokens and token.pos_ == "NOUN" and token.dep_ == "amod"):
                return token.text
            # answer is just: "hybrid" or "remote"
            elif (token.pos_ == "NOUN" or token.pos_ == "ADJ") and (token.dep_ == "ROOT" or token.dep_ == "nsubj"):
                return token.text
        return "No work preference found"


    def text_to_digits(self, text):
        # Define a mapping of textual representations of numbers to their digit counterparts
        word_to_digit = {
            "zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
            "ten": "10",
            "eleven": "11",
            "twelve": "12",
            "thirteen": "13",
            "fourteen": "14",
            "fifteen": "15",
            "sixteen": "16",
            "seventeen": "17",
            "eighteen": "18",
            "nineteen": "19",
            "twenty": "20"
            # Add more mappings as needed
        }
        # Check if the text is in the mapping, if yes, return the digit representation
        if text.lower() in word_to_digit:
            return word_to_digit[text.lower()]
        else:
            return None  # Return None if the text is not a known number word


    # Extract years of experience from the user's response
    def extract_experience(self, doc):
        for token in doc:
            if token.like_num == True:
                if token.text.isdigit():
                    return token.text
                else:
                    # Attempt to convert the textual representation to digits
                    digit = self.text_to_digits(token.text)
                    if digit is not None:
                        return digit
        return "No experience found"


    # user will answer yes or no to the question if they have a degree (caps dont matter)
    def extract_if_has_degree(self, doc):
        for token in doc:
            if token.text.lower() == "yes":
                return "User has a degree"
            elif token.text.lower() == "no":
                return "User does not have a degree"
        return "No degree found"


    # extract the name of the degree (computer science, mechanical engineering, etc.)
    def extract_degree_field(self, doc):
        for index, token in enumerate(doc):
            #answers where the degree title consists of 3 words
            if (((token.pos_ == "ADJ" or token.pos_ == "NOUN" or token.pos_ == "PROPN") and (token.dep_ == "amod" or token.dep_ =="compound")) and\
                ((doc[index + 1].pos_ == "ADJ" or doc[index + 1].pos_ == "NOUN" or doc[index + 1].pos_ == "PROPN") and (doc[index + 1].dep_ == "compound" or doc[index + 1].dep_ == "amod")) and\
                    ((doc[index + 2].pos_ == "NOUN" or doc[index + 2].pos_ == "PROPN") and (doc[index + 2].dep_ == "pobj" or doc[index + 2].dep_ == "ROOT"))):
                return token.text + " " + doc[index + 1].text + " " + doc[index + 2].text
            # answers with just degree title that consists of 2 words
            elif (((token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ =="ADJ") and (token.dep_ == "compound" or token.dep_ == "amod")) and\
                    ((doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and (doc[index + 1].dep_ == "compound" or doc[index + 1].dep_ == "pobj" or doc[index + 1].dep_ == "ROOT"))):
                return token.text + " " + doc[index + 1].text
            # answers with just degree title that consists of 1 word
            elif ((token.pos_ == "PROPN" or token.pos_ == "NOUN") and (token.dep_ == "pobj" or token.dep_ == "ROOT") and\
                (token.text != "degree")):
                return token.text
        return "No degree filed found"
    