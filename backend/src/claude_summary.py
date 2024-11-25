import anthropic

def claude_summary(cat: dict) -> str:
    client = anthropic.Anthropic()
    if 'new_attribute' in cat:
        del cat['new_attribute']
    prompt = f"""
    Your task is to transform technical data into a friendly, informative description. Use variety in your descriptions. Use different adjectives to describe key features. Be vreative.

    Here's the bird data you need to summarize in JSON format:
    {cat}

    Please follow these steps to create your summary:
    1. Carefully read and parse the JSON data provided.
    2. Consider how to make the description engaging and conversational.
    3. Create a summary based on your analysis, adhering to these rules:
   - Use the exact words from the JSON values, wrapping them in <> tags.
   - Craft a conversational and varied paragraph structure.
   - Incorporate engaging descriptors and maintain a friendly tone.
   - Ensure the summary flows naturally and is pleasant to read aloud.

    Your final output should be a single paragraph without any additional text or explanations.

    Example output structure 1 (using generic terms):
    This delightful <size> bird boasts a stunning plumage of <color1>, <color2>, and <color3>. Its most striking feature is its <pattern> pattern, which <interesting fact about the pattern>. You're most likely to spot this feathered friend in <habitat> areas, where it <typical behavior>.
    
    Example structure 2 using more creative terms:
    This charming <extra small> songbird catches the eye with its graceful <long> <black> beak, perfect for probing delicate blossoms. Its feathers showcase a beautiful blend of <pink, brown> hues, creating a subtle yet striking appearance that sets it apart from its forest companions. Adding to its elegant profile is a sweeping <long> tail that trails behind as it flits through the branches. Listen closely for its <cheerful> calls that ring through the air like tiny bells, bringing life and joy to its surroundings.

    Remember, this is just an example structure. Feel free to be creative in your composition while maintaining accuracy and using the provided data.
    Vary your description each time.
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