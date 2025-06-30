import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import anthropic
import json

class BirdKnowledgeBase:
    def __init__(self, json_file: str):
        """Initialize with bird database"""
        # Load and process JSON data
        self.df = pd.read_json(json_file)
        self.df = self.df.fillna('')
        
        # Define feature mappings for natural language understanding
        self.feature_mappings = {
            "colour": ["Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)"],
            "size": ["Size", "Min Length (cm)", "Max Length (cm)", "Wingspan (cm)", "Weight (g)"],
            "shape": ["Beak Shape 1", "Beak shape 2 (optional)", "Tail shape 1", "Tail shape 2 (optional)"],
            "pattern": ["Pattern/ Markings"],
            "habitat": ["Habitat(s)", "Where to see them (countries)"],
            "sound": ["Call"],
            "behaviour": ["Behaviour"]
        }
        print("Bird database loaded successfully")
    
    def search_birds(self, criteria: Dict[str, str]) -> pd.DataFrame:
        """Search birds based on criteria"""
        mask = pd.Series(True, index=self.df.index)
        
        for category, value in criteria.items():
            if category in self.feature_mappings:
                category_mask = pd.Series(False, index=self.df.index)
                for field in self.feature_mappings[category]:
                    if field in self.df.columns:
                        field_match = self.df[field].str.contains(value, case=False, na=False)
                        category_mask = category_mask | field_match
                mask = mask & category_mask
        
        return self.df[mask]

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
        bird_identifier=None
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
        self.bird_identifier = bird_identifier

    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.history.append({"role": role, "content": content})
    
    def clear_history(self):
        """Clear the conversation history"""
        self.history = []

    def chat(self, message: str, clear_after_response=False, **kwargs) -> str:
        """Send a message and get a response"""
        self.add_message("user", message)
        response = self.get_response(**kwargs)
        
        if response:
            self.add_message("assistant", response.content[0].text)
            
        if clear_after_response:
            self.clear_history()
        return response
        
    def get_response(self, should_print=True, **kwargs) -> str:
        """Get a response from the model"""
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

def main():
    # Initialize the bird identification system
    system_prompt = """You are Chirpy, an enthusiastic bird expert helping identify UK garden birds. Your goal is to:
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
       - Use these attributes to identify the bird
       - If you are confident, you can identify the bird
       - Confidence = 5
    5. Use UK spelling and terms for birds
    
    Important guidelines:
    - Start by asking if they've spotted a bird
    - Keep the conversation flowing naturally
    - Help the user with how to provide the information by giving examples
    - Don't repeat questions
    - Ask about one feature at a time, in a conversational way
    - Only use information from the bird_data.json file to identify the bird
    - After each user response, acknowledge what you learned
    - Ask for the next feature in a natural way
    - Keep track of the features already mentioned
    - If you get vague input, ask clarifying questions
    - Don't suggest bird identifications yet - just gather information
    - If some attributes are missing, ask for the information
    - If they don't know skip the attribute
    - If they are unsure ask one more question about the attribute to help them
    - Include the corresponding image from the bird_data.json file in your response
    - If user mentions multiple features, acknowledge them all
    - Keep your questions short and to the point
    
    Remember: You're having a friendly conversation, not conducting an interrogation. Be enthusiastic about their bird sighting!"""

    # Initialize the knowledge base and chatbot
    knowledge_base = BirdKnowledgeBase('bird_data.json')
    
    bird_assistant = AnthropicCalls(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        system_prompt=system_prompt,
        stream=True,
        bird_identifier=knowledge_base
    )
    
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