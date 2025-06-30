import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import anthropic

# Load environment variables
load_dotenv()

# Get API key
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Verify API key is loaded
if ANTHROPIC_API_KEY is None:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

class AnthropicCalls:
    def __init__(
            self,
            api_key: str,
            system_prompt: str = "",
            model: str = "claude-3-5-sonnet-20240620",
            max_tokens: int = 1024,
            temperature: float = 0.7
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.history = []

    def chat(self, message: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error in chat: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

class BirdIdentificationAssistant:
    def __init__(self, csv_file: str):
        """Initialize the bird identification assistant with the bird database."""
        try:
            # Skip the first row when reading the CSV
            self.df = pd.read_csv(csv_file, skiprows=1)
            # print("CSV file loaded successfully")
            # print("\nAvailable columns:", list(self.df.columns))
            
            # Clean and prepare the data
            self.df = self.df.fillna('')
            
            # Print first few rows to verify data
            # print("\nFirst few rows of data:")
            # print(self.df.head(2))
            
             # Define column mappings
            self.column_mappings = {
                'plumage': 'Plumage colour(s)',
                'size': 'Size',
                'beak': 'Beak Shape 1',
                'habitat': 'Habitat(s)',
                'behavior': 'Behaviour'
            }
            
            # Define features dictionary
            self.features = {
                'colour': self.extract_unique_values(self.column_mappings['plumage']),
                'size': self.extract_unique_values(self.column_mappings['size']),
                'beak_shape': self.extract_unique_values(self.column_mappings['beak']),
                'habitat': self.extract_unique_values(self.column_mappings['habitat']),
                'behaviour': self.df[self.column_mappings['behavior']].unique().tolist() if self.column_mappings['behavior'] in self.df.columns else []
            }
            
            # Print available features
            # print("\nExtracted features:")
            # for feature_type, values in self.features.items():
            #     print(f"\n{feature_type}: {values}")
            
        except Exception as e:
            print(f"Error initializing BirdIdentificationAssistant: {e}")
            raise

    def extract_unique_values(self, column: str) -> List[str]:
        """Extract unique values from a column that may contain multiple values."""
        values = set()
        if column not in self.df.columns:
            print(f"Warning: Column '{column}' not found. Returning empty list.")
            return []
            
        for entry in self.df[column].dropna():
            if isinstance(entry, str):
                items = [item.strip() for item in entry.split(',')]
                values.update(items)
        return sorted(list(values))

    def match_bird_features(self, user_input: Dict[str, List[str]]) -> List[Tuple[str, float]]:
        """Match bird features to database and return possible matches with confidence scores."""
        matches = []
        
        for idx, bird in self.df.iterrows():
            score = 0
            total_features = 0
            
            # Check each feature category
            if 'colour' in user_input and user_input['colour']:
                total_features += 1
                bird_colors = str(bird[self.column_mappings['plumage']]).split(',')
                score += self._calculate_feature_match(user_input['colour'], bird_colors)
                
            if 'size' in user_input and user_input['size']:
                total_features += 1
                score += 1 if bird[self.column_mappings['size']] in user_input['size'] else 0
                
            if 'habitat' in user_input and user_input['habitat']:
                total_features += 1
                bird_habitats = str(bird[self.column_mappings['habitat']]).split(',')
                score += self._calculate_feature_match(user_input['habitat'], bird_habitats)
            
            if total_features > 0:
                confidence = score / total_features
                if confidence > 0.3:
                    matches.append((bird['Name'], confidence))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_feature_match(self, user_features: List[str], bird_features: List[str]) -> float:
        if not user_features or not bird_features:
            return 0
            
        matches = sum(1 for f in user_features if any(f.lower() in bf.lower() for bf in bird_features))
        return matches / len(user_features)

    def get_bird_details(self, bird_name: str) -> Dict:
        """Get detailed information about a specific bird."""
        try:
            bird_data = self.df[self.df['Name'] == bird_name].iloc[0]
            return {
                'name': bird_name,
                'appearance': bird_data['Appearance'] if 'Appearance' in self.df.columns else 'No appearance information available',
                'behaviour': bird_data[self.column_mappings['behavior']] if self.column_mappings['behavior'] in self.df.columns else 'No behavior information available',
                'habitat': bird_data[self.column_mappings['habitat']] if self.column_mappings['habitat'] in self.df.columns else 'No habitat information available',
                'size': bird_data[self.column_mappings['size']] if self.column_mappings['size'] in self.df.columns else 'No size information available',
                'call': bird_data['Call'] if 'Call' in self.df.columns else 'No call information available',
                'interesting_facts': [
                    bird_data['Fact 1'] if 'Fact 1' in self.df.columns else '',
                    bird_data['Fact 2'] if 'Fact 2' in self.df.columns else '',
                    bird_data['Fact 3'] if 'Fact 3' in self.df.columns else ''
                ]
            }
        except Exception as e:
            print(f"Error getting bird details: {e}")
            return {}

    def process_user_input(self, user_message: str) -> Dict:
        features = {
            'colour': [],
            'size': [],
            'habitat': [],
            'behaviour': []
        }
        
        for colour in self.features['colour']:
            if colour.lower() in user_message.lower():
                features['colour'].append(colour)
                
        for size in self.features['size']:
            if size.lower() in user_message.lower():
                features['size'].append(size)
                
        for habitat in self.features['habitat']:
            if habitat.lower() in user_message.lower():
                features['habitat'].append(habitat)
        
        return features

# In the create_conversation_handler function, let's modify the system prompt:
def create_conversation_handler(api_key: str):
    assistant = AnthropicCalls(
        api_key=api_key,
        system_prompt="""You are Chirpy, an enthusiastic and friendly bird identification assistant with a 
        passion for helping people learn about birds. Your personality traits are:
        - Encouraging and supportive of beginner bird watchers
        - Uses friendly, conversational language
        - Shares interesting facts about birds with excitement
        - Sometimes uses bird-related puns (but not too many!)
        - Always eager to help people learn more about birds
        
        When responding:
        1. Be encouraging of any observation the user shares
        2. If the description is vague, ask specific follow-up questions
        3. Share a fun fact about identified birds
        4. Suggest what to look for next time
        5. If you're not sure about a bird, be honest but supportive
        """
    )

    bird_assistant = BirdIdentificationAssistant('birds.csv')
    
    def handle_conversation(user_input: str) -> str:
        try:
            # Check for basic yes/no response to initial question
            if user_input.lower() in ['yes', 'yeah', 'yep', 'sure', 'yup']:
                return "Wonderful! I love helping fellow bird enthusiasts! Tell me what you observed - any details about colors, size, behavior, or where you spotted it will help me identify your feathered friend!"
            
            if user_input.lower() in ['no', 'nope', 'not yet']:
                return "No worries! When you do spot a bird, I'll be here to help you identify it. Want to learn about what birds you might see in your area?"
            
            features = bird_assistant.process_user_input(user_input)
            matches = bird_assistant.match_bird_features(features)
            
            if matches:
                response = "Oh, how exciting! Based on your description, I think I might know this bird!\n\n"
                for bird, confidence in matches[:3]:
                    bird_details = bird_assistant.get_bird_details(bird)
                    response += f"🦜 {bird} (I'm {confidence:.2%} confident about this one!)\n"
                    response += f"   {bird_details['appearance']}\n\n"
                    
                    # Add a random fact if available
                    facts = [f for f in bird_details['interesting_facts'] if f]
                    if facts:
                        response += f"Fun fact: {np.random.choice(facts)}\n\n"
                
                response += "Would you like to know more about any of these birds? Or did you notice any other features I should know about?"
            else:
                response = "Hmm, I'm not quite sure which bird that might be yet, but let's figure it out together! Could you tell me more about:\n"
                response += "🎨 The bird's colors\n"
                response += "📏 Its size (compared to familiar birds like pigeons or sparrows)\n"
                response += "🏠 Where you saw it (garden, park, woods?)\n"
                response += "🎭 Any interesting behaviors you noticed?"
            
            return response
        except Exception as e:
            print(f"Error in conversation handler: {e}")
            return "Oh dear, something's ruffled my feathers! Could you try describing that again?"
    
    return handle_conversation

if __name__ == "__main__":
    try:
        conversation_handler = create_conversation_handler(ANTHROPIC_API_KEY)
        
        print("\n" + "="*50)
        print("🦜 Chirpy: Hey aspiring twitcher! I'm Chirpy, your friendly bird identification assistant!")
        print("I guess you've spotted a bird. Is that right?")
        print("(Type 'quit' when you're done bird watching)\n")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("\nChirpy: Happy bird watching! Remember, every bird you spot is a new adventure! 🦜")
                break
                
            response = conversation_handler(user_input)
            print("\nChirpy:", response)
    except Exception as e:
        print(f"Error in main execution: {e}")