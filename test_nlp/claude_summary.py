import anthropic

def claude_summary(cat: dict) -> str:
    client = anthropic.Anthropic()
    
    prompt = f"""
    You are an enthusiastic ornithologist tasked with creating engaging and conversational summaries of bird characteristics. Your goal is to transform technical data into a an articulate and eloquent yet succinct summary. Don't overdo it. Keep it simple and engaging.

    Here's the bird data you need to summarize in JSON format:
    {cat}

    Please follow these steps to create your summary:
    1. Carefully read and parse the JSON data provided.
    2. In <analysis> tags:
    a. List out all the key characteristics from the JSON data.
    b. For each characteristic, brainstorm engaging descriptors and conversational phrases.
    c. Draft a rough outline of the summary, ensuring all key points are covered in a logical flow.
    d. Consider how to make the description engaging and conversational.
    3. Create a final summary based on your analysis, adhering to these rules:
   - Use the exact words from the JSON values, wrapping them in <> tags.
   - Craft a conversational and varied paragraph structure.
   - Incorporate engaging descriptors and maintain a friendly tone.
   - Ensure the summary flows naturally and is pleasant to read aloud.

    Your final output should be a single paragraph without any additional text or explanations.

    Example output structure (using generic terms):
    This delightful <size> bird boasts a stunning plumage of <color1>, <color2>, and <color3>. Its most striking feature is its <pattern> pattern, which <interesting fact about the pattern>. You're most likely to spot this feathered friend in <habitat> areas, where it <typical behavior>.

    Remember, this is just an example structure. Feel free to be creative in your composition while maintaining accuracy and using the provided data. Vary your sentence structure and word choice to keep the summary engaging and informative.
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

if __name__ == "__main__":
    # Example JSON data for bird characteristics
    bird_data = {
        "size": "small",
        "beak_shape_1": "short",
        "beak_color": "black",
        "plumage_color": "yellow, brown",
        "tail_shape_1": "long",
        "new_attribute": {
            "call": "cheerful"
        }
    }
    
    summary = claude_summary(bird_data)
    print(summary)