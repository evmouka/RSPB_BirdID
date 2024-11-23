class Answer:
    def __init__(self, isConfused, category_prompt, identifications, categories, summary, user_data):
        self.isConfused = isConfused
        self.category_prompt = category_prompt
        self.identifications = identifications
        self.categories = categories
        self.summary = summary
        self.user_data = user_data

    def to_dict(self):
        return {
            "isConfused": self.isConfused,
            "category_prompt": self.category_prompt,
            "categories": self.categories,
            "identifications": self.identifications,
            "categories": self.categories,
            "summary": self.summary,
            "user_data": self.user_data
        }

class Identification:
    def __init__(
        self,
        species_number: int,
        name: str,
        latin_name: str,
        alt_names: str,
        sex_age_variations: str,
        seasonal_variations: str,
        conservation_status: str,
        group: str,
        time_of_year_active: str,
        summary: str,
        picture_primary: str,
        picture_2: str,
        picture_3: str,
        picture_4: str,
        illustration: str,
        audio: str,
        distribution_map: str,
        plumage_colours: str,
        beak_colours: str,
        feet_colours: str,
        leg_colours: str,
        beak_shape_1: str,
        beak_shape_2: str,
        tail_shape_1: str,
        tail_shape_2: str,
        pattern_markings: str,
        diet: str,
        population_uk: str,
        min_length_cm: float,
        max_length_cm: float,
        mean_length_cm: float,
        size: str,
        wingspan_cm: str,
        weight_g: str,
        habitats: str,
        appearance: str,
        habitat_description: str,
        call: str,
        behaviour: str,
        fact_1: str,
        fact_2: str,
        fact_3: str,
        similar_species: str,
        where_to_see: str
    ):
        self.species_number = species_number
        self.name = name
        self.latin_name = latin_name
        self.alt_names = alt_names
        self.sex_age_variations = sex_age_variations
        self.seasonal_variations = seasonal_variations
        self.conservation_status = conservation_status
        self.group = group
        self.time_of_year_active = time_of_year_active
        self.summary = summary
        self.picture_primary = picture_primary
        self.picture_2 = picture_2
        self.picture_3 = picture_3
        self.picture_4 = picture_4
        self.illustration = illustration
        self.audio = audio
        self.distribution_map = distribution_map
        self.plumage_colours = plumage_colours
        self.beak_colours = beak_colours
        self.feet_colours = feet_colours
        self.leg_colours = leg_colours
        self.beak_shape_1 = beak_shape_1
        self.beak_shape_2 = beak_shape_2
        self.tail_shape_1 = tail_shape_1
        self.tail_shape_2 = tail_shape_2
        self.pattern_markings = pattern_markings
        self.diet = diet
        self.population_uk = population_uk
        self.min_length_cm = min_length_cm
        self.max_length_cm = max_length_cm
        self.mean_length_cm = mean_length_cm
        self.size = size
        self.wingspan_cm = wingspan_cm
        self.weight_g = weight_g
        self.habitats = habitats
        self.appearance = appearance
        self.habitat_description = habitat_description
        self.call = call
        self.behaviour = behaviour
        self.fact_1 = fact_1
        self.fact_2 = fact_2
        self.fact_3 = fact_3
        self.similar_species = similar_species
        self.where_to_see = where_to_see


class Category:
    def __init__(self, plumage_colours: str, tail_shape_1: str, size: str, beak_shape: str):
        self.plumage_colours = plumage_colours
        self.tail_shape_1 = tail_shape_1
        self.size = size
        self.beak_shape = beak_shape


class BirdData:
    def __init__(self, is_confused: bool, category_prompt: str, identifications: dict, categories: dict):
        self.is_confused = is_confused
        self.category_prompt = category_prompt
        self.identifications = Identification(**identifications)  # Pass as keyword arguments
        self.categories = Category(**categories)  # Pass as keyword arguments

    def display(self):
        print("Is Confused:", self.is_confused)
        print("Category Prompt:", self.category_prompt)
        print("Identifications:", vars(self.identifications))
        print("Categories:", vars(self.categories))