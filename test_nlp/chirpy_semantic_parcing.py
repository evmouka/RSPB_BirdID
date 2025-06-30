import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os
import anthropic
import json

class SemanticParser:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Define our knowledge base categories and valid values
        self.feature_schema = {
            "plumage_colors": {
                "description": "Colors of the bird's feathers",
                "type": "list",
                "valid_values": ["brown", "grey", "black", "white", "blue", "red", "yellow", "green", "orange", "purple", "pink"]
            },
            "size": {
                "description": "Overall size of the bird",
                "type": "string",
                "valid_values": ["extra small", "small", "medium", "large", "extra large"]
            },
            "beak_shape": {
                "description": "Shape of the bird's beak",
                "type": "string",
                "valid_values": ["short and stubby", "long and thin", "hooked", "pointed", "curved"]
            },
            "beak_color": {
                "description": "Color of the bird's beak",
                "type": "string",
                "valid_values": ["black", "yellow", "orange", "red", "grey", "brown"]
            },
            "leg_length": {
                "description": "Length of the bird's legs",
                "type": "string",
                "valid_values": ["short", "medium", "long"]
            },
            "leg_color": {
                "description": "Color of the bird's legs",
                "type": "string",
                "valid_values": ["pink", "yellow", "black", "grey", "brown", "orange"]
            },
            "tail_shape": {
                "description": "Shape of the bird's tail",
                "type": "string",
                "valid_values": ["forked", "pointed", "rounded", "square", "fan-shaped"]
            },
            "patterns": {
                "description": "Notable patterns or markings",
                "type": "list",
                "valid_values": ["spotted", "striped", "speckled", "solid", "mottled", "barred"]
            },
            "location": {
                "description": "Where the bird was seen",
                "type": "list",
                "valid_values": ["garden", "woodland", "urban", "farmland", "wetland", "coastal", "park"]
            }
        }

    def parse_input(self, user_input: str) -> Dict[str, any]:
        """
        Parse user input into structured features matching our knowledge base categories
        """
        prompt = f"""Extract bird features from this description: "{user_input}"

        Return a JSON object with features matching these categories:
        {json.dumps(self.feature_schema, indent=2)}

        Rules:
        1. Only include features that are explicitly mentioned or can be directly inferred
        2. Map descriptions to the closest valid value in each category
        3. Include confidence level (0-1) for each extracted feature
        4. Provide reasoning for each extraction

        Format:
        {{
            "extracted_features": {{
                "feature_name": {{
                    "value": "extracted_value",
                    "confidence": 0.8,
                    "reasoning": "explanation"
                }}
            }},
            "missing_features": ["list of important missing features"],
            "clarification_needed": ["any ambiguous features that need clarification"]
        }}
        """

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            parsed_result = json.loads(response.content[0].text)
            return self.validate_parsed_features(parsed_result)
        except Exception as e:
            print(f"Error in parsing: {e}")
            return {}

    def validate_parsed_features(self, parsed_result: Dict) -> Dict:
        """Validate extracted features against our schema"""
        validated = {
            "extracted_features": {},
            "missing_features": parsed_result.get("missing_features", []),
            "clarification_needed": parsed_result.get("clarification_needed", [])
        }

        for feature, data in parsed_result.get("extracted_features", {}).items():
            if feature in self.feature_schema:
                schema = self.feature_schema[feature]
                
                # Validate value against valid values
                if schema["type"] == "list":
                    valid_values = [v for v in data["value"] if v.lower() in schema["valid_values"]]
                    if valid_values:
                        data["value"] = valid_values
                        validated["extracted_features"][feature] = data
                else:
                    if data["value"].lower() in schema["valid_values"]:
                        validated["extracted_features"][feature] = data

        return validated

    def get_missing_key_features(self, parsed_features: Dict) -> List[str]:
        """Identify important missing features for identification"""
        key_features = ["plumage_colors", "size", "beak_shape"]
        extracted = set(parsed_features.get("extracted_features", {}).keys())
        return [f for f in key_features if f not in extracted]

class BirdMatcher:
    def __init__(self, parser: SemanticParser, csv_file: str):
        self.parser = parser
        self.df = pd.read_csv(csv_file, skiprows=1)
        self.df = self.df.fillna('')

    def process_description(self, description: str) -> Dict:
        """Process user description and return structured analysis"""
        # Parse the input
        parsed_features = self.parser.parse_input(description)
        
        # Check if we have enough information
        missing_features = self.parser.get_missing_key_features(parsed_features)
        
        return {
            "parsed_features": parsed_features["extracted_features"],
            "missing_features": missing_features,
            "clarification_needed": parsed_features["clarification_needed"],
            "confidence": self.calculate_parsing_confidence(parsed_features)
        }

    def calculate_parsing_confidence(self, parsed_features: Dict) -> float:
        """Calculate overall confidence in the parsing"""
        if not parsed_features.get("extracted_features"):
            return 0.0
            
        confidences = [data["confidence"] 
                      for data in parsed_features["extracted_features"].values()]
        return sum(confidences) / len(confidences)

def main():
    # Initialize
    load_dotenv()
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    parser = SemanticParser(ANTHROPIC_API_KEY)
    matcher = BirdMatcher(parser, 'bird_data.json')
    
    print("\nChirpy: Hello! Tell me about the bird you saw!")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        # Process the description
        result = matcher.process_description(user_input)
        
        # Display results
        print("\nParsed Features:")
        for feature, data in result["parsed_features"].items():
            print(f"\n{feature}:")
            print(f"  Value: {data['value']}")
            print(f"  Confidence: {data['confidence']:.2f}")
            print(f"  Reasoning: {data['reasoning']}")
            
        if result["missing_features"]:
            print("\nMissing important features:", result["missing_features"])
            
        if result["clarification_needed"]:
            print("\nNeeds clarification:", result["clarification_needed"])
            
        print(f"\nOverall parsing confidence: {result['confidence']:.2f}")

if __name__ == "__main__":
    main()