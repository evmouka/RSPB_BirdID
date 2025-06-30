from dataclasses import dataclass
from typing import List, Dict, Optional, Set
import sqlite3
import json
import anthropic
from difflib import SequenceMatcher

@dataclass
class BirdFeature:
    name: str
    value: str
    confidence: float
    source_fields: List[str]

class ImprovedBirdIdentifier:
    def __init__(self, db_path: str, words_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        with open(words_path) as f:
            self.common_words = json.load(f)
            
        self.collected_features: Dict[str, BirdFeature] = {}
        self.asked_features: Set[str] = set()
        
        # Feature priority order
        self.feature_order = [
            "Plumage colour(s)",
            "Pattern/ Markings",
            "Size",
            "Beak Shape 1",
            "Beak Colour(s)", 
            "Tail shape 1",
            "Feet colour(s)",
            "Leg colour(s)"
        ]

    def string_similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def extract_features(self, text: str) -> List[BirdFeature]:
        features = []
        text = text.lower()
        
        # Check each feature category
        for category, words in self.common_words.items():
            words = [w.lower() for w in words.split(", ")]
            
            for word in words:
                if word in text:
                    confidence = self.string_similarity(word, text)
                    features.append(BirdFeature(
                        name=category,
                        value=word,
                        confidence=confidence,
                        source_fields=[category]
                    ))
                    
        return features

    def get_next_question(self) -> Optional[str]:
        for feature in self.feature_order:
            if (feature not in self.collected_features and 
                feature not in self.asked_features):
                self.asked_features.add(feature)
                return self.generate_question(feature)
        return None

    def generate_question(self, feature: str) -> str:
        questions = {
            "Plumage colour(s)": "What colors do you see on the bird?",
            "Pattern/ Markings": "Do you notice any distinctive patterns or markings?",
            "Size": "How big is the bird compared to a sparrow or pigeon?",
            "Beak Shape 1": "What shape is the bird's beak?",
            "Beak Colour(s)": "What color is the beak?",
            "Tail shape 1": "What shape is the tail?",
            "Feet colour(s)": "What color are the feet?",
            "Leg colour(s)": "What color are the legs?"
        }
        return questions.get(feature, f"Can you tell me about the bird's {feature.lower()}?")

    def identify_bird(self) -> List[Dict]:
        query = """
        SELECT * FROM birds WHERE 1=1
        """
        params = []
        
        for feature in self.collected_features.values():
            if feature.confidence > 0.7:
                placeholders = " OR ".join([f"{field} LIKE ?" for field in feature.source_fields])
                query += f" AND ({placeholders})"
                params.extend([f"%{feature.value}%" for _ in feature.source_fields])
        
        self.cursor.execute(query, params)
        matches = self.cursor.fetchall()
        
        return [dict(zip([col[0] for col in self.cursor.description], row)) 
                for row in matches]

class ImprovedBirdChat:
    def __init__(self, api_key: str, db_path: str, words_path: str):
        self.client = anthropic.Client(api_key=api_key)
        self.identifier = ImprovedBirdIdentifier(db_path, words_path)
        
    async def chat(self, message: str) -> str:
        # Extract features from user message
        features = self.identifier.extract_features(message)
        
        # Update collected features
        for feature in features:
            self.identifier.collected_features[feature.name] = feature
            
        # Get next question if needed
        next_question = self.identifier.get_next_question()
        
        if next_question:
            return next_question
            
        # If we have enough features, identify the bird
        if len(self.identifier.collected_features) >= 3:
            matches = self.identifier.identify_bird()
            if matches:
                return self.format_bird_matches(matches)
            
        return "I need more information about the bird. " + next_question

    def format_bird_matches(self, matches: List[Dict]) -> str:
        if not matches:
            return "I couldn't find any birds matching that description."
            
        response = []
        for match in matches[:3]:  # Top 3 matches
            confidence = self.calculate_match_confidence(match)
            response.append(f"- {match['Name']} ({confidence:.0%} confident)")
            
        return "\n".join(response)

    def calculate_match_confidence(self, match: Dict) -> float:
        total_weight = 0
        matched_weight = 0
        
        for feature in self.identifier.collected_features.values():
            weight = 1.0 if feature.name in self.identifier.feature_order[:3] else 0.5
            total_weight += weight
            
            if any(feature.value in str(match.get(field, "")).lower() 
                  for field in feature.source_fields):
                matched_weight += weight * feature.confidence
                
        return matched_weight / total_weight if total_weight > 0 else 0.0