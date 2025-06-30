import os
import json
from dotenv import load_dotenv
from collections import defaultdict

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Load the bird information from the JSON file
with open("bird_data.json", "r") as f:
    bird_data = json.load(f)

def process_user_input(user_input):
    """
    Process the user's natural language input and map it to the corresponding categories in the bird data.
    
    Parameters:
    user_input (str): The user's natural language input.
    
    Returns:
    dict or None: A dictionary containing the processed information, with keys matching the categories in the bird data, if at least 5 categories can be confidently matched. Otherwise, returns None.
    """
    # Convert the user input to lowercase for case-insensitive matching
    user_input = user_input.lower()
    
    # Create a dictionary to store the matching scores for each category
    category_scores = defaultdict(int)
    
    # Iterate through the bird data and check if the user input matches any of the category values
    for bird in bird_data:
        for category, value in bird.items():
            if isinstance(value, str) and value.lower() in user_input:
                category_scores[category] += 1
    
    # Check if at least 5 categories can be confidently matched
    if sum(category_scores.values()) >= 5:
        # Create the output dictionary with the matched categories
        output = {category: bird_data[0][category] for category in category_scores if category_scores[category] > 0}
        return output
    else:
        return None

def start_conversation():
    print("Welcome to Chirpy, the bird identification bot!")
    print("Please describe the bird you saw, and I'll do my best to identify it.")

    while True:
        user_input = input("Your description: ")
        result = process_user_input(user_input)
        
        if result:
            print("Based on your description, it sounds like you saw a:")
            for category, value in result.items():
                print(f"- {category.capitalize()}: {value}")
            break
        else:
            print("Sorry, I couldn't confidently identify the bird from your description.")
            print("Please try providing more details about the bird's appearance, behavior, or location.")

if __name__ == "__main__":
    start_conversation()