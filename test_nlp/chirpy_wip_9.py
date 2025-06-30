import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Set
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
        self.df = pd.read_json(json_file)
        self.df = self.df.fillna('')
        
        self.feature_mappings = {
            "colour": ["Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)"],
            "size": ["Size", "Min Length (cm)", "Max Length (cm)", "Wingspan (cm)", "Weight (g)"],
            "shape": ["Beak Shape 1", "Beak shape 2 (optional)", "Tail shape 1", "Tail shape 2 (optional)"],
            "pattern": ["Pattern/ Markings"],
            "habitat": ["Habitat(s)", "Where to see them (countries)"],
            "sound": ["Call"],
            "behaviour": ["Behaviour"],
            "name": ["Name", "Alt names/ mispellings", "Latin name"],
            "appearance": ["Appearance"]
        }
        print("Bird database loaded successfully")

class BirdConversationHandler:
    def __init__(self, words_file: str):
        with open(words_file) as f:
            self.valid_terms = json.load(f)
        
        self.required_fields = [
            "Plumage colour(s)",
            "Pattern/ Markings", 
            "Size",
            "Beak Shape 1",
            "Beak Colour(s)",
            "Tail shape 1",
            "Feet colour(s)",
            "Leg colour(s)"
        ]
        
        self.collected_info = {field: None for field in self.required_fields}
        self.asked_questions = set()
        self.current_feature = None

    def extract_features(self, text: str) -> dict:
        text = text.lower()
        features = {}
        
        # Handle size specifically
        size_mappings = {
            "small": "small",
            "medium": "medium",
            "large": "large",
            "tiny": "extra small"
        }
        for size_word, size_value in size_mappings.items():
            if size_word in text:
                features["Size"] = size_value
                
        # Handle other features
        for field, valid_values in self.valid_terms.items():
            values = [v.lower() for v in valid_values.split(", ")]
            matches = [v for v in values if v in text]
            if matches:
                features[field] = matches[0]
                
        return features

    def update_collected_info(self, features: dict):
        for field, value in features.items():
            if field in self.collected_info:
                self.collected_info[field] = value
                print(f"Updated {field}: {value}")  # Debug line

    def format_current_knowledge(self) -> str:
        info = []
        for field, value in self.collected_info.items():
            if value:
                info.append(f"{field}: {value}")
        return "Current information:\n" + "\n".join(info) if info else ""

    def get_next_question(self) -> str:
        questions = {
            "Plumage colour(s)": "What are the main colors of the bird? 🎨",
            "Pattern/ Markings": "Do you notice any patterns or markings on the bird? 👁️",
            "Size": "How big is the bird compared to common birds like sparrows or pigeons? 📏",
            "Beak Shape 1": "What shape is the beak? (e.g. sharp, curved, pointed) 🐦",
            "Beak Colour(s)": "What color is the beak? 🎨",
            "Tail shape 1": "What shape is the tail? (e.g. forked, fan-shaped, pointed) 🪽",
            "Feet colour(s)": "What color are the feet? 🦶",
            "Leg colour(s)": "What color are the legs? 🦿"
        }

        for field in self.required_fields:
            if not self.collected_info[field] and field not in self.asked_questions:
                self.asked_questions.add(field)
                self.current_feature = field
                return questions[field]
        return None

    def get_collected_info(self) -> dict:
        return {k: v for k, v in self.collected_info.items() if v is not None}

    def is_complete(self) -> bool:
        required_count = len([v for v in self.collected_info.values() if v])
        return required_count >= 3

def main():
    system_prompt = """You are Chirpy, an enthusiastic bird expert helping identify UK garden birds. Your task is to maintain a natural conversation while gathering specific information about birds. Important rules:

1. Always acknowledge new information the user provides
2. Ask only ONE question at a time
3. Never repeat questions about features already provided
4. Keep responses concise and focused
5. When you have collected at least 3 features, output a JSON dictionary in this format:
   {
       "Plumage colour(s)": "value",
       "Pattern/ Markings": "value",
       "Size": "value",
       ...
   }
6. Only output the JSON when you have enough information and the user seems done describing

Key features to collect:
- Plumage colour(s)
- Pattern/ Markings
- Size
- Beak Shape 1
- Beak Colour(s)
- Tail shape 1
- Feet colour(s)
- Leg colour(s)"""

    bird_assistant = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY,
        system_prompt=system_prompt,
        stream=True
    )
    
    conversation_handler = BirdConversationHandler('words.json')
    
    print("\nChirpy: Hey there! I'm Chirpy, let's identify the bird you spotted! 🦜")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nChirpy: Happy birding! Come back when you spot another interesting bird! 🦜")
            break
        
        features = conversation_handler.extract_features(user_input)
        conversation_handler.update_collected_info(features)
        
        # Create context for Claude including current knowledge
        context = conversation_handler.format_current_knowledge()
        next_question = conversation_handler.get_next_question()
        
        if conversation_handler.is_complete():
            message = f"{context}\nBased on this information, please provide the data in JSON format."
        else:
            message = f"{context}\n{next_question if next_question else 'Can you tell me anything else about the bird?'}"
            
        if "tail shape" in message.lower():
            show_tail_shape_guide()
        elif "beak shape" in message.lower():
            beak_shape_guide()
            
        response = bird_assistant.chat(message)
        if response:
            print(f"\nChirpy: {response.content[0].text}")
        else:
            print("\nChirpy: I encountered an error. Could you please try again?")

if __name__ == "__main__":
    main()