import ast
from utils import update_last_search
from jobscraper.run_scraper import Scraper
from algorithm.chatbot import Chatbot
from db import db


def handle_chat_request(data, chatbot : Chatbot):
    try:
        user_message = data.get("message")
        username = data.get("username")
        bot_response = ''
        
        if user_message == "start":
            chatbot.reset_chat()
            bot_response = "Hello! Welcome to Career Sync. What job are you looking for?"
        elif user_message == "test":
            bot_response = "DONE {'job': 'web developer', 'location': 'new york', 'job_type': 'full time', 'job_preference': 'onsite', 'experience': '1', 'degree': False, 'degree_field': ''}"
        else:
            bot_response = chatbot.ask_question(user_message)
        
        if 'DONE' in bot_response:
            cleaned_response = bot_response.replace('DONE', '').strip()
            start_crawling(cleaned_response, username)
            bot_response = "Thank you! Let's move forward with the next step."
            return bot_response
        
        return bot_response
    except Exception as e:
        print(f"Error during chatbot conversation: {e}")
        return "An error occurred during the chatbot conversation. Please try again."



def start_crawling(cleaned_response,username):
    
    job_preference_dic = ast.literal_eval(cleaned_response)
    job_preference_dic["username"] = username
    
    update_last_search(username,job_preference_dic)
    
    scraper = Scraper(**job_preference_dic)
    scraper.run_spiders()
    