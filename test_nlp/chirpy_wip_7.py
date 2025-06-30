
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os
import anthropic
import json
import voyageai
from sklearn.metrics.pairwise import cosine_similarity

class BirdKnowledgeBase:
    def __init__(self, json_file: str, voyage_api_key: str):
        """Initialize the bird knowledge base with Voyage AI client"""
        self.df = pd.read_json(json_file)
        self.df = self.df.fillna('')
        self.voyage_client = voyageai.Client(api_key=voyage_api_key)
        
        # Define feature mappings
        self.feature_mappings = {
            "color": ["Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)"],
            "size": ["Size", "Min Length (cm)", "Max Length (cm)", "Wingspan (cm)", "Weight (g)"],
            "shape": ["Beak Shape 1", "Beak shape 2 (optional)", "Tail shape 1", "Tail shape 2 (optional)"],
            "pattern": ["Pattern/ Markings"],
            "habitat": ["Habitat(s)", "Where to see them (countries)"],
            "sound": ["Call"],
            "behavior": ["Behaviour"],
            "name": ["Name", "Alt names/ mispellings", "Latin name"],
            "appearance": ["Appearance"]
        }
        
        try:
            # Generate embeddings for database
            print("Generating embeddings...")
            self.embeddings = self.generate_embeddings()
            print("Bird database and embeddings loaded successfully")
        except Exception as e:
            print(f"Error during initialization: {e}")
            self.embeddings = {}

def generate_embeddings(self) -> Dict[str, np.ndarray]:
        """Generate embeddings for searchable content"""
        embeddings = {}
        try:
            # Generate embeddings for descriptions
            descriptions = []
            embed_results = []
            
            print("Processing bird descriptions...")
            for _, row in self.df.iterrows():
                desc = f"{row['Appearance']} {row['Pattern/ Markings']} {row['Plumage colour(s)']}"
                desc = desc.strip()
                if desc:  # Only process non-empty descriptions
                    try:
                        # Updated Voyage AI embed syntax
                        embed_result = self.voyage_client.embed([desc])  # Changed to use list syntax
                        embed_results.append(embed_result[0])  # Take first result
                    except Exception as e:
                        print(f"Error embedding description: {e}")
                        embed_results.append(np.zeros(1024))  # Fallback embedding
            
            if embed_results:
                embeddings['descriptions'] = np.array(embed_results)
            else:
                print("Warning: No embeddings generated")
                embeddings['descriptions'] = np.array([])
                
        except Exception as e:
            print(f"Error in generate_embeddings: {e}")
            embeddings['descriptions'] = np.array([])
            
        return embeddings

def search_birds(self, query: str, top_k: int = 3) -> List[Dict]:
    """Search for birds using embedding similarity"""
    try:
        if not self.embeddings.get('descriptions', []).size:
            print("No embeddings available for search")
            return []

        # Get query embedding with updated syntax
        query_embedding = self.voyage_client.embed([query])[0]
        
        # Calculate similarities
        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings['descriptions']
        )[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            bird_data = self.df.iloc[idx].to_dict()
            bird_data['similarity_score'] = float(similarities[idx])
            results.append(bird_data)
            
        return results
        
    except Exception as e:
        print(f"Error in search: {e}")
        return []

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

# System prompt
SYSTEM_PROMPT = """You are Chirpy, an enthusiastic bird expert helping identify UK garden birds. Your goal is to:
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
- Keep track of the features already mentioned"""

def setup_clients():
    """Setup API clients"""
    load_dotenv()
    
    api_keys = {
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'voyage': os.getenv('VOYAGE_API_KEY')
    }
    
    if not all(api_keys.values()):
        missing = [k for k, v in api_keys.items() if not v]
        raise ValueError(f"Missing API keys: {', '.join(missing)}")
        
    return api_keys

def main():
    try:
        # Setup API clients
        api_keys = setup_clients()
        
        # Initialize knowledge base with embeddings
        kb = BirdKnowledgeBase('bird_data.json', api_keys['voyage'])
        
        # Initialize bird assistant
        bird_assistant = AnthropicCalls(
            api_key=api_keys['anthropic'],
            system_prompt=SYSTEM_PROMPT,
            stream=True,
            bird_identifier=kb
        )
        
        print("\nChirpy: Hey there! I'm Chirpy, let's try and identify the bird you spotted! 🦜")
        print("Tell me something about the bird you saw or type 'quit' to exit.")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'quit':
                break
                
            response = bird_assistant.chat(user_input)
            if response:
                print(f"\nChirpy: {response.content[0].text}")
            else:
                print("\nChirpy: I encountered an error. Could you please try again?")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()