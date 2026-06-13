#from dataclasses import dataclass
from faker import Faker
from core.player import Player, Attributes, Trait, Contract, Morale

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

    def generate_stats(self, position_role):

        position_stats = POSITIONS_DATA[position_role]["stats"]
        position_weights = POSITIONS_DATA[position_role]["weights"]

        player_stats = {}

        for stat in position_stats:

            stats_range = range(position_stats[stat][0], position_stats[stat][1])
            generated_stat = self.randomizer.choice(stats_range)
            player_stats[stat] = generated_stat

        attributes = Attributes(**player_stats)

        attributes.calculate_overall_rating(**position_weights)

        return attributes

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

    def generate_player(self, position_layer=None):

        if position_layer is None:
            position_layer = self.randomizer.choice(self.position_categories)

        if position_layer != "GK":
            position_role = self.randomizer.choice(self.position_specific_roles[position_layer])

        else:
            position_role = "GK"

        player_stats = self.stats_gen.generate_stats(position_role)
        player_name, age, nationality = self.generate_profile(self.randomizer.choice(LOCALES))
        height = 120
        weight = 70
        strong_foot = "Right"

        morale = Morale(
            condition="Fine",
            happiness=70,
            playtime=0
        )

        traits = None

        contract = Contract(
            "Active",
            "Red Devils United",
            "4 years",
            15000
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
            contract
        )
    
    def generate_profile(self, locale):

        fake = Faker(locale)
        Faker.seed(self.seed)

        player_name = f"{fake.unique.first_name_male()} {fake.unique.last_name()}"
        age = fake.random_int(min=18, max=27)
        nationality = fake.current_country()

        return player_name, age, nationality