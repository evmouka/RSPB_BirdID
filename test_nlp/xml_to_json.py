import xmltodict
import json
from typing import Dict, Union
from claude_1 import claude_1

def xml_to_json(claude_output: str) -> Dict:
    
    try:
        if not claude_output or not isinstance(claude_output, str):
            raise ValueError("Invalid input: Expected non-empty string from claude_1")
            
        xml_dict = xmltodict.parse(claude_output)
        json_string = json.dumps(xml_dict)
        return json.loads(json_string)
        
    except Exception as e:
        raise Exception(f"Failed to convert Claude output to JSON: {str(e)}")

def process_claude_response(user_input: str) -> Dict:
    
    claude_response = claude_1(user_input)
    return xml_to_json(claude_response)

