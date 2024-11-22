from flask import Flask, request, jsonify
from model import Guess, Answer

app = Flask(__name__)

def process_bird_data(json_data):
    request_data = Guess(
        message=json_data["message"],
        category_prompt=json_data["categoryPrompt"],
        categories=json_data["categories"]
    )

    # request for adjectives from claude algorith.py 

    # request to db based on adjectives

    response_data = Answer(
        isConfused ="false",
        category_prompt = "beak shape",
        identifications = None,
        categories =  {
            "Plumage colour(s)": "black, gray",
            "Tail shape 1": "fan",
            "Size": "small"
        }
    )
    return response_data

@app.route('/birds', methods=['POST'])
def birds():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'})

        processed_data = process_bird_data(data)
        
        # Call the to_dict method and pass its result to jsonify
        return jsonify({'message': 'Bird data processed successfully', 'data': processed_data.to_dict()}), 200

    else:
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(port=5000)