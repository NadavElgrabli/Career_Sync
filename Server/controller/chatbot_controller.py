import ast
from jobscraper.run_scraper import Scraper

def handle_chat_request(data, chatbot):
    try:
        user_message = data.get("message")
        bot_response = ''
        
        if user_message == "start":
            chatbot.reset_chat()
            bot_response = "Hello! Welcome to Career Sync. What job are you looking for?"
        elif user_message == "nadav":
            bot_response = "DONE {'job': 'web developer', 'location': 'new york', 'type_of_job': 'full time', 'work_preference': 'hybrid', 'experience': '1', 'degree': True, 'degree_field': 'computer science'}"
        else:
            bot_response = chatbot.ask_question(user_message)
        
        if 'DONE' in bot_response:
            cleaned_response = bot_response.replace('DONE', '').strip()
            start_crawling(cleaned_response)
        
        return bot_response
    except Exception as e:
        print(f"Error during chatbot conversation: {e}")
        return "An error occurred during the chatbot conversation. Please try again."



def start_crawling(cleaned_response):
    
    job_preference_dic = ast.literal_eval(cleaned_response)
    
    scraper = Scraper(**job_preference_dic)
    scraper.run_spiders()
    