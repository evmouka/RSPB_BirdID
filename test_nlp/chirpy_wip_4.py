import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import anthropic
import json

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class AnthropicCalls:
    def __init__(
        self,
        name="Anthropic Chat",
        api_key="",
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.7,
        system_prompt="",
        stream=False,
    ):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.stream = stream
        self.history = []
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
    
    def clear_history(self):
        self.history.clear()

    def chat(self, message, clear_after_response=False, **kwargs):
        self.add_message("user", message)
        response = self.get_response(**kwargs)
        if clear_after_response:
            self.clear_history()
        return response
        
    def get_response(self, should_print=True, **kwargs) -> str:
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self.history,
            "system": self.system_prompt,
            **kwargs
        }
        
        try:
            response = self.client.messages.create(**params)
            return response
        except Exception as e:
            print(f"Error in chat: {e}")
            return None

class BirdIdentifier:
    def __init__(self, json_file: str):
        """Initialize with bird database"""
        self.df = pd.read_json(json_file) #code for taking in .json file instead of .csv:  pd.read_json(csv_file)
        self.df = self.df.fillna('')
        print("Bird database loaded successfully")

def main():
    # Initialize the bird identification system
    system_prompt = """You are Chirpy, a bird identification assistant that ONLY uses the provided bird_data.json database.
    
    Critical Rules:
    1. ONLY use information from bird_data.json for identification
    2. NEVER reference external sources like Wikipedia
    
    Your goal is to:
    1. Have a natural conversation to gather key identifying features about birds
    2. Always ask about one feature at a time, in a conversational way
    3. Keep track of what you've learned about the bird
    4. Focus on these key features in this order:
       - Plumage colour(s)
       - Pattern/Markings
       - Size (compared to common birds like sparrows or pigeons)
       - Beak shape 
       - Beak colour(s)
       - Tail shape
       - Feet colour(s) 
       - Feet length
       - use these attributes to identify the bird
       - if you are confident, you can identify the bird
       - confidence = 5
    5. Use UK spelling and terms for birds
    Important guidelines:
    - Start by asking if they've spotted a bird
    - keep the conversation flowing naturally
    - help the user with how to porvide the information by giving examples
    - don't repat questions
    - ask about one feature at a time, in a conversational way
    - Only use information for the bird_data.json file to identify the bird
    - After each user response, acknowledge what you learned
    - Ask for the next feature in a natural way
    - Keep track of the features already mentioned
    - If you get vague input, ask clarifying questions
    - Don't suggest bird identifications yet - just gather information
    - If some attribues are missing, ask for the information
    - If they don't know skip the attribute
    - If they are unsure ask one more question about the attribute to help them
    - include the corresponding image from the bird_data.json file in your response, showing the image of the bird you identified
    - If user mentions multiple features, acknowledge them all
    - keep your questions short and to the point
    - Output final identification as a JSON dictionary matching database structure    - before outputting the dict check for null entries. Then ask questions to get the missing information
    - the categories should cerrespond exactly to the features in the bird_data.json file
    - only output the json dictionary, no other text
    - if asked after you have outputed the dictionary, you can identify the bird
    
    Remember: You're having a friendly conversation, not conducting an interrogation. Be enthusiastic about their bird sighting!
    """

    bird_assistant = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY,
        system_prompt=system_prompt,
        stream=True
    )
    
    bird_db = BirdIdentifier('bird_data.json')
    
    print("\nChirpy: Hey there! I'm Chirpy, let's try and identify the bird you spotted! 🦜")
    print("Tell me something about the bird you saw or type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nChirpy: Happy birding! Come back when you spot another interesting bird! 🦜")
            break
            
        response = bird_assistant.chat(user_input)
        if response:
            print(f"\nChirpy: {response.content[0].text}")
        else:
            print("\nChirpy: I encountered an error. Could you please try again?")

if __name__ == "__main__":
    main()