import anthropic
import xmltodict
import json

def claude_1(user_input: str, category_prompt: str) -> dict:
    client = anthropic.Anthropic()
    category = ""
    if category_prompt:
        category = f"The user_input is an anwser to a question asking description for this category : {category_prompt}. Consider it strongly in your classification but still make sure it is relevant and matching one of the words"
    
    prompt = f"""You are a specialist in interpretation and a bird expert. Your job is to take a bird description and to interpret it and classify it in different categories in our specific wording.

Here is the user input:
<user_input>
{user_input}
</user_input>

{category}
Output your interpretation in the following format:
<bird_sighting>
    <size>[BIRD SIZE]</size>
    <plumage_colour></plumage_colour>
    <pattern></pattern>
    <beak_shape_1></beak_shape>
    <beak_colour></beak_colour>
    <leg_colour></leg_colour>
    <habitat></habitat>
    <pattern_markings></pattern_markings>
    <tail_shape_1></tail_shape_1>
    <feet_colour></feet_colour>
</bird_sighting>

the values to fill the XML should exclusively be taken from this JSON:
[
    "size": "medium, extra small, large, small",
    "plumage_colour": "orange, blue, cream/buff, brown, pink, buff, cream, yellow, grey, purple, white, green, pale brown, brown, beige, black, red",
    "beak_colour": "orange, yellow, grey, white, brown, black",
    "feet_colour": "blue, pink, grey, brown, black, red",
    "leg_colour": "pink, grey, brown, black, red",
    "beak_shape_1": "sharp, thick, narrow, short, curved, thin, hooked, long, pointed, stubby",
    "tail_shape_1": "double, thin, fan, fanned in flight, square, long, pointed, forked",
    "pattern_markings": "black, yellow, bright yellow breast, green, white cheeks, black cap, red, black neck collar, blue, red brest, dark brown, sooty black. yellow bill, brown back, white, green gloss to the tail, black plumage, orange brest, darker wings and tail, speckles, green back, yellow eye ring, black stripe, purplish-blue iridescent sheen to the wing feathers",
    "habitat": "grassland, city, hedgerow, heathland, meadow, suburban, wetland, farmland, woodland, town, garden, park, urban, upland"
]

Here are some important rules to follow:
-only output in the XML format and nothing else than the XML
-In the XML dict only include the fields you have data for
-if you have no relavant data for a field do not include it in the XML dict
-if the input is irrelevant to bird identification dont output it in the XML
-if the XML is empty just output an empty XML
This is a very important rule:
-If the input or part of it dont match with any categories nor adjective but is relevant to bird identification add a dict with a new entry tagged as <new_attribute> with your interpretation of this new characteristic

Here are some examples:
user input: it was in my garden and singing super loudly and was quite fast
the output:
<bird_sighting>
    <habitat>garden</habitat>
    <new_attribute>
        <flight_speed>fast<flight_speed>
        <call>loud</call>
    </new_attribute>
</bird_sighting>

user input: A small bird with a bright yellow chest, brown wings, and a short black beak. It has a long tail and sings a cheerful melody. I also like to play tennis.
the output:
<bird_sighting>
    <size>small</size>
    <beak_shape_1>short</beak_shape_1>
    <beak_color>black</beak_color>
    <plumage_color>yellow, brown</plumage_color>
    <tail_shape_1>long</tail_shape_1>
    <new_attribute>
        <call>cheerfull</call>
    </new_attribute>
</bird_sighting>
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
    try:
        xml_dict = xmltodict.parse(xml_string)
        json_dict = json.loads(json.dumps(xml_dict))
    except:
        return {"bird_sighting": {}}
    
    return json_dict
    