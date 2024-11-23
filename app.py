from flask import Flask, request, jsonify
from model import Guess, Answer
from flask_cors import CORS, cross_origin
from algo import find_bird, fetch_db
from claude_1a import claude_1
from utils import update_and_join
from claude_summary import claude_summary

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
def process_bird_data(json_data):
    request_data = Guess(
        message=json_data["message"],
        category_prompt=json_data["categoryPrompt"],
        categories=json_data["categories"]
    )

    dic = claude_1(request_data.message, request_data.category_prompt)
    dic =  dic["bird_sighting"]
    if not dic:
        dic = {}
    dic = update_and_join(request_data.categories, dic)
    algo_dic = dic.copy()
    if "new_attribute" in dic:
        del algo_dic["new_attribute"]
    isConfused = False
    if not isConfused:
        question, birds = find_bird(algo_dic)
    summary = claude_summary(algo_dic)
    print(summary)
    response_data = Answer(
        isConfused =isConfused,
        category_prompt = question,
        identifications = birds,
        categories =  dic,
        summary = summary
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
    
@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify('erorr: No JSON data provided')

        return jsonify("request accepted"), 202

if __name__ == '__main__':
    app.run(port=5000)