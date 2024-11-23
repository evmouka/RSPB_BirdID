import anthropic

def claude_summary(cat: dict) -> str:
    client = anthropic.Anthropic()
    
    prompt = f"""
    I have some bird characteristic in form of json. I want you to make a nice summary of the current description. 
    Here is the json:
    {cat}

    follow these rules:
    -Give me only the summary without any other text
    -use the exact words used in the json but make the rest nice and custom
    -wrap every word that are used in the value of the json with <>

    here is an example:
JSON input:
[
  "bird_sighting": [
    "size": "small",
    "plumage_colour": "orange, pink, grey, black, white",
    "pattern_markings": "black stripe",
    "habitat": "woodland"
  ]
]
would give this output:
This bird is <small> in size, with a plumage of <orange>, <pink>, <grey>, <black>, and <white> colors. It has a <black stripe> marking. It typically inhabits <woodland> areas.
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
    
    string = message.content[0].text if isinstance(message.content, list) else message.content.text
    return string