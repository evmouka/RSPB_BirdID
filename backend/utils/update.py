import json
import re

def clarify_database(data):
    clarified_data = []
    for entry in data:
        clarified_entry = {}
        for key, value in entry.items():
            # Replace spaces with underscores in the key
            new_key = key.replace(" ", "_")
            # Remove everything in parentheses and the parentheses themselves
            new_key = re.sub(r'\(.*?\)', '', new_key)
            # Remove all '/'
            new_key = new_key.replace("/", "")
            # Remove trailing underscores if any
            new_key = new_key.rstrip("_").lower()

            # Process the value: lowercase everything
            if(type(value) == str):
                new_value = value.lower()
            else:
                new_value = value

            # Add to the clarified entry
            clarified_entry[new_key] = new_value

        clarified_data.append(clarified_entry)

    return clarified_data

# Load data from JSON file
with open('bird_data.json', 'r') as file:
    data = json.load(file)

# Clarify the data
clarified_data = clarify_database(data)

# Write the clarified data to a new JSON file
with open('new_bird.json', 'w') as file:
    json.dump(clarified_data, file, indent=4)

print("Data transformation complete. Output saved to 'output_data.json'.")
