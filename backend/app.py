from flask import Flask, request, jsonify
from model.guess import Guess
from model.answer import Answer
from flask_cors import CORS, cross_origin
from src.filter import find_bird, fetch_db
from src.claude_1a import claude_1
from src.utils import update_and_join ,server_setup, hard_summary
from src.claude_summary import claude_summary
from src.formatData import formatData, save_user_data
from dotenv import load_dotenv
import json

app = Flask(__name__)
cors = CORS(app)
load_dotenv()
app.config['CORS_HEADERS'] = 'Content-Type'
with open('config.json') as config_file:
    app.config.update(json.load(config_file))
all_words = server_setup(app.config["key_features"])

def process_bird_data(json_data):
    request_data = Guess(
        id=-1, #id for game mode
        message=json_data["message"],
        category_prompt=json_data["categoryPrompt"],
        categories=json_data["categories"],
        user_data=json_data["user_data"]
    )

    #claude interpret input
    dic = claude_1(request_data.message, request_data.category_prompt, all_words)

    #join new to old dictionnary
    dic = update_and_join(dic, request_data.categories)

    #if both dictionnary are the same and a category was prompt -> set category to null so not reasked
    if dic == request_data.categories and request_data.category_prompt:
        dic[request_data.category_prompt] = None


    #find next best question + filtering
    question, error, matches = find_bird(dic, app.config['birds_left'], app.config['key_features'], request_data.id, app.config['match_count'])
    #get sumamry from claude
    if dic:
        summary = hard_summary(dic)

        #custom clause summary
        # summary = claude_summary(dic)
    else:
        summary = "We couldn't manage to get any informations from your input"

    #format user data
    user_data = formatData(dic, request_data.message, request_data.user_data, error)

    #if found birds or error we save user data
    if matches or not question or error:
        save_user_data(user_data, matches)

    response_data = Answer(
        isConfused = False,
        category_prompt = question,
        identifications = matches,
        categories =  dic,
        summary = summary,
        user_data = user_data
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

        return jsonify({'message': 'Bird data processed successfully', 'data': processed_data.to_dict()}), 200

    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/new-bird', methods=['GET'])
def get_bird():
    if request.method == 'GET':
        bird = fetch_db(None, None, True)
        return jsonify({"id": bird['species_number'], "image": bird['picture']})
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(host="0.0.0.0")