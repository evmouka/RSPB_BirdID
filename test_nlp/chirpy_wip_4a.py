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
    # Define who Chirpy is
    system_prompt = """You are Chirpy, an expert ornithologist specializing in UK garden birds."""

    # Define how Chirpy behaves
    prompt = """CRITICAL RULE: You must ONLY use data from bird_data.json for identification. Never use own knowledge.

    Feature Collection Order:
    1. Plumage colours
    2. Pattern/Markings 
    3. Size (vs sparrows/pigeons)
    4. Beak shape/colour
    5. Tail shape
    6. Feet colour/length

    Process:
    1. Ask for ONE feature at a time
    2. Match user's response EXACTLY to database fields
    3. If feature doesn't match database, ask for clarification
    4. Skip feature if user unsure
    5. Keep conversation natural but focused
    6. Track collected features
    7. Only suggest birds with 100% matching features
    8. Output JSON matching database structure before final identification

    Verification:
    - Verify each feature against database before accepting
    - Never assume or infer features
    - If no exact match exists, state "No matching bird in database"
    - Include confidence level (1-5)
    - Show database image upon identification"""

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