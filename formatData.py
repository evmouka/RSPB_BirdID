import json

def calculate_average(conversations):
    total = 0
    for conv in conversations:
        total += conv['length']
    return total / len(conversations)

def formatData(categories, new_attribute, user_input, current_data, error=None):
    if not current_data:
        with open('blankData.json', 'r') as file:
            current_data = json.load(file)
    current_data['user_data']['conversation'].append({
        'text': user_input,
        "categories_described": categories,
        "new_attribute": new_attribute,
        "length": len(user_input.split())
        })
    if error:
        current_data['user_data']['error'] = error
    return current_data

def save_user_data(data, suggestions):
    if data['user_data']['error']:
        data['app_response']['correct'] = False
    data['app_response']['suggestions'] = [entry['name'] for entry in suggestions if 'name' in entry]
    data['user_data']['average_message_length'] = calculate_average(data['user_data']['conversation'])
    with open('user_data.json', "r") as file:
        database = json.load(file)
    database.append(data)
    with open('user_data.json', "w") as file:
        json.dump(database, file, indent=4)