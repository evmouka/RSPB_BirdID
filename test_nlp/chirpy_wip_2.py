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
        self.collected_info = {
            'colours': [],
            'beak_shape': [],
            'beak_colour': [],
            'size': [],
            'leg_size': [],
            'leg_colour': [],
            'tail_shape': [],
            'patterns': []
        }
        self.confidence_threshold = 0.6

    def update_info(self, feature_type: str, value: str):
        if feature_type in self.collected_info and value:
            if isinstance(value, list):
                self.collected_info[feature_type].extend(value)
            else:
                self.collected_info[feature_type].append(value)
            # Remove duplicates
            self.collected_info[feature_type] = list(set(self.collected_info[feature_type]))

    def get_missing_features(self) -> List[str]:
        return [k for k, v in self.collected_info.items() if not v]

    def calculate_match(self) -> List[Tuple[str, float, Dict]]:
        matches = []
        for _, bird in self.df.iterrows():
            score = 0
            total_weights = 0
            
            weights = {
                'colours': 0.3,
                'beak_shape': 0.15,
                'beak_colour': 0.1,
                'size': 0.15,
                'leg_size': 0.05,
                'leg_colour': 0.05,
                'tail_shape': 0.1,
                'patterns': 0.1
            }

            for feature, weight in weights.items():
                if self.collected_info[feature]:
                    total_weights += weight
                    if feature == 'colours':
                        bird_colors = str(bird['Plumage colour(s)']).lower().split(',')
                        bird_colors = [c.strip() for c in bird_colors]
                        user_colors = [c.lower() for c in self.collected_info[feature]]
                        color_match = sum(1 for c in user_colors if any(c in bc for bc in bird_colors))
                        score += (color_match / len(user_colors)) * weight
                    elif feature in ['size', 'beak_shape', 'tail_shape']:
                        field_map = {
                            'size': 'Size',
                            'beak_shape': 'Beak Shape 1',
                            'tail_shape': 'Tail shape 1'
                        }
                        if str(bird[field_map[feature]]).lower() in [s.lower() for s in self.collected_info[feature]]:
                            score += weight

            if total_weights > 0:
                confidence = score / total_weights
                if confidence >= self.confidence_threshold:
                    bird_details = {
                        'name': bird['Name'],
                        'appearance': bird['Appearance'],
                        'behaviour': bird['Behaviour'],
                        'facts': [f for f in [bird.get('Fact 1', ''), bird.get('Fact 2', ''), bird.get('Fact 3', '')] if f]
                    }
                    matches.append((bird['Name'], confidence, bird_details))

        return sorted(matches, key=lambda x: x[1], reverse=True)

class ChirpyAssistant:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.bird_identifier = BirdIdentifier('birds.csv')
        self.conversation_state = 'greeting'
        self.questions = {
            'colours': "What colors did you notice on the bird?",
            'beak_shape': "How would you describe the shape of the beak? Is it short and stubby, long and thin, hooked, etc?",
            'beak_colour': "What color was the beak?",
            'size': "How big was the bird? You can compare it to familiar birds like sparrows or pigeons.",
            'leg_size': "How would you describe the legs - long, short, medium?",
            'leg_colour': "What color were the legs?",
            'tail_shape': "How would you describe the tail shape - forked, fan-shaped, pointed?",
            'patterns': "Did you notice any particular patterns or markings on the bird?"
        }
        self.current_feature = 'colours'
        self.features_asked = set()

    def extract_features(self, user_input: str) -> Dict[str, str]:
        # Handle special responses
        if user_input.lower() in ["i have done that", "i told you", "already answered"]:
            return {}

        prompt = f"""Extract bird features from this description: "{user_input}"
        Return a JSON object with any of these features that are EXPLICITLY mentioned:
        - colours: list of colors mentioned
        - beak_shape: one of [short and stubby, long and thin, hooked, curved, sharp, pointed]
        - beak_colour: color of the beak
        - size: one of [small, medium, large, extra small]
        - leg_size: one of [short, medium, long]
        - leg_colour: color of legs
        - tail_shape: one of [forked, pointed, fan, square]
        - patterns: any specific markings

        Include ONLY features that are clearly stated in the description.
        For example: "short and stubby" would return {{"beak_shape": "short and stubby"}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            extracted = json.loads(response.content[0].text)
            print(f"Extracted features: {extracted}")  # Debug print
            return extracted
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            # Try to handle direct responses
            if "short" in user_input.lower() and "stubby" in user_input.lower():
                return {"beak_shape": "short and stubby"}
            return {}
        except Exception as e:
            print(f"Error extracting features: {e}")
            return {}

    def get_next_question(self) -> str:
        """Get the next feature to ask about."""
        all_features = list(self.questions.keys())
        for feature in all_features:
            if feature not in self.features_asked:
                self.current_feature = feature
                self.features_asked.add(feature)
                return self.questions[feature]
        return None

    def process_response(self, user_input: str) -> str:
        if self.conversation_state == 'greeting':
            if user_input.lower() in ['yes', 'yeah', 'yep', 'y']:
                self.conversation_state = 'collecting_info'
                return "Fantastic! Let's identify your feathered friend! " + self.questions['colours']
            else:
                return "No worries! When you do spot a bird, I'll be here to help identify it. Just let me know!"

        elif self.conversation_state == 'collecting_info':
            # Extract features from user input
            extracted_features = self.extract_features(user_input)
            
            # Update collected information
            for feature_type, value in extracted_features.items():
                self.bird_identifier.update_info(feature_type, value)

            # Get next question
            next_question = self.get_next_question()
            if next_question:
                return f"Thank you! {next_question}"
            else:
                # We've asked all questions, try to identify the bird
                self.conversation_state = 'identification'
                matches = self.bird_identifier.calculate_match()
                if matches:
                    return self.format_identification(matches[0])
                else:
                    return "I'm not quite sure which bird it is based on the description. Would you like to try again with a different description?"

    def format_identification(self, match_tuple: Tuple[str, float, Dict]) -> str:
        name, confidence, details = match_tuple
        response = f"I think I know your bird! With {confidence:.1%} confidence, it's a {name}!\n\n"
        if details['appearance']:
            response += f"Description: {details['appearance']}\n\n"
        if details['facts']:
            response += "Fun fact: " + details['facts'][0]
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
            
        response = assistant.process_response(user_input)
        print(f"\nChirpy: {response}")

if __name__ == "__main__":
    main()