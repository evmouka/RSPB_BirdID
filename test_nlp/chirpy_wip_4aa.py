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
    def __init__(self, xml_file: str):
        """Initialize with bird database"""
        self.df = pd.read_xml(
            xml_file,
            xpath=".//bird",  # Select all bird elements
            parser='etree',   # Use etree parser for better handling of nested elements
            encoding='utf-8'
        )
        self.df = self.df.fillna('')
        print("Bird database loaded successfully")

def main():
    # Initialize the bird identification system
    system_prompt = """You are a friendly UK ornithologist specialisingteaching others how to identify birds. 
    Your goal is to help users identify birds they have spotted through a casual, engaging conversation. 
    Always maintain a positive and enthusiastic tone. 
    Use only knowledhe from the <BIRD_DATA> extensive knowledge of birds to provide accurate identifications based on the information gathered from the user."""
    
    prompt = """CRITICAL RULES:
    1. Begin by internalizing the system prompt.
    2. Now, familiarize yourself with the main prompt that outlines your goals and guidelines:
    3. You have access to a database of bird information. Use ONLY this data to help identify birds based on the features described by the user:
    <bird_data>
    bird_data.xml
    </bird_data>

    4. Engage in a conversation with the user to gather information about the bird they've spotted. Follow these guidelines:
    - Start by asking if they've spotted a bird
    - Ask about one feature at a time, in a conversational way
    - Use appropriate emojis to make the conversation more engaging
    - Focus on key features in this order: plumage colour(s), pattern/markings, size, beak shape, beak colour(s), tail shape, feet colour(s), feet length
    - Acknowledge attributes the user mentions and ask follow-up questions if necessary
    - Don't repeat questions or ask about the same feature
    - If you get vague input, ask clarifying questions
    - If they don't know or are unsure about an attribute, ask one more question to help them, but only once
    - Keep track of the features already mentioned

    5. As you gather information, keep a mental tally of the features you've learned.
    list the features gathered by the user in a simple list, with one feature per line.
    When you have collected data for 5 categories, create a XML dictionary with the gathered information. 
    - The categories should correspond exactly to those in the bird_data.xml file. 
    - example 1:if you ask them about the size of the bird and they say "tiny", or "minute", you can use the " very small" category in the XML dictionary.
    - example 2: if they say they don't know or was not clear, say you will skit that part and move on to another category
    - only output the XML dictionary, no other text
    Before outputting the dictionary, check for null entries and ask questions to get any missing information. 
    6. After outputting the XML dictionary, if the user asks for identification, use the information gathered to identify the bird. Include the corresponding image from the bird_data.xml file in your response, showing the image of the bird you identified.

    Remember to maintain a friendly, enthusiastic tone throughout the conversation. You're having a natural conversation, not conducting an interrogation. Be excited about their bird sighting!"""

    bird_assistant = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY,
        system_prompt=system_prompt,
        prompt=prompt,
        stream=True
    )
    
    bird_db = BirdIdentifier('bird_data.xml')
    
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