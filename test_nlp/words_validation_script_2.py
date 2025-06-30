import json
from typing import Dict, Set

def load_allowed_values(words_json: Dict) -> Dict[str, Set[str]]:
    return {k.lower(): set(v.split(", ")) for k, v in words_json.items()}

def validate_bird_sighting(output: Dict) -> Dict[str, bool]:
    validation = {
        "size": "medium, extra small, large, small",
        "plumage_colour": "orange, blue, cream/buff, brown, pink, buff, cream, yellow, grey, purple, white, green, pale brown, brown, beige, black, red",
        "beak_colour": "orange, yellow, grey, white, brown, black",
        "feet_colour": "blue, pink, grey, brown, black, red",
        "leg_colour": "pink, grey, brown, black, red",
        "beak_shape": "sharp, thick, narrow, short, curved, thin, hooked, long, pointed, stubby",
        "tail_shape": "double, thin, fan, fanned in flight, square, long, pointed, forked",
        "pattern": "black, yellow, bright yellow breast, green, white cheeks, black cap, red, black neck collar, blue, red brest, dark brown, sooty black. yellow bill, brown back, white, green gloss to the tail, black plumage, orange brest, darker wings and tail, speckles, green back, yellow eye ring, black stripe, purplish-blue iridescent sheen to the wing feathers",
        "habitat": "grassland, city, hedgerow, heathland, meadow, suburban, wetland, farmland, woodland, town, garden, park, urban, upland"
    }
    
    results = {}
    
    if not output.get("bird_sighting"):
        return {"error": False, "message": "No bird_sighting found in output"}
        
    for field, value in output["bird_sighting"].items():
        if field == "new_attribute" or value == "null":
            results[field] = True
            continue
            
        if field in validation:
            # Clean and split the validation string into a set
            valid_values = {v.strip().lower() for v in validation[field].split(",")}
            # Check if the lowercase value is in our valid values
            results[field] = value.lower() in valid_values
        else:
            results[field] = False
            
    return results

def main():
    # Test the output from claude_1a
    from claude_1a import claude_1
    test_output = claude_1("I saw a small bird")
    
    # Validate the output
    results = validate_bird_sighting(test_output)
    
    # Print results
    print("\nValidation Results:")
    for field, is_valid in results.items():
        print(f"{field}: {'✓' if is_valid else '✗'}")

if __name__ == "__main__":
    main()