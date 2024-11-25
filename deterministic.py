import pandas as pd
import sqlite3
import random

class BirdIdentifier:
    def __init__(self, birds_df: dict, dic: dict, features: list):
        self.birds = pd.DataFrame.from_dict(birds_df)
        self.curr_dic = dic
        self.features = features

    def calculate_match_percentage(self, bird: dict) -> float:
        """
        Calculate match percentage considering db values are comma-separated strings
        and current dictionary values are arrays.
        """
        total_features = 0
        matched_features = 0
        
        for feature, curr_values in self.curr_dic.items():
            if feature not in self.features:
                continue
                
            total_features += 1
            
            if feature in bird and not pd.isna(bird[feature]):
                bird_values = set(v.strip().lower() for v in bird[feature].split(','))
                
                if isinstance(curr_values, list):
                    curr_values_set = set(v.lower() for v in curr_values)
                else:
                    curr_values_set = {curr_values.lower()}
                
                if bird_values & curr_values_set:
                    matched_features += 1
                        
        if total_features == 0:
            return 0
        return (matched_features / total_features) * 100

    def get_best_matches(self) -> list:
        """
        Return all birds with their match percentages, sorted by best match.
        """
        matches = []
        current_birds = self.birds.to_dict(orient='records')
        
        for bird in current_birds:
            match_percentage = self.calculate_match_percentage(bird)
            matches.append({
                'name': bird['name'],
                'match_percentage': round(match_percentage, 2),
                # 'bird_data': bird
            })
        
        matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        return matches[:5]

    def can_feature_split_further(self, current_birds: list, feature: str) -> bool:
        """this function checks if a feature can help filter further"""
        possible_values = self.get_possible_values(current_birds, feature)
        current_size = len(current_birds)
        
        for value in possible_values:
            filtered_birds = self.filter_birds(current_birds, feature, value)
            if len(filtered_birds) < current_size and len(filtered_birds) > 0:
                return True
        return False
    
    def filter_birds(self, current_birds: list, feature: str, value: str) -> list:
        """this function filters birds based on a feature and its value"""
        return [bird for bird in current_birds 
                if pd.isna(bird.get(feature)) or value in bird.get(feature, '')]
    
    def find_best_feature(self, current_birds: list, used_features: list) -> str:
        """this function finds the best feature to filter on"""
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
        """this function returns all possible values for a feature"""
        values = set()
        for bird in birds_subset:
            if feature in bird and not pd.isna(bird[feature]):
                bird_values = set(v.strip() for v in bird[feature].split(','))
                values.update(bird_values)
        return values

    def find_best_question(self) -> tuple:
        """this function finds the best question to ask"""
        current_birds = self.birds.copy().to_dict(orient='records')
        used_features = list(self.curr_dic.keys())
        best_feature = self.find_best_feature(current_birds, used_features)
        if best_feature:
            return best_feature, None
        return best_feature, self.birds.to_dict(orient='records')
