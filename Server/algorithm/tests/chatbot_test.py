import spacy
from spacy import displacy
import random
nlp = spacy.load("en_core_web_lg")
errors = 0

# doc1 = nlp("I have a strong financial background and am aiming for a position as a Financial Controller.")
# displacy.serve(doc1, style="dep",host="127.0.0.1")
# doc2 = nlp("I'm experienced in software architecture and want to become a Software Architect.")
# displacy.serve(doc2, style="dep",host="127.0.0.1")


def print_tokens(doc):
    for token in doc:
        print('TEXT:', token.text," | ", 'POS:', token.pos_," | ", 'DEP:', token.dep_, " | ", 'HEAD:', token.head)
        #print('TEXT:', token.text," | ", 'POS:', token.pos_," | ", 'DEP:', token.dep_, " | ", 'HEAD:', token.head, 'ENT_TYPE:', token.ent_type_)
        #print('TEXT:', token.text," | ", 'POS:', token.pos_," | ", 'DEP:', token.dep_, " | ", 'HEAD:', token.head, 'like_num:', token.like_num)

    return "No role found"


test_answers = [
    "I am looking for a job as a software developer",
    "Software Development Engineer",
    "User Experience Designer",
    "Project Coordinator",
    "Graphic Design Specialist",
    "Customer Relationship Manager",
    "Human Resources Manager",
    "I am looking for a job as a software developer",
    "Graphic Designer",
    "Police Officer",
    "Firefighter",
    "Dental Hygienist",
    "Photographer",
    "I'm passionate about data analysis and want to become a Data Engineer.",
    "I love creating interactive user interfaces and aspire to work as a Frontend Developer.",
    "I have a knack for designing mechanical systems and am looking for a position as a Mechanical Engineer.",
    "I have a keen eye for aesthetics and want to shape products as a Product Designer.",
    "I excel in building brand identity and am seeking a position as a Brand Manager.",
    "Product Marketing Specialist",
    "Cybersecurity Specialist Analyst",
    "UX Research Assistant",
    "Business Development Representative",
    "Compliance Risk Analyst",
    "DevOps Engineer",
    "I have a passion for user experience and want to specialize as a UX/UI Designer.",
    "I thrive in identifying growth opportunities and am looking for a role as a Business Development Specialist.",
    "I enjoy uncovering market insights and am interested in pursuing a role in Market Research.",
    "I have a strong financial acumen and am aiming to be a Financial Planner.",
    "I have a passion for healthcare management and am seeking a position as a Health Services Administrator.",
    "I'm skilled in crafting compelling narratives and want to work as a Copywriter.",
    "I'm passionate about digital product management and am aiming for a position as a Digital Product Manager.",
    "I excel in analyzing business processes and am seeking a position as a Business Process Analyst.",
    "I have a strong financial background and am aiming for a position as a Financial Controller.",
    "I excel in representing brands and am seeking a position as a Brand Ambassador.",
    "I have expertise in providing solutions and want to be a Solutions Consultant.",
    "I'm interested in becoming a Data Engineer.",
    "I want to work as a Frontend Developer.",
    "I am looking for a position as a Mechanical Engineer.",
    "I'm aiming for a role as a Product Designer.",
    "I'm seeking a position as a Brand Manager.",
    "I want to be a UX/UI Designer.",
    "I am looking for a role as a Business Development Specialist.",
    "I'm interested in pursuing a role in Market Research.",
    "I'm aiming to be a Financial Planner.",
    "I'm seeking a position as a Health Services Administrator.",
    "I want to work as a Copywriter.",
    "I'm seeking a position as a Brand Ambassador.",
    "I want to be a Solutions Consultant."
]


# test_answers = [
#     "I am seeking a position as a Project Management Specialist.",
#     "I excel in analyzing data trends and am looking for a Data Science Analyst.",
#     "I thrive in researching user experiences and am seeking a User Experience Researcher.",
#     "I'm looking for a Digital Marketing Strategist.",
#     "I focus on developing new business and am seeking a Business Development Manager.",
#     "I am interested in the Software Quality Engineer role.",
#     "I excel in assisting customers and am seeking a Customer Service Representative.",
#     "I thrive in planning finances and am looking for a Financial Planning Analyst.",
#     "I'm seeking a position as an Operations Support Coordinator.",
#     "I aim to innovate products as a Product Marketing Manager.",
#     "I am looking for a Human Resources Coordinator.",
#     "I am interested in a Sales Account Executive position.",
#     "I excel in providing technical support and am seeking a Technical Support Engineer.",
#     "I am looking for a Content Marketing Manager.",
#     "Graphic Design Specialist",
#     "Supply Chain Analyst",
#     "Corporate Communications Specialist",
#     "Social Media Coordinator",
#     "Market Research Analyst",
#     "Instructional Design Consultant",
#     "Quality Assurance Tester",
#     "Event Planning Coordinator",
#     "Business Process Analyst",
#     "Network Security Administrator",
#     "Financial Compliance Officer",
#     "Health Services Manager",
#     "Logistics Operations Manager",
#     "User Interface Developer",
#     "Public Relations Manager",
#     "Training and Development Specialist",
#     "Real Estate Analyst",
#     "Data Visualization Expert",
#     "Legal Compliance Officer",
#     "Investment Banking Analyst",
#     "Cloud Solutions Architect",
#     "Risk Management Consultant",
#     "Digital Content Creator",
#     "Sales Development Representative",
#     "Information Technology Specialist",
#     "Product Development Engineer",
#     "Strategic Partnership Manager",
#     "Research and Development Scientist",
#     "Cybersecurity Operations Analyst",
#     "Brand Marketing Specialist",
#     "E-commerce Business Analyst",
#     "Environmental Health Specialist",
#     "Healthcare Project Coordinator",
#     "System Integration Engineer",
#     "Facilities Management Specialist",
#     "Financial Risk Analyst",
#     "Community Outreach Coordinator",
#     "I am seeking a position as a Software Engineer.",
#     "I thrive in data analysis and am looking for a Data Analyst.",
#     "I am interested in the Graphic Designer role.",
#     "I'm looking for a Marketing Manager.",
#     "I focus on improving user experiences as a User Researcher.",
#     "I excel in financial forecasting and am seeking a Financial Analyst.",
#     "I'm interested in a Product Owner position.",
#     "I am seeking a position as a Sales Representative.",
#     "I thrive in content creation as a Content Creator.",
#     "I aim to innovate technology as a DevOps Engineer.",
#     "UX Designer",
#     "Web Developer",
#     "Project Coordinator",
#     "Business Analyst",
#     "Health Manager",
#     "HR Specialist",
#     "Sales Consultant",
#     "Data Scientist",
#     "Technical Writer",
#     "Operations Manager",
#     "Quality Inspector",
#     "Social Strategist",
#     "Risk Manager",
#     "Account Executive",
#     "IT Consultant",
#     "Recruitment Coordinator",
#     "Brand Manager",
#     "Compliance Officer",
#     "Logistics Specialist",
#     "Training Manager",
#     "Event Planner",
#     "Network Engineer",
#     "Research Analyst",
#     "Business Consultant",
#     "Digital Specialist",
#     "Systems Analyst",
#     "Cyber Analyst",
#     "Finance Director",
#     "Customer Advocate",
#     "Support Specialist",
#     "Media Buyer",
#     "Product Analyst",
#     "Market Analyst",
#     "Sales Trainer",
#     "Operations Analyst",
#     "Technical Consultant",
#     "Facilities Manager",
#     "Field Engineer",
#     "Engineer",
#     "Manager",
#     "Analyst",
#     "Developer",
#     "Consultant",
#     "Director",
#     "Coordinator",
#     "Specialist",
#     "Associate",
#     "Administrator",
#     "Strategist",
#     "Designer",
#     "Technician",
#     "Salesperson",
#     "Representative",
#     "Scientist",
#     "Writer",
#     "Auditor",
#     "Trainer",
#     "Advocate",
#     "Inspector"
# ]

def extract_job(doc):
    for index, token in enumerate(doc):
        #answers with full sentence where the job title consists of 3 words
        if (token.pos_ == "PROPN" and token.dep_ == "compound") and\
              (doc[index + 1].pos_ == "PROPN" and doc[index + 1].dep_ == "compound") and\
                  ((doc[index + 2].pos_ == "PROPN" or doc[index + 2].pos_ == "NOUN") and (doc[index + 2].dep_ == "pobj" or doc[index + 2].dep_ == "attr" or doc[index + 2].dep_ == "dobj" or doc[index + 2].dep_ == "compound")):
            return print("possible job:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text)
        # answers with just job title that consists of 3 words
        elif (token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "compound" and\
              (token.head.text == doc[index + 1].text or token.head.text == doc[index + 2].text) and\
                  ((doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and doc[index + 1].dep_ == "compound") and\
                      (doc[index + 1].head.text == doc[index + 2].text) and\
                          ((doc[index + 2].pos_ == "PROPN" or doc[index + 2].pos_ == "NOUN") and\
                            (doc[index + 2].dep_ == "ROOT" and doc[index + 2].head.text == doc[index + 2].text)):
            return print("possible job:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text)
        # answers with full sentence where job title consists of 2 words
        elif ((token.pos_ == "PROPN" or token.pos_ == "NOUN") and (token.dep_ == "compound" or token.dep_ == "pobj")) and\
                  (index + 1 < len(doc) and token.head.text ==doc[index +1].text) and\
                    (doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and (doc[index + 1].dep_ == "attr" or doc[index + 1].dep_ == "pobj"):
            return print("possible job:" + token.text + " " + doc[index +1].text)
        # answers with just job title thats consists of 2 words
        elif ((token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "ADJ") and token.dep_ == "compound") and\
                (token.head.text == doc[index + 1].text and (doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and\
                  doc[index + 1].dep_ == "ROOT") and\
                    (doc[index + 1].head.text == doc[index + 1].text):
            return print("possible job:" + token.text + " " + doc[index + 1].text)

        # One word job titles
        elif token.pos_ == "PROPN" and (token.dep_ == "compound" or token.dep_ == "pobj"):
            return print("possible job:" + token.text)
        else:
            if token.pos_ == "NOUN" and (token.dep_ == "attr" or token.dep_ == "ROOT") and doc[index - 1].head == token:
                return print("possible job:" + token.text)
    return print("No role found")


# test_answers = [
#     "New York City, USA",
#     "London, UK",
#     "Tokyo, Japan",
#     "Istanbul, Turkey",
#     "Manchester, UK sounds fantastic!",
#     "Glasgow, UK is where I aim to work!",
#     "Frankfurt, Germany is where I see myself!"]


def extract_location(doc):
    num_tokens = len(doc)
    for index, token in enumerate(doc):
        # city, country country country
        if index + 4 < num_tokens and token.ent_type_ == "GPE" and\
                (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and\
                    (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT") and\
                        (doc[index + 3].ent_type_ == "GPE" or doc[index + 3].pos_ == "PUNCT") and\
                            (doc[index + 4].ent_type_ == "GPE" or doc[index + 4].pos_ == "PUNCT"):
            return print("possible location:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text + " " + doc[index + 3].text + " " + doc[index + 4].text)
        elif index + 3 < num_tokens and token.ent_type_ == "GPE" and\
              (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and\
                  (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT") and\
                      (doc[index + 3].ent_type_ == "GPE" or doc[index + 3].pos_ == "PUNCT"):
            return print("possible location:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text + " " + doc[index + 3].text)
        elif index + 2 < num_tokens and token.ent_type_ == "GPE" and\
              (doc[index + 1].ent_type_ == "GPE" or doc[index + 1].pos_ == "PUNCT") and\
                  (doc[index + 2].ent_type_ == "GPE" or doc[index + 2].pos_ == "PUNCT"):
            return print("possible location:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text)
        # country country
        elif index + 1 < num_tokens and token.ent_type_ == "GPE" and doc[index + 1].ent_type_ == "GPE":
            return print("possible location:" + token.text + " " + doc[index + 1].text)
        #One word (country or city)
        elif token.ent_type_ == "GPE":
            return print("possible location:" + token.text)
    return print("No location found")


# test_answers = [
#     'full time',
#     'part time',
#     'fulltime',
#     'parttime',
#     'full-time',
#     'part-time',
#     'I\'m available full-time',
#     'I\'m available part-time',
#     'full',
#     'part',
#     'I am looking for a full time job']


#type of job is either full-time or part-time
def extract_type_of_job(doc):
    num_tokens = len(doc)
    for index, token in enumerate(doc):
        # answer is in form: "full - time" or "part - time"
        if index + 2 < num_tokens and (token.pos_ == "ADJ" or token.pos_ == "NOUN") and (token.dep_ == "amod" or token.dep_ == "compound") and\
                (doc[index + 1].pos_ == "NOUN" or doc[index + 1].pos_ == "PUNCT") and\
                    (doc[index + 2].pos_ == "NOUN" and (doc[index + 2].dep_ == "ROOT" or doc[index + 2].dep_ == "npadvmod")):
            return print("possible type of job:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text)
        #answer consist of :"full time" or "part time"
        elif index + 1 < num_tokens and (token.pos_ == "NOUN" or token.pos_ == "ADJ") and token.dep_ == "amod" and\
                (doc[index+1].pos_ == "NOUN" and (doc[index+1].dep_ == "ROOT" or doc[index+1].dep_ == "compound")):
            return print("possible type of job:" + token.text + " " + doc[index+1].text)
        #answer is just: "full" or "part"
        elif token.text == "full" or token.text == "part":
            return print("possible type of job:" + token.text + "time")
    return print("I am sorry I don't understand. Please write 'full time' or 'part time'")


# test_answers = [
#     "Yes, I prefer a hybrid arrangement.",
#     "Hybrid offers the best of both worlds, so that's my preference.",
#     "I enjoy a hybrid model because it provides flexibility.",
#     "hybrid",
#     "remote",
#     "on-site",
#     "on site",
#     "No, I'm specifically seeking an on-site position.",
#     "I prefer an on-site job because I thrive in an office environment.",
#     "Working in person on-site helps me stay more focused and engaged.",
#     "I'm open to both hybrid and remote options.",
#     "I'm adaptable but would prefer an on-site role to stay connected with colleagues.",
#     "I find working remotely to be more productive, so I prefer remote.",
#     "Seeking remote roles exclusively for location independence.",
#     "Remote work offers a better work-life balance for me.",
#     "I prefer fully remote positions due to flexibility and lack of commute.",
#     "Hybrid work is appealing due to its balance of in-person and remote aspects.",
#     "A hybrid setup gives me the flexibility I need while still collaborating in person.",
#     "I enjoy working in an office, so I'd prefer an on-site position.",
#     "Remote is my top choice due to its flexibility and ability to work from anywhere.",
#     "I prioritize remote positions due to their flexibility and convenience.",
#     "Remote jobs allow me to optimize my time and avoid commuting.",
#     "I like the option of hybrid work because it allows for occasional face-to-face meetings.",
#     "Working on-site gives me a sense of structure and routine, which I value.",
#     "Hybrid is ideal as it lets me work from home but still have in-person collaboration.",
#     "I'm looking for a fully remote position to take advantage of location flexibility.",
#     "Remote work allows for better focus and fewer office distractions.",
#     "On-site roles are what I'm after because I value direct interaction with my team.",
#     "I prefer remote roles as they give me the freedom to manage my own schedule.",
#     "I'm comfortable with either hybrid or remote roles, as long as the work is flexible."
# ]



#on site, remote or hybrid work preference
def extract_work_preference(doc):
    num_tokens = len(doc)
    for index, token in enumerate(doc):
        # answer consists of: "on - site"
        if (index + 2 < num_tokens and token.pos_ == "ADP" and (token.dep_ == "ROOT" or token.dep_ == "nmod" or token.dep_ =="prep") and
            doc[index + 1].pos_ == "PUNCT" and
                  doc[index + 2].pos_ == "NOUN" and (doc[index + 2].dep_ == "pobj" or doc[index+2].dep_ =="compound")):
            return print("possible work preference:" + token.text + " " + doc[index+1].text + " " + doc[index + 2].text)
        
        # answer consists of: "on site"
        elif (index + 1 < num_tokens and token.pos_ == "ADP" and token.dep_ == "ROOT" and
            doc[index + 1].pos_ == "NOUN" and doc[index + 1].dep_ == "pobj"):
            return print("possible work preference:" + token.text + " " + doc[index+1].text)
        
        # answer consists of: "remote" or "hybrid"
        elif (index + 1 < num_tokens and token.pos_ == "ADJ" and
                (token.dep_ == "amod" or token.dep_ == "compound")):
            return print("possible work preference:" + token.text)
        
        # answer consists of "hybrid" i think
        elif (index + 1 < num_tokens and token.pos_ == "NOUN" and token.dep_ == "amod"):
            return print("possible work preference:" + token.text)
        
        # answer is just: "hybrid" or "remote"
        elif (token.pos_ == "NOUN" or token.pos_ == "ADJ") and (token.dep_ == "ROOT" or token.dep_ == "nsubj"):
            return print("possible work preference:" + token.text)
    
    return print("I am sorry I don't understand. Please write 'on-site', 'remote' or 'hybrid'")

def text_to_digits(text):
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

# test_answers = [
#     "10",
#     "twenty",
#     "I have 5 years of experience",
#     "Almost 3 years",
#     "Around nine years",
#     "Less than 2 years",
#     "More than 15 years",
#     "Approximately 7 years",
#     "Over 20 years",
#     "Over 5 years",
#     "Around 14 years",
#     "I've got 2 years under my belt",
#     "I'd say I'm experienced with 11 years",
#     "I've been in the field for 6 years now",
#     "Around 4 years more or less",
#     "Nearly ten years",
#     "Close to 12 years",
#     "I've accumulated 8 years of experience",
#     "Roughly 3 years",
#     "Nearly 7 years of experience",
#     "I have six years of experience",
#     "A little over 5 years",
#     "About a decade",
#     "Roughly nine years",
#     "Fourteen years of experience",
#     "Seventeen years in total",
#     "Twelve solid years",
#     "A bit over 3 years",
#     "Nearly five years"
# ]


# Extract years of experience from the user's response
def extract_experience(doc):
    for token in doc:
        if token.like_num == True:
            if token.text.isdigit():
                return print("possible years of experience:" + token.text)
            else:
                # Attempt to convert the textual representation to digits
                digit = text_to_digits(token.text)
                if digit is not None:
                    return print("possible years of experience:" + digit)

    return print("I am sorry I don't understand. Please write the number of years of experience you have.")



# test_answers = [
#     "yes", 
#     "yeah", 
#     "yep", 
#     "absolutely", 
#     "definitely", 
#     "sure",
#     "Of course I do, I worked hard for it.", 
#     "Yes, I have a degree in computer science.", 
#     "Absolutely, I earned my degree last year.", 
#     "Yeah, I completed my degree a few years ago.", 
#     "Sure, I’ve had my degree for a while now.",
#     "no", 
#     "nah", 
#     "nope", 
#     "not at all", 
#     "No, I don't have one unfortunately.", 
#     "Not at all, I haven't pursued higher education.", 
#     "No, I didn’t complete my degree.", 
#     "Unfortunately, no, I never got the chance to finish my studies.", 
#     "Nope, I never went to college."
# ]

# user will answer yes or no to the question if they have a degree (caps dont matter)
def extract_if_has_degree(doc):
    for token in doc:
        if token.text.lower() == "yes":
            return print("User has a degree")
        elif token.text.lower() == "no":
            return print("User does not have a degree")
    return print("I am sorry I don't understand. Please answer 'yes' or 'no'")


# test_answers = [
#     "computer science",
#     "I just graduated with a degree in environmental health sciences.",
#     "My degree is in applied computer science.",
#     "I completed my degree in mechanical systems engineering.",
#     "I earned my degree in business information systems.",
#     "I have a degree in international development studies.",
#     "I hold a degree in media and communication studies.",
#     "I have a degree in mathematics.",
#     "I just finished my degree in mechanical engineering.",
#     "I graduated with a degree in electrical engineering.",
#     "I hold a degree in biology.",
#     "I earned my degree in economics.",
#     "I have a degree in software engineering.",
#     "My degree is in psychology.",
#     "I graduated with a degree in chemistry.",
#     "I have a degree in architecture.",
#     "My degree is in data science.",
#     "I completed my degree in physics.",
#     "I have a degree in business administration.",
#     "I earned my degree in civil engineering.",
#     "I just graduated with a degree in nursing.",
#     "I have a degree in graphic design.",
#     "My degree is in environmental science.",
#     "I completed my degree in political science.",
#     "I have a degree in industrial engineering.",
#     "I just finished my degree in history.",
#     "psychology.",                                
#     "I have a degree in history.",
#     "I just completed my degree in environmental science.",
#     "I have a degree in marketing.",
#     "I earned my degree in urban planning.",
#     "I completed my degree in artificial intelligence.",
#     "My degree is in sociology."
# ]

# extract the name of the degree (computer science, mechanical engineering, etc.)
def extract_degree_field(doc):
    for index, token in enumerate(doc):
        #answers where the degree title consists of 3 words
        if (((token.pos_ == "ADJ" or token.pos_ == "NOUN" or token.pos_ == "PROPN") and (token.dep_ == "amod" or token.dep_ =="compound")) and\
              ((doc[index + 1].pos_ == "ADJ" or doc[index + 1].pos_ == "NOUN" or doc[index + 1].pos_ == "PROPN") and (doc[index + 1].dep_ == "compound" or doc[index + 1].dep_ == "amod")) and\
                  ((doc[index + 2].pos_ == "NOUN" or doc[index + 2].pos_ == "PROPN") and (doc[index + 2].dep_ == "pobj" or doc[index + 2].dep_ == "ROOT"))):
            return print("possible degree:" + token.text + " " + doc[index + 1].text + " " + doc[index + 2].text)
        
        # answers with just degree title that consists of 2 words
        elif (((token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ =="ADJ") and (token.dep_ == "compound" or token.dep_ == "amod")) and\
                  ((doc[index + 1].pos_ == "PROPN" or doc[index + 1].pos_ == "NOUN") and (doc[index + 1].dep_ == "compound" or doc[index + 1].dep_ == "pobj" or doc[index + 1].dep_ == "ROOT"))):
            return print("possible degree:" + token.text + " " + doc[index + 1].text)

        # answers with just degree title that consists of 1 word
        elif ((token.pos_ == "PROPN" or token.pos_ == "NOUN") and (token.dep_ == "pobj" or token.dep_ == "ROOT") and\
              (token.text != "degree")):
            return print("possible degree:" + token.text)
    return print("I am sorry I don't understand. Please write the name of the degree you have.")





for answer in test_answers:
    doc = nlp(answer)
    print_tokens(doc)
    print("--------------------------------------------------------------------------")
    extract_experience(doc)
    print("--------------------------------------------------------------------------")
# print("number of errors:" + str(errors))

# displacy.serve(nlp(test_answers[1]), style="dep",host="127.0.0.1")