from enum import Enum
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import datetime

# Enums for bird characteristics
class BirdColor(str, Enum):
    BLUE = 'blue'
    BLACK = 'black'
    BROWN = 'brown'
    GREY = 'grey'
    GREEN = 'green'
    ORANGE = 'orange'
    PINK = 'pink'
    PURPLE = 'purple'
    RED = 'red'
    YELLOW = 'yellow'
    WHITE = 'white'
    BEIGE = 'beige'

class BeakShape(str, Enum):
    SHARP_THIN_POINTED = 'sharp_thin_pointed'
    SHORT_STUBBY_POINTED = 'short_stubby_pointed'
    SHORT_NARROW_CURVED = 'short_narrow_curved'
    SHARP_THICK_POINTED = 'sharp_thick_pointed'
    LONG_WIDE_ROUNDED = 'long_wide_rounded'
    SHORT_SHARP_HOOKED = 'short_sharp_hooked'
    LONG_THICK_CURVED = 'long_thick_curved'
    VERY_LONG_THIN = 'very_long_thin'

class TailShape(str, Enum):
    FORKED = 'forked'
    POINTED = 'pointed'
    ROUNDED = 'rounded'
    SQUARED = 'squared'
    DIAMOND = 'diamond'
    FAN = 'fan'
    DOUBLE = 'double'

class Habitat(str, Enum):
    WOODLAND = 'woodland'
    GARDEN_OR_PARK = 'garden_or_park'
    FARMLAND_OR_HEDGEROW = 'farmland_or_hedgerow'
    COAST = 'on_the_coast'
    MEADOW_OR_GRASSLAND = 'meadow_or_grassland'
    MOUNTAINS_OR_UPLANDS = 'mountains_or_uplands'
    FRESH_WATER = 'near_or_in_fresh_water'
    TOWN_OR_CITY = 'town_or_city'

class BirdSize(str, Enum):
    VERY_SMALL = 'very_small'  # < 15cm
    SMALL = 'small'           # 15-25cm
    MEDIUM = 'medium'         # 25-40cm
    LARGE = 'large'          # 40-70cm
    VERY_LARGE = 'very_large' # > 70cm

@dataclass
class BirdSpecies:
    id: str
    common_name: str
    scientific_name: str
    plumage_colors: List[BirdColor]
    beak_colors: List[BirdColor]
    feet_colors: List[BirdColor]
    leg_colors: List[BirdColor]
    beak_shapes: List[BeakShape]
    tail_shapes: List[TailShape]
    min_length_cm: float
    max_length_cm: float
    mean_length_cm: float
    size: BirdSize
    habitats: List[Habitat]
    description: Optional[str] = None
    common_species: bool = True
    seasonal_presence: Dict[str, bool] = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

@dataclass
class SearchParams:
    colors: Optional[List[BirdColor]] = None
    beak_shape: Optional[List[BeakShape]] = None
    tail_shape: Optional[List[TailShape]] = None
    size: Optional[List[BirdSize]] = None
    habitat: Optional[List[Habitat]] = None
    min_length: Optional[float] = None
    max_length: Optional[float] = None

@dataclass
class MatchScore:
    bird: BirdSpecies
    color_score: float
    beak_score: float
    tail_score: float
    size_score: float
    habitat_score: float
    total_score: float

class BirdIdentifier:
    def __init__(self):
        self.color_weight = 0.35
        self.beak_weight = 0.25
        self.tail_weight = 0.15
        self.size_weight = 0.15
        self.habitat_weight = 0.10

    def identify_birds(self, search_params: SearchParams, bird_database: List[BirdSpecies], limit: int = 5) -> List[MatchScore]:
        """
        Main identification method that returns top matches with confidence scores
        """
        matches = []
        for bird in bird_database:
            scores = self._calculate_scores(search_params, bird)
            matches.append(scores)

        # Sort by total score and return top matches
        matches.sort(key=lambda x: x.total_score, reverse=True)
        return matches[:limit]

    def _calculate_scores(self, params: SearchParams, bird: BirdSpecies) -> MatchScore:
        """Calculate individual and total scores for a bird"""
        color_score = self._calculate_color_score(params, bird)
        beak_score = self._calculate_beak_score(params, bird)
        tail_score = self._calculate_tail_score(params, bird)
        size_score = self._calculate_size_score(params, bird)
        habitat_score = self._calculate_habitat_score(params, bird)

        total_score = (
            (color_score * self.color_weight) +
            (beak_score * self.beak_weight) +
            (tail_score * self.tail_weight) +
            (size_score * self.size_weight) +
            (habitat_score * self.habitat_weight)
        )

        return MatchScore(
            bird=bird,
            color_score=color_score,
            beak_score=beak_score,
            tail_score=tail_score,
            size_score=size_score,
            habitat_score=habitat_score,
            total_score=total_score
        )

    def _calculate_color_score(self, params: SearchParams, bird: BirdSpecies) -> float:
        """Calculate color matching score using F1-score-like metric"""
        if not params.colors:
            return 1.0

        # Combine all bird colors
        bird_colors = set(bird.plumage_colors + bird.beak_colors + 
                         bird.feet_colors + bird.leg_colors)
        
        # Count matches and mismatches
        matches = sum(1 for color in params.colors if color in bird_colors)
        false_positives = len(params.colors) - matches
        false_negatives = len(bird_colors) - matches

        # Calculate precision and recall
        precision = matches / (matches + false_positives) if matches + false_positives > 0 else 0
        recall = matches / (matches + false_negatives) if matches + false_negatives > 0 else 0

        # Calculate F1-score
        if precision + recall == 0:
            return 0
        return 2 * (precision * recall) / (precision + recall)

    def _calculate_beak_score(self, params: SearchParams, bird: BirdSpecies) -> float:
        """Calculate beak shape matching score"""
        if not params.beak_shape:
            return 1.0

        matches = sum(1 for shape in params.beak_shape if shape in bird.beak_shapes)
        return 1.0 if matches > 0 else 0.0

    def _calculate_tail_score(self, params: SearchParams, bird: BirdSpecies) -> float:
        """Calculate tail shape matching score"""
        if not params.tail_shape:
            return 1.0

        matches = sum(1 for shape in params.tail_shape if shape in bird.tail_shapes)
        return 1.0 if matches > 0 else 0.0

    def _calculate_size_score(self, params: SearchParams, bird: BirdSpecies) -> float:
        """Calculate size matching score"""
        if not params.size:
            return 1.0

        # Size order for proximity calculation
        size_order = [
            BirdSize.VERY_SMALL,
            BirdSize.SMALL,
            BirdSize.MEDIUM,
            BirdSize.LARGE,
            BirdSize.VERY_LARGE
        ]

        bird_size_idx = size_order.index(bird.size)
        param_size_indices = [size_order.index(s) for s in params.size]
        
        # Find closest size match
        closest_distance = min(abs(i - bird_size_idx) for i in param_size_indices)
        
        # Score decreases with distance from actual size
        return max(0, 1 - (closest_distance * 0.25))

    def _calculate_habitat_score(self, params: SearchParams, bird: BirdSpecies) -> float:
        """Calculate habitat matching score"""
        if not params.habitat:
            return 1.0

        matches = sum(1 for habitat in params.habitat if habitat in bird.habitats)
        return matches / len(params.habitat)

    def explain_results(self, score: MatchScore) -> str:
        """Generate child-friendly explanation of the match"""
        explanations = []
        
        if score.color_score > 0.8:
            explanations.append("The colors match really well!")
        elif score.color_score > 0.5:
            explanations.append("Some of the colors match.")

        if score.beak_score > 0.8:
            explanations.append("The beak shape is just right!")

        if score.tail_score > 0.8:
            explanations.append("The tail shape matches perfectly!")

        if score.size_score > 0.8:
            explanations.append("The size is exactly right!")
        elif score.size_score > 0.5:
            explanations.append("The size is pretty close.")

        if score.habitat_score > 0.8:
            explanations.append("And you found it in just the right place!")

        if not explanations:
            return "I'm not quite sure about this bird. Can you tell me more about what you saw?"

        return " ".join(explanations)

# Example usage:
"""
identifier = BirdIdentifier()

# Sample bird data
sample_bird = BirdSpecies(
    id="1",
    common_name="Herring Gull",
    scientific_name="Larus argentatus",
    plumage_colors=[BirdColor.WHITE, BirdColor.GREY, BirdColor.BLACK],
    beak_colors=[BirdColor.YELLOW, BirdColor.RED],
    feet_colors=[BirdColor.PINK],
    leg_colors=[BirdColor.PINK],
    beak_shapes=[BeakShape.LONG_THICK_CURVED],
    tail_shapes=[TailShape.SQUARED],
    min_length_cm=54,
    max_length_cm=60,
    mean_length_cm=57,
    size=BirdSize.LARGE,
    habitats=[Habitat.COAST, Habitat.FRESH_WATER]
)

# Sample search
search = SearchParams(
    colors=[BirdColor.WHITE, BirdColor.GREY],
    beak_shape=[BeakShape.LONG_THICK_CURVED],
    habitat=[Habitat.COAST]
)

results = identifier.identify_birds(search, [sample_bird])
for match in results:
    print(f"{match.bird.common_name}: {match.total_score * 100:.1f}% match")
    print(identifier.explain_results(match))
"""