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
        prompt="",
        stream=False,
    ):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.prompt = prompt
        self.stream = stream
        self.history = []
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def add_message(self, role, content):
        if not self.history and self.prompt:
            self.history.append({"role": "assistant", "content": self.prompt})
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
            "messages": [{"role": "user", "content": self.prompt}] + self.history,
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
        self.df = pd.read_json(json_file)
        self.df = self.df.fillna('')
        print("Bird database loaded successfully")

def main():
    system_prompt = """You are Chirpy, an engaging conversasionist who knows how to identify birds and will help children learn how to identify birds."""

    prompt = """CRITICAL RULES: 
    1. ONLY use information from bird_data.json for identification
    2. NEVER reference external sources like Wikipedia or your own.

    Your goal is to:
    1. Have a natural conversation to gather key identifying features about birds
    2. Always ask about one feature at a time, in a conversational way
    3. Keep track of what you've learned about the bird
    
    Feature Collection Order:
    1. Plumage colours
    2. Pattern/Markings 
    3. Size (vs sparrows/pigeons)
    4. Beak shape/colour
    5. Tail shape
    6. Feet colour/length

    Process:
    1. Start by asking if they've spotted a bird
    2. keep the conversation flowing naturally
    3. help the user with how to porvide the information by giving examples
    4. Ask for ONE feature at a time
    5. Skip feature if user unsure
    6. Keep track of your questions so you don't repeat yourself
    7. Keep conversation natural but focused
    8. Track collected features
    9. when you have collected four complete features, output JSON formated dictionary
    10. If user asks for identification after then try to provide it
    
    Guidelines:
    - don't ask about same feature twice, unless no response
    - don't ask about same attribute twice, unless no response
    - 
    """

    bird_assistant = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY,
        system_prompt=system_prompt,
        prompt=prompt,
        stream=True
    )
    
    bird_db = BirdIdentifier('bird_data.json')
    
    print("\nChirpy: Hey there! I'm Chirpy, let's identify that bird! 🦜")
    print("Tell me about the bird you saw or type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nChirpy: Happy birding! 🦜")
            break
            
        response = bird_assistant.chat(user_input)
        if response:
            # Only print the text content, not the full Message object
            print(f"\nChirpy: {response.content[0].text}")
        else:
            print("\nChirpy: I encountered an error. Please try again.")

if __name__ == "__main__":
    main()