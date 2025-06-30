import xmltodict
import json
from claude_1 import claude_1

def convert_bird_sighting():
    """
    Gets bird sighting from claude_1 and converts XML output to JSON
    """
    try:
        # Get response from claude_1
        response = claude_1()
        
        # Convert TextBlock to string if needed
        if hasattr(response, 'text'):
            response = response.text
        
        # Parse XML to dict then convert to JSON
        xml_dict = xmltodict.parse(response)
        json_string = json.dumps(xml_dict, indent=2)
        
        # Print the JSON
        print("\nJSON Output:")
        print(json_string)
        
    except Exception as e:
        print(f"Error converting bird sighting: {str(e)}")
        print("Raw response:", response)

if __name__ == "__main__":
    convert_bird_sighting()
