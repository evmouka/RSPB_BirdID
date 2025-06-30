import xmltodict
import json
from typing import Dict, Union
from claude_1 import claude_1

def xml_to_json(claude_output: str) -> None:
    """
    Convert Claude's XML output to JSON dictionary and print it
    
    Args:
        claude_output (str): Output from claude_1 function
    """
    try:
        if not claude_output or not isinstance(claude_output, str):
            raise ValueError("Invalid input: Expected non-empty string from claude_1")
            
        xml_dict = xmltodict.parse(claude_output)
        json_string = json.dumps(xml_dict, indent=2)
        print(json_string)
        
    except Exception as e:
        print(f"Failed to convert Claude output to JSON: {str(e)}")

def process_claude_response(user_input: str) -> None:
    """
    Process user input through claude_1 and print JSON result
    
    Args:
        user_input (str): Input for claude_1 function
    """
    claude_response = claude_1(user_input)
    xml_to_json(claude_response)

# Call the function with your input
process_claude_response("your question or prompt here")