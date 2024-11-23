import pandas as pd
import sqlite3
import random

class BirdIdentifier:
    def __init__(self, birds_df, dic):
        self.birds = pd.DataFrame.from_dict(birds_df)
        self.curr_dic = dic
        self.features = [
            "plumage_colour", "beak_Colour", "feet_colour", 
            "leg_colour", "beak_Shape_1", "tail_shape_1", 
            "size", "habitat", "pattern_markings"
        ]

    def can_feature_split_further(self, current_birds, feature):
        possible_values = self.get_possible_values(current_birds, feature)
        current_size = len(current_birds)
        
        for value in possible_values:
            filtered_birds = self.filter_birds(current_birds, feature, value)
            if len(filtered_birds) < current_size and len(filtered_birds) > 0:
                return True
        return False
    def filter_birds(self, current_birds, feature, value):
        return [bird for bird in current_birds 
                if pd.isna(bird.get(feature)) or value in bird.get(feature, '')]
    
    def find_best_feature(self, current_birds, used_features):
        best_score = float('inf')
        best_feature = None
        
        for feature in self.features:
            if feature not in used_features:
                if not self.can_feature_split_further(current_birds, feature):
                    continue
                    
                possible_values = self.get_possible_values(current_birds, feature)
                if not possible_values:
                    continue
                
                total_remaining = 0
                max_group_size = 0
                for value in possible_values:
                    matching_birds = self.filter_birds(current_birds, feature, value)
                    group_size = len(matching_birds)
                    total_remaining += group_size
                    max_group_size = max(max_group_size, group_size)
                
                avg_remaining = total_remaining / len(possible_values)
                score = avg_remaining + max_group_size
                
                if score < best_score:
                    best_score = score
                    best_feature = feature
        
        if not best_feature:
            for feature in self.features:
                if (feature not in used_features and 
                    self.can_feature_split_further(current_birds, feature)):
                    return feature
                    
        return best_feature

    def get_possible_values(self, birds_subset, feature):
        values = set()
        for bird in birds_subset:
            if feature in bird and not pd.isna(bird[feature]):
                bird_values = set(v.strip() for v in bird[feature].split(','))
                values.update(bird_values)
        return values

    def find_best_question(self):
        current_birds = self.birds.copy().to_dict(orient='records')
        used_features = list(self.curr_dic.keys())
        best_feature = self.find_best_feature(current_birds, used_features)
        if best_feature:
            self.birds = None
        else:
            self.birds = self.birds.to_dict(orient='records')
        return best_feature, self.birds

def create_querry(dbName: str, dic: dict) -> str:
    query = f"SELECT * FROM {dbName} WHERE 1=1"
    params = []
    for key, value in dic.items():
        if not value:
            continue
        conditions = []
        value = value.split(', ')
        key = f"`{key}`"
        for item in value:
            conditions.append(f"{key} LIKE ?")
            params.append(f"%{item}%")      
        if conditions:
            query += f" AND ({' AND '.join(conditions)} OR {key} IS NULL)"
    return query, params 

def fetch_db(querry: str, params: list, isGame: bool=False) -> list:
    db = sqlite3.connect('bird_database.db')
    cursor = db.cursor()
    if isGame:
        cursor.execute("select * from birdInfo")
    else:
        cursor.execute(querry, params)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    
    result = [dict(zip(column_names, row)) for row in rows]
    
    db.close()
    if isGame:
        return random.choice(result)
    return result

def find_bird(dic: dict):
    query, params = create_querry("birdInfo", dic)
    birds = fetch_db(query, params)
    if len(birds) == 1:
        return None, birds
    bird = BirdIdentifier(birds, dic)
    question, bird = bird.find_best_question()

    return question, bird

