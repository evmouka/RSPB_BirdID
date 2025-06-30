import os
import pandas as pd
from dotenv import load_dotenv
import anthropic

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
    def __init__(self, csv_file: str):
        """Initialize with bird database"""
        self.df = pd.read_csv(csv_file, skiprows=1)
        self.df = self.df.fillna('')
        print("Bird database loaded successfully")

    def gather_attributes(self, user_input: str) -> dict:
        """
        Gather bird attributes from user input and return a dictionary.
        
        Parameters:
        user_input (str): The user's description of the bird.
        
        Returns:
        dict: A dictionary containing the gathered attributes.
        """
        attributes = {
            "colors_and_markings": "",
            "size": "",
            "beak_shape_and_color": "",
            "tail_shape": "",
            "leg_color_and_length": ""
        }

        # Initialize the conversation
        print("\nChirpy: Okay, let's start identifying the bird you saw!")
        print("I'll ask you some questions about the bird's features, and we'll see if we can figure out what it is.")

        # Ask for colors and markings
        print("\nChirpy: First, what colors and markings did you notice on the bird?")
        attributes["colors_and_markings"] = input("You: ")

        # Ask for size
        print("\nChirpy: Great, now how would you describe the bird's size compared to a common bird like a sparrow or pigeon?")
        attributes["size"] = input("You: ")

        # Ask for beak shape and color
        print("\nChirpy: Okay, what about the bird's beak - what shape and color was it?")
        attributes["beak_shape_and_color"] = input("You: ")

        # Ask for tail shape
        print("\nChirpy: Now, can you tell me about the shape of the bird's tail?")
        attributes["tail_shape"] = input("You: ")

        # Ask for leg color and length
        print("\nChirpy: Finally, what color were the bird's legs, and how long were they?")
        attributes["leg_color_and_length"] = input("You: ")

        print("\nChirpy: Okay, let me review what we know so far:")
        for k, v in attributes.items():
            print(f"- {k.capitalize()}: {v}")

        return attributes

def main():
    system_prompt = """You are Chirpy, an enthusiastic bird expert helping identify UK garden birds. Your goal is to:
    1. Have a natural conversation to gather key identifying features about birds
    2. Always ask about one feature at a time, in a conversational way
    3. Keep track of what you've learned about the bird
    4. Focus on these key features in this order:
       - Colors and markings
       - Size (compared to common birds like sparrows or pigeons)
       - Beak shape and color
       - Tail shape
       - Leg color and length
    5. Provide the gathered attributes in a dictionary
    6. If you are unsure how to map a user's response to a specific attribute, ask for clarification
    7. Provide educational information about bird identification as needed
    """

    bird_assistant = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY,
        system_prompt=system_prompt,
        stream=True
    )
    
    bird_db = BirdIdentifier('birds.csv')
    
    print("\nChirpy: Hey there! I'm Chirpy, the bird identification expert. Let's work together to identify the bird you saw!")
    print("Whenever you're ready, describe the bird and I'll guide you through the process.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nChirpy: Happy birding! Come back when you spot another interesting bird! 🦜")
            break
            
        attributes = bird_db.gather_attributes(user_input)

        # Implement your bird identification algorithm using the gathered attributes
        # For now, just print the attributes
        print("\nChirpy: Based on the information you provided, here's what we know about the bird:")
        for k, v in attributes.items():
            print(f"- {k.capitalize()}: {v}")

if __name__ == "__main__":
    main()