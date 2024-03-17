import google.generativeai as genai

class GenerativeModel:
    def __init__(self, model_name, api_key=None):
        if api_key is not None:
            genai.configure(api_key=api_key)
            #configure harm safety settings at chat object

            self.model = genai.GenerativeModel(model_name)
        else:
            print("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    
    def chat_object(self, history=[]):
        return self.model.start_chat(history=history)