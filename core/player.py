from dataclasses import dataclass
from typing import List

import json

@dataclass
class Attributes:

    # Offensive
    shooting: int
    offensive_vision: int
    heading: int
    free_kicks: int

    # Playmaking
    pace: int
    passing: int
    dribbling: int
    ball_control: int
    crossing: int

    # Defensive
    tackling: int
    defensive_vision: int
    interceptions: int
    physical: int

    # Goalkeeping
    gk_positioning: int
    gk_reflexes: int
    gk_handling: int

    def __repr__(self):

        return f"Offensive: {self.get_offensive()}\tDefensive: {self.get_defensive()}\nPlaymaking: {self.get_playmaking()}\tGoalkeeping: {self.get_goalkeeping()}"

    def get_offensive(self):
        return (self.shooting + self.offensive_vision + self.heading + self.free_kicks) // 4
    
    def get_playmaking(self):
        return (self.pace + self.passing + self.dribbling + self.ball_control + self.crossing) // 5

    def get_defensive(self):
        return (self.tackling + self.defensive_vision + self.interceptions + self.physical) // 4

    def get_goalkeeping(self):
        return (self.gk_positioning + self.gk_reflexes + self.gk_handling) // 3

    def calculate_overall_rating(self, offensive, defensive, playmaking, goalkeeping):

        return round(
            self.get_offensive() * offensive +
            self.get_playmaking() * playmaking +
            self.get_defensive() * defensive +
            self.get_goalkeeping() * goalkeeping
        )

# The experience players gained should depend on:
# How many games played.
# Performance of the player.
@dataclass
class Development:
    talent: float
    remaining_growth: int

@dataclass
class Trait:
    name: str
    effect: str

@dataclass
class Contract:
    status: str
    team: str
    duration: str
    weekly_wage: int
    release_clause: int | None

@dataclass
class Morale:
    # Injured or good
    condition: str
    # Percentage: 80% happy
    happiness: int
    playtime: int

# TODO: Add alt_roles field to define what other position the player can play.
#       Add development field with development class, defines the growth and potential of a player.
@dataclass
class Player:
    name: str
    age: int
    nationality: str
    height_cm: int
    weight_kg: int
    # Positions: FORWARD, MIDFIELD, DEFENSE, GOALKEEPER
    position_group: str
    # Roles: LW, ST, CAM
    best_role: str
    strong_foot: str
    morale: Morale
    attributes: Attributes
    traits: List[Trait] | None
    development: Development
    contract: Contract
    value_in_usd: int

    def __repr__(self):

        with open("positions.json", "r", encoding='utf-8') as position_file:
            POSITIONS_DATA = json.load(position_file)

        position_weights = POSITIONS_DATA[self.best_role]["weights"]

        return f"{self.name}\n{self.nationality}\n{self.best_role}\nOverall: {self.attributes.calculate_overall_rating(**position_weights)}\n{self.attributes}\n"