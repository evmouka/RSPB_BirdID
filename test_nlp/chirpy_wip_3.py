import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import anthropic
import json

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

class BirdIdentifier:
    def __init__(self, csv_file: str):
        self.df = pd.read_csv(csv_file, skiprows=1)
        self.df = self.df.fillna('')
        # Load unique values for each feature from the database
        self.available_features = {
            'colours': self.get_unique_values('Plumage colour(s)'),
            'size': self.get_unique_values('Size'),
            'beak_shape': self.get_unique_values('Beak Shape 1'),
            'beak_colour': self.get_unique_values('Beak Colour(s)'),
            'leg_colour': self.get_unique_values('Feet colour(s)'),
            'tail_shape': self.get_unique_values('Tail shape 1'),
            'patterns': self.get_unique_values('Pattern/ Markings')
        }

    def get_unique_values(self, column: str) -> List[str]:
        if column in self.df.columns:
            values = []
            for val in self.df[column].dropna():
                values.extend([v.strip() for v in str(val).split(',')])
            return list(set(values))
        return []

    def find_matching_birds(self, features: Dict[str, List[str]]) -> List[Tuple[str, float, Dict]]:
        matches = []
        for _, bird in self.df.iterrows():
            score = self.calculate_match_score(bird, features)
            if score > 0.3:  # Minimum confidence threshold
                details = {
                    'name': bird['Name'],
                    'appearance': bird['Appearance'],
                    'behaviour': bird['Behaviour'],
                    'facts': [bird.get('Fact 1', ''), bird.get('Fact 2', ''), bird.get('Fact 3', '')]
                }
                matches.append((bird['Name'], score, details))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def calculate_match_score(self, bird, features: Dict[str, List[str]]) -> float:
        # Add matching logic here based on features
        # Return score between 0 and 1
        return 0.5  # Placeholder

class ChirpyAssistant:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.bird_identifier = BirdIdentifier('birds.csv')
        self.current_features = {}
        self.chat_history = []
        
        # Create initial system prompt using available features from database
        self.system_prompt = f"""You are Chirpy, a friendly and knowledgeable bird identification assistant. 
        Your goal is to help identify birds by having natural conversations with users.
        
        You have access to a database of UK garden birds with these features:
        {json.dumps(self.bird_identifier.available_features, indent=2)}

        Follow these guidelines:
        1. Be friendly and enthusiastic about birds
        2. Ask one question at a time about the bird's features
        3. Focus on getting clear information about:
           - Colors and patterns
           - Size (compared to common birds)
           - Beak shape and color
           - Tail shape
           - Leg color and length
        4. Acknowledge what the user has told you and build on it
        5. If the user provides multiple features, note them all
        6. Don't guess the bird until you have at least 3-4 key features
        7. Use natural conversation, not rigid questions

        Current features collected: {self.current_features}

        Respond in a conversational way, like an enthusiastic bird expert chatting with a friend."""

    def chat(self, user_message: str) -> str:
        # Add user message to history
        self.chat_history.append({"role": "user", "content": user_message})
        
        try:
            # Create conversation with Claude
            messages = [
                {"role": "system", "content": self.system_prompt},
                *self.chat_history
            ]
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0.7,
                messages=messages
            )
            
            # Extract Claude's response
            assistant_message = response.content[0].text
            
            # Add response to history
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            
            # Extract any features mentioned
            self._extract_features(user_message)
            
            # Check if we have enough features to identify the bird
            if len(self.current_features) >= 3:
                matches = self.bird_identifier.find_matching_birds(self.current_features)
                if matches:
                    bird_info = self._format_bird_info(matches[0])
                    assistant_message += f"\n\n{bird_info}"
            
            return assistant_message
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I apologize, I encountered an error. Could you rephrase that?"

    def _extract_features(self, user_message: str):
        # Ask Claude to extract features from user message
        feature_prompt = f"""Extract bird features from this message: "{user_message}"
        Return a JSON object containing any mentioned features from these categories:
        {json.dumps(self.bird_identifier.available_features, indent=2)}
        Only include features that are explicitly mentioned."""
        
        try:
            feature_response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                temperature=0,
                messages=[{"role": "user", "content": feature_prompt}]
            )
            
            features = json.loads(feature_response.content[0].text)
            self.current_features.update(features)
            
        except Exception as e:
            print(f"Error extracting features: {e}")

    def _format_bird_info(self, match_tuple: Tuple[str, float, Dict]) -> str:
        name, confidence, details = match_tuple
        response = f"Based on your description, I think this might be a {name} (confidence: {confidence:.1%})!\n\n"
        if details['appearance']:
            response += f"{details['appearance']}\n\n"
        if any(details['facts']):
            response += f"Fun fact: {next(f for f in details['facts'] if f)}"
        return response

def main():
    assistant = ChirpyAssistant(ANTHROPIC_API_KEY)
    
    print("\nChirpy: Hey there! I'm Chirpy, your friendly bird identification assistant!")
    print("Have you spotted a bird you'd like to identify?")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nChirpy: Happy birding! Come back when you spot another interesting bird! 🦜")
            break
            
        response = assistant.chat(user_input)
        print(f"\nChirpy: {response}")

if __name__ == "__main__":
    main()