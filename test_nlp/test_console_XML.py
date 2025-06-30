import anthropic
user_input = input("put your summary here: ")

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
)

# Replace placeholders like {{USER_INPUT}} with real values,
# because the SDK does not support variables.
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Analyze the provided information and identify which characteristics are already mentioned. The key characteristics we're looking for are:\n1. Plumage colour(s)\n2. Beak Colour(s)\n3. Feet colour(s)\n4. Leg colour(s)\n5. Beak Shape 1\n6. Beak shape 2 (optional)\n7. Tail shape 1\n8. Pattern/ Markings\n9. Size\n10. Habitat(s)\n\n<user_input>\n{user_input}\n</user_input>\n\nOnce you have gathered all the information, output your data in the following format:\n<bird_sighting>\n    <size>[BIRD SIZE]</size>\n    <plumage_colour></plumage_colour>\n    <pattern></pattern>\n    <beak_shape></beak_shape>\n    <beak_colour></beak_colour>\n</bird_sighting> \n\nthe values for this output should be taken from this JSON:\n|\n    \"Plumage colour(s)\": \"orange, blue, cream/buff, brow, pink, buff, cream, yellow, grey, purple, white, green, pale brown, brown, beige, black, red\",\n    \"Beak Colour(s)\": \"orange, yellow, grey, white, brown, black\",\n    \"Feet colour(s)\": \"blue, pink, grey, brown, black, red\",\n    \"Leg colour(s)\": \"pink, grey, brown, black, red\",\n    \"Beak Shape 1\": \"sharp, thick, narrow, short, curved, thin, hooked, long, pointed, stubby\",\n    \"Beak shape 2 (optional)\": \"sharp, thick, short, curved, long, pointed, stubby\",\n    \"Tail shape 1\": \"double, thin, fan, fanned in flight, square, long, pointed, forked\",\n    \"Pattern/ Markings\": \"black, yellow, bright yellow breast, green, white cheeks, black cap, red, black neck collar, blue, red brest, dark brown, sooty black. yellow bill, brown back, white, green gloss to the tail, black plumage, orange brest, darker wings and tail, speckles, green back, yellow eye ring, black stripe, purplish-blue iridescent sheen to the wing feathers\",\n    \"Size\": \"medium, extra small, large, small\",\n    \"Habitat(s)\": \"grassland, city, hedgerow, heathland, meadow, suburban, wetland, farmland, woodland, town, garden, park, urban, upland\"\n\n\n\n\n\n"""   
                }
            ]
        }
    ]
)
print(message.content)