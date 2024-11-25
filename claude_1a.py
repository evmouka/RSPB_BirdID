import anthropic
import xmltodict
from dict2xml import dict2xml
import json

def claude_1(user_input: str, category_prompt: str, all_words: dict) -> dict:
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
{dict2xml(all_words)}

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
        bird_features = json.loads(json.dumps(xml_dict))
        bird_features =  bird_features["bird_sighting"]
        if not bird_features:
            bird_features = {}
    except:
        return {"bird_sighting": {}}
    
    return bird_features
    