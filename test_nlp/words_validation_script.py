import json
from typing import Dict, Set

def load_allowed_values(words_json: Dict) -> Dict[str, Set[str]]:
    return {k.lower(): set(v.split(", ")) for k, v in words_json.items()}

def validate_bird_sighting(output: Dict) -> bool:
    validation = {
        "size": "medium, extra small, large, small",
        "plumage_colour": "orange, blue, cream/buff, brown, pink, buff, cream, yellow, grey, purple, white, green, pale brown, brown, beige, black, red",
        "beak_colour": "orange, yellow, grey, white, brown, black",
        "feet_colour": "blue, pink, grey, brown, black, red",
        "leg_colour": "pink, grey, brown, black, red",
        "beak_shape_1": "sharp, thick, narrow, short, curved, thin, hooked, long, pointed, stubby",
        "tail_shape_1": "double, thin, fan, fanned in flight, square, long, pointed, forked",
        "pattern": "black, yellow, bright yellow breast, green, white cheeks, black cap, red, black neck collar, blue, red brest, dark brown, sooty black. yellow bill, brown back, white, green gloss to the tail, black plumage, orange brest, darker wings and tail, speckles, green back, yellow eye ring, black stripe, purplish-blue iridescent sheen to the wing feathers",
        "habitat": "grassland, city, hedgerow, heathland, meadow, suburban, wetland, farmland, woodland, town, garden, park, urban, upland"
    }
    if not output.get("bird_sighting"):
        return True
    for keys, value in output["bird_sighting"].items():
        if keys == "new_attribute":
            continue
        if keys in list(validation.keys()) and value in validation[keys].split(", "):
            continue
        return False
    return True

def main():
    # Load words.json
    # with open('words.json', 'r') as f:
    #     allowed_values = load_allowed_values(json.load(f))
    
    # Test the output from claude_1a
    from claude_1a import claude_1
    test_output = claude_1("The bird has orange plumage and a sharp beak")
    
    # Validate the output
    results = validate_bird_sighting(test_output)
    
    # Print results
    print("\nResults:")
    print(results)
    # for field, is_valid in results.items():
    #     print(f"{field}: {'✓' if is_valid else '✗'}")

if __name__ == "__main__":
    main()