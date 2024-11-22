from flask import Flask, request, jsonify
from model import Guess, Answer
from flask_cors import CORS, cross_origin
from algo import find_bird

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
def process_bird_data(json_data):
    request_data = Guess(
        message=json_data["message"],
        category_prompt=json_data["categoryPrompt"],
        categories=json_data["categories"]
    )

    isConfused = False
    # request for adjectives from claude algorith.py 

    if not isConfused:
        question, birds = find_bird({
            "Plumage colour(s)": 'Brown'
        })

    print(question, birds)

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
@cross_origin()
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
    
@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify('erorr: No JSON data provided')
        
        # This IP can be user with libraries like "Flask-Simple-GeoIP" to map the IP to a region
        ip = request.remote_addr

        return jsonify("request accepted"), 202

if __name__ == '__main__':
    app.run(port=5000)