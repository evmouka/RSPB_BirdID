import sqlite3
import os
import numpy as np
import json

def update_and_join(dict1: dict, dict2: dict) -> dict:
    for key, value in dict2.items():
        if key == 'new_attribute' and key in dict1:
            dict1['new_attribute'] = update_and_join(dict1['new_attribute'], dict2['new_attribute'])
            continue

        if key in dict1:
            existing_values = set(dict1[key].split(", "))
            new_values = set(value.split(", "))
            combined_values = ", ".join(existing_values | new_values)
            dict1[key] = combined_values
        else:
            dict1[key] = value

    return dict1

def server_setup(key_features: list) -> dict:
    query = f"SELECT {', '.join(key_features)} FROM birdInfo"

    db = sqlite3.connect(os.getenv('POSTGRES_DB'))
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    results = np.array([list(row) for row in results])
    all_words = {}
    for i, feature in enumerate(key_features):
        all_words[feature] = []
        rows = results[:, i]
        for row in rows:
            if not row:
                continue
            adjectives = row.split(', ')
            for word in adjectives:
                if not word in all_words[feature]:
                    all_words[feature].append(word)
    cursor.close()
    db.close()
    # with open('words.json', "w") as file:
    #     json.dump(all_words, file, indent=4)
    return all_words