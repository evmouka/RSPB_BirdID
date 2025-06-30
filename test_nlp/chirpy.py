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
    def __init__(self, csv_file: str):
        """Initialize with bird database"""
        self.df = pd.read_csv(csv_file, skiprows=1)
        self.df = self.df.fillna('')
        print("Bird database loaded successfully")

def main():
    # Initialize the bird identification system
    system_prompt = """You are Chirpy, an enthusiastic bird expert helping identify UK garden birds. Your goal is to:
    1. Have a natural conversation to gather key identifying features about birds
    2. Always ask about one feature at a time, in a conversational way
    3. Keep track of what you've learned about the bird
    4. Focus on these key features in this order:
       - Colors and markings
       - Size (compared to common birds like sparrows or pigeons)
       - Beak shape and color
       - Tail shape
       - Leg color and length
       - use 5 attributes to identify the bird
       - if you are confident, you can identify the bird
       - confidence = 5
       
    Important guidelines:
    - Start by asking if they've spotted a bird
    - After each user response, acknowledge what you learned
    - Ask for the next feature in a natural way
    - Keep track of the features already mentioned
    - Don't suggest bird identifications yet - just gather information
    - after 5 atributes have been identified, you can identify the bird
    - include the corresponding image from the birds.csv file in your response, showing the image of the bird you identified
    - If user mentions multiple features, acknowledge them all
    - keep your questions short and to the point
    
    Remember: You're having a friendly conversation, not conducting an interrogation. Be enthusiastic about their bird sighting!
    """

    bird_assistant = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY,
        system_prompt=system_prompt,
        stream=True
    )
    
    bird_db = BirdIdentifier('birds.csv')
    
    print("\nChirpy: Hey there! I'm Chirpy, let's try and identify the bird you spotted! 🦜")
    print("Tell mesomething about the bird you saw or type 'quit' to exit.")
    
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