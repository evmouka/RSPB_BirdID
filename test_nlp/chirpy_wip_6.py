import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import anthropic
import json

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
        json_mode=False,
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
        
        # Add feature mappings for natural language understanding
        self.feature_mappings = {
            "colour": ["Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)"],
            "size": ["Size", "Min Length (cm)", "Max Length (cm)", "Wingspan (cm)", "Weight (g)"],
            "shape": ["Beak Shape 1", "Beak shape 2 (optional)", "Tail shape 1", "Tail shape 2 (optional)"],
            "pattern": ["Pattern/ Markings"],
            "habitat": ["Habitat(s)", "Where to see them (countries)"],
            "sound": ["Call"],
            "behaviour": ["Behaviour"],
            "name": ["Name", "Alt names/ mispellings", "Latin name"],
            "appearance": ["Appearance"],
            "common_terms": {
                "small": ["Size"],
                "large": ["Size"],
                "tiny": ["Size"],
                "huge": ["Size"],
                "spotted": ["Pattern/ Markings"],
                "striped": ["Pattern/ Markings"],
                "singing": ["Call"],
                "chirping": ["Call"],
                "garden": ["Habitat(s)"],
                "park": ["Habitat(s)"],
                "urban": ["Habitat(s)"]
            }
        }
        print("Bird database loaded successfully")

    def map_user_input(self, user_text: str) -> Dict[str, List[str]]:
        """Map user input to relevant database columns"""
        mapped_fields = {}
        user_text = user_text.lower()
        
        if any(colour in user_text for colour in ["red", "blue", "green", "yellow", "black", "white", "brown", "grey", "orange"]):
            mapped_fields["colour"] = self.feature_mappings["colour"]
            
        if any(size in user_text for size in ["small", "large", "tiny", "huge", "big", "little"]):
            mapped_fields["size"] = self.feature_mappings["size"]
            
        if any(shape in user_text for shape in ["beak", "tail", "pointed", "curved", "long", "short"]):
            mapped_fields["shape"] = self.feature_mappings["shape"]
            
        if any(pattern in user_text for pattern in ["spotted", "striped", "marking", "pattern"]):
            mapped_fields["pattern"] = self.feature_mappings["pattern"]
            
        if any(behaviour in user_text for behaviour in ["flying", "eating", "singing", "chirping"]):
            mapped_fields["behavior"] = self.feature_mappings["behaviour"]
            
        if any(habitat in user_text for habitat in ["garden", "park", "tree", "urban", "woodland"]):
            mapped_fields["habitat"] = self.feature_mappings["habitat"]
            
        for term, columns in self.feature_mappings["common_terms"].items():
            if term in user_text:
                mapped_fields[term] = columns
                
        return mapped_fields

def show_tail_shape_guide():
    pdf_path = './tail_shape.pdf'
    if os.path.exists(pdf_path):
        os.system(f'open {pdf_path}')

def beak_beak_shape_guide():
    pdf_path = './beak_shape.pdf'
    if os.path.exists(pdf_path):
        os.system(f'open {pdf_path}')

def main():
    system_prompt = """You are Chirpy, an enthusiastic bird expert helping identify UK garden birds, while teachimg you how to.
    """
    prompt = """Your goal is to:
    1. Have a natural conversation to gather key identifying features about birds
        - use appropriate emojis to make more fun
    2. Always ask about one feature at a time, in a conversational way
    3. Keep track of what you've learned about the bird
    4. Focus on these key features in this order:
       - Plumage colour(s)
       - Pattern/Markings
       - Size (compared to common birds like sparrows or pigeons)
       - Beak shape, ask exacly as "beak shape"
       - Beak colour(s)
       - Tail shape, ask exacly as "tail shape"
       - Feet colour(s) 
       - Feet length
       - use these attributes to identify the bird
       - don't ask about the same feature twice in a row
       - aknowledge attributes the user mentiones, you may ask one more question about the attribute if neccesary
       - if you are confident, you can identify the bird
       - confidence = 5
    5. Use UK spelling and terms for birds
    
    additional database context:
- Map user descriptions to these database fields:
  - Colours → Plumage colour(s), Beak Colour(s), Feet colour(s), Leg colour(s)
  - Size → Size, Length, Wingspan, Weight
  - Shape → Beak Shape, Tail shape
  - Pattern → Pattern/Markings
  - Habitat → Habitat(s), Where to see them
  - Sound → Call
  - Behaviour → Behaviour
  
    Important guidelines:
    - Start by asking if they've spotted a bird
    - keep the conversation flowing naturally
    - help the user with how to porvide the information by giving examples
    - don't repat questions
    - don't ask about the same feature twice
    - ask about one feature at a time, in a conversational way
    - Only use information from the bird_data.json file to identify the bird
    - After each user response, acknowledge what you've learned
    - Ask for the next feature in a natural way
    - Keep track of the features already mentioned
    - make sure you don't ask about things twice
    - If you get vague input, ask clarifying questions
    - Don't suggest bird identifications yet - just gather information
    - If some attribues are missing, ask for the information
    - If they don't know skip the attribute
    - If they are unsure ask one more question about the attribute to help them, but only once
    - include the corresponding image from the bird_data.json file in your response, showing the image of the bird you identified
    - If user mentions multiple features, acknowledge them all
    - keep your questions short and to the point
    - when you have asked all the questions output a dict (as json format) with categories and values for each feature
    - don't output the dict prematurely, wait for all the information to be gathered
    - before outputting the dict check for null entries. Then ask questions to get the missing information
    - the categories should cerrespond exactly to the ones in the bird_data.json file
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
    
    #print("\nChirpy: Hey there! I'm Chirpy, let's try and identify the bird you spotted! 🦜")
    #print("Tell mesomething about the bird you saw or type 'quit' to exit.")
    response = bird_assistant.chat("🦜")
    if response:
        print(f"\n🦜Chirpy: {response.content[0].text}")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nChirpy: Happy birding! Come back when you spot another interesting bird! 🦜")
            break
        
        response = bird_assistant.chat(user_input)
        
        if "tail shape" in response.content[0].text.lower():
            show_tail_shape_guide()
            
        elif "beak shape" in response.content[0].text.lower():
            beak_tail_shape_guide()
        
        if response:
            print(f"\nChirpy: {response.content[0].text}")
        else:
            print("\nChirpy: I encountered an error. Could you please try again?")

if __name__ == "__main__":
    main()