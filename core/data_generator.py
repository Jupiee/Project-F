#from dataclasses import dataclass
from faker import Faker
from core.player import Player, Attributes, Trait, Contract, Morale, Development

import random
import json

#  Young player => 18 - 20
#  Prime player => 20 - 30
#  Developed player => 30 - 40

LOCALES = ["fr_FR", "it_IT", "de_DE", "en_US", "en_UK", "pt_BR", "es_AR", "es_ES", "uk_UA", "tr_TR", "sv_SE", "sq_AL"]

with open("positions.json", "r", encoding='utf-8') as position_file:
    POSITIONS_DATA = json.load(position_file)

class Stats_Gen:

    def __init__(self, randomizer):

        self.randomizer = randomizer

    def generate_stats(self, position_role, age):

        position_stats = POSITIONS_DATA[position_role]["stats"]

        player_stats = {}

        age_factor = self.get_age_factor(age)

        for stat in position_stats:

            min_stat, max_stat = (position_stats[stat][0], position_stats[stat][1])
            base = min_stat + (max_stat - min_stat) * age_factor
            noise = self.randomizer.randint(-3, 3)
            mixed_stat = round(base + noise)
            finalized_stat = max(min_stat, min(mixed_stat, max_stat))
            
            player_stats[stat] = finalized_stat

        attributes = Attributes(**player_stats)

        return attributes
    
    def get_age_factor(self, age):

        if age <= 18:
            return 0.15
        
        if age <= 20:
            return 0.30
        
        if age <= 23:
            return 0.50
        
        if age <= 26:
            return 0.75
        
        return 0.90

class Player_Gen:

    def __init__(self, seed=None):

        self.seed = seed
        self.randomizer = random.Random(seed)
        self.position_categories = ["GK", "DEF", "MF", "FW"]
        self.position_specific_roles = {
            "DEF": ["CB", "LB", "RB", "LWB", "RWB"],
            "MF": ["DMF", "CM", "RM", "LM", "CAM"],
            "FW": ["CF", "ST", "LW", "RW", "SS"]
        }
        self.stats_gen = Stats_Gen(self.randomizer)

    def generate_player(self, position_layer=None, position_role=None):

        if position_layer is None and position_role is None:
            position_layer = self.randomizer.choice(self.position_categories)

        if position_layer is not None and position_role is None:

            if position_layer == "GK":
                position_role = "GK"

            elif position_layer in self.position_categories:
                position_role = self.randomizer.choice(self.position_specific_roles[position_layer])

            else:
                raise ValueError(f"Invalid Position layer {position_layer}, it must be one of GK, DEF, MF or FW")

        elif position_layer is None and position_role is not None:

            if position_role == "GK":
                position_layer = "GK"

            else:

                for layer in range(1, 4):
                    if position_role in self.position_specific_roles[self.position_categories[layer]]:
                        position_layer = layer
                        break

                if position_layer is None:

                    raise ValueError(f"Invalid Position role {position_role}")

        foot_bias_weights = POSITIONS_DATA[position_role]["foot_bias"]
        position_weights = POSITIONS_DATA[position_role]["weights"]

        player_name, age, nationality = self.generate_profile(self.randomizer.choice(LOCALES))

        player_stats = self.stats_gen.generate_stats(position_role, age)

        height = 120
        weight = 70
        
        strong_foot = self.randomizer.choices(population=['Left', 'Right'], weights=[foot_bias_weights['left'], foot_bias_weights['right']], k=1)[0]

        morale = Morale(
            condition="Fine",
            happiness=70,
            playtime=0
        )

        traits = None
        
        overall_rating = player_stats.calculate_overall_rating(**position_weights)
        remaining_years = max(0, 35 - age)
        talent = self.randomizer.gauss(1.0, 0.15)
        random_factor = self.randomizer.uniform(0.85, 1.15)
        growth_room = remaining_years * talent * random_factor
        max_cap = overall_rating + growth_room

        max_cap = round(min(99, max_cap))

        development = Development(
            0.5,
            max_cap,
            max_cap
        )

        contract = Contract(
            "Active",
            "Red Devils United",
            "4 years",
            15000,
            None
        )

        return Player(
            player_name,
            age,
            nationality,
            height,
            weight,
            position_layer,
            position_role,
            strong_foot,
            morale,
            player_stats,
            traits,
            development,
            contract,
            1000000
        )
    
    def generate_profile(self, locale):

        fake = Faker(locale)
        Faker.seed(self.seed)

        player_name = f"{fake.unique.first_name_male()} {fake.unique.last_name()}"
        age = fake.random_int(min=18, max=27)
        nationality = fake.current_country()

        return player_name, age, nationality