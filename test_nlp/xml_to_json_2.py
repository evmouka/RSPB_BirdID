import xmltodict
import json
from claude_1 import claude_1

def process_bird_sighting():
    """
    Process bird sighting input through claude_1 and convert to JSON
    """
    try:
        # Get Claude's response
        claude_response = claude_1("")
        
        # Convert TextBlock to string
        if hasattr(claude_response, 'text'):
            claude_response = claude_response.text
        elif hasattr(claude_response, '__str__'):
            claude_response = str(claude_response)
            
        # Handle empty or invalid responses
        if not claude_response:
            print("No valid XML received from Claude")
            return
            
        # Convert XML to JSON and print
        xml_dict = xmltodict.parse(claude_response)
        json_string = json.dumps(xml_dict, indent=2)
        print("\nConverted JSON:")
        print(json_string)
        
    except Exception as e:
        print(f"Error processing bird sighting: {str(e)}")
        print("Debug - Response content:", claude_response)

if __name__ == "__main__":
    process_bird_sighting()