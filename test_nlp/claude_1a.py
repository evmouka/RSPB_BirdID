import anthropic
import xmltodict
import json

def claude_1(user_input: str) -> dict:
    client = anthropic.Anthropic()
    
    user_input = input("what have you seen? ")
    
    prompt = f"""Analyze the provided information and identify which characteristics are already mentioned. The key characteristics we're looking for are:
1. plumage_colour
2. beak_colour
3. feet_colour
4. Leg_colour
5. beak_shape
6. tail_shape
7. pattern_markings
8. size
9. habitat

<user_input>
{user_input}
</user_input>

Once you have gathered all the information, output your data in the following format:
<bird_sighting>
    <size>[BIRD SIZE]</size>
    <plumage_colour></plumage_colour>
    <pattern></pattern>
    <beak_shape_1></beak_shape>
    <beak_colour_1></beak_colour>
</bird_sighting> 

refinements:
if input mentions tiny size output <size>extra small</size>

only output only the XML dict nothing else
In the XML dict only include the fields you have data for
if you have no relavant data for a field do not include it in the XML dict
if the input is irrelevant to bird identification output an empty XML dict
if the input includes a bird identification attribute that is not inluded in the characteristisc already mentioned output a dict with a ner entry tageged as <new_attribute>
the values for this output should be taken from this JSON:

    "size": "medium, extra small, large, small",
    "plumage_colour": "orange, blue, cream/buff, brown, pink, buff, cream, yellow, grey, purple, white, green, pale brown, brown, beige, black, red",
    "beak_colour": "orange, yellow, grey, white, brown, black",
    "feet_colour": "blue, pink, grey, brown, black, red",
    "leg_colour": "pink, grey, brown, black, red",
    "beak_shape_1": "sharp, thick, narrow, short, curved, thin, hooked, long, pointed, stubby",
    "tail_shape_1": "double, thin, fan, fanned in flight, square, long, pointed, forked",
    "pattern": "black, yellow, bright yellow breast, green, white cheeks, black cap, red, black neck collar, blue, red brest, dark brown, sooty black. yellow bill, brown back, white, green gloss to the tail, black plumage, orange brest, darker wings and tail, speckles, green back, yellow eye ring, black stripe, purplish-blue iridescent sheen to the wing feathers",
    "habitat": "grassland, city, hedgerow, heathland, meadow, suburban, wetland, farmland, woodland, town, garden, park, urban, upland"
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        messages=[{
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        }]
    )
    
    xml_string = message.content[0].text if isinstance(message.content, list) else message.content.text
    xml_dict = xmltodict.parse(xml_string)
    json_dict = json.loads(json.dumps(xml_dict))
    
    # Print for verification
    print("\nJSON Output:")
    print(json.dumps(json_dict, indent=2))
    
    return json_dict

if __name__ == "__main__":
    result = claude_1("")
    
