import anthropic
import xmltodict
import json
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def claude_1(user_input: str) -> dict:
    client = anthropic.Anthropic()
    
    prompt = f"""Analyze the provided information and identify which characteristics are already mentioned.

<user_input>
{user_input}
</user_input>

Once you have gathered all the information, output your data in the following format:
<bird_sighting>
    <Size>[BIRD SIZE]</Size>
    <Plumage_colour></Plumage_colour>
    <pattern></pattern>
    <beak_shape></beak_shape>
    <beak_colour></beak_colour>
</bird_sighting> 

only output only the XML dict nothing else
In the XML dict only include the fields you have data for
if you have no relavant data for a field do not include it in the XML dict
if the input is irrelevant to bird identification output an empty XML dict
if the input includes a bird identification attribute that is not included in the characteristisc already mentioned output a dict with a ner entry tageged as <new_attribute>
the values for this output should be taken from this JSON:

    "Plumage colour(s)": "orange, blue, cream/buff, Brown, pink, buff, cream, yellow, grey, purple, white, green, pale brown, beige, black, red",
    "Beak Colour(s)": "orange, yellow, grey, white, brown, black",
    "Feet colour(s)": "blue, pink, grey, brown, black, red",
    "Leg colour(s)": "pink, grey, brown, black, red",
    "Beak Shape 1": "sharp, thick, narrow, short, curved, thin, hooked, long, pointed, stubby",
    "Beak shape 2 (optional)": "sharp, thick, short, curved, long, pointed, stubby",
    "Tail shape 1": "double, thin, fan, fanned in flight, square, long, pointed, forked",
    "Pattern/ Markings": "black, yellow, bright yellow breast, green, white cheeks, black cap, red, black neck collar, blue, red brest, dark brown, sooty black. yellow bill, brown back, white, green gloss to the tail, black plumage, orange brest, darker wings and tail, speckles, green back, yellow eye ring, black stripe, purplish-blue iridescent sheen to the wing feathers",
    "Size": "medium, Extra small, large, small",
    "Habitat(s)": "grassland, city, hedgerow, heathland, meadow, suburban, wetland, farmland, woodland, town, garden, park, urban, upland"
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
    
    return json_dict
    