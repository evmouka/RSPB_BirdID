import pandas as pd
import sqlite3
import random

class BirdIdentifier:
    def __init__(self, birds_df: dict, dic: dict, features: list):
        self.birds = pd.DataFrame.from_dict(birds_df)
        self.curr_dic = dic
        self.features = features

    def can_feature_split_further(self, current_birds: list, feature: str) -> bool:
        possible_values = self.get_possible_values(current_birds, feature)
        current_size = len(current_birds)
        
        for value in possible_values:
            filtered_birds = self.filter_birds(current_birds, feature, value)
            if len(filtered_birds) < current_size and len(filtered_birds) > 0:
                return True
        return False
    
    def filter_birds(self, current_birds: list, feature: str, value: str) -> list:
        return [bird for bird in current_birds 
                if pd.isna(bird.get(feature)) or value in bird.get(feature, '')]
    
    def find_best_feature(self, current_birds: list, used_features: list) -> str:
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

    def get_possible_values(self, birds_subset: list, feature: str) -> set:
        values = set()
        for bird in birds_subset:
            if feature in bird and not pd.isna(bird[feature]):
                bird_values = set(v.strip() for v in bird[feature].split(','))
                values.update(bird_values)
        return values

    def find_best_question(self) -> tuple:
        current_birds = self.birds.copy().to_dict(orient='records')
        used_features = list(self.curr_dic.keys())
        best_feature = self.find_best_feature(current_birds, used_features)
        if best_feature:
            self.birds = None
        else:
            self.birds = self.birds.to_dict(orient='records')
        return best_feature, self.birds
