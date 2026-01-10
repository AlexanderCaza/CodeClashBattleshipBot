#!/usr/bin/env python3
"""
Code Clash Battleship Bot Challenge - CREATE UofT - Winter 2026

YOUR CUSTOM BATTLESHIP BOT STRATEGY
Override the strategy methods below to implement your bot.

===========================================
IMPORTANT:
===========================================
- DO NOT modify battleship_api.py
- ONLY override the 3 strategy methods below
- Use helper methods (starting with _) from the API
- Test your bot with bot_validator.py before submission

Have fun!
"""

import random
from battleship_api import BattleshipBotAPI, run_bot, ABILITY_CODES

class MyBattleshipBot(BattleshipBotAPI):
    def ability_selection(self) -> list:
        """Choose 2 abilities for the entire game."""
        return ["SP", "HS"] 
    
    def place_ship_strategy(self, ship_name: str, game_state: dict) -> dict:
        """Place a ship on your board."""
        # TODO: Replace with your strategy
        ship_positions = thisdict = {
            "ship_1x2": [8, 7],
            "ship_1x3": [4, 7], 
            "ship_1x4": [5, 2], 
            "ship_2x3": [4, 5]
        }
        ship_directions = {
            "ship_1x2": "V",
            "ship_1x3": "H", 
            "ship_1x4": "H", 
            "ship_2x3": "H"
        }
        return {
            "placement": {
                "name": ship_name, 
                "cell": ship_positions[ship_name], 
                "direction": ship_directions[ship_name]
            }
        }
        
    def combat_strategy(self, game_state: dict) -> dict:
        """Choose a combat move."""
        # TODO: Replace with your strategy
        available_abilities = self._get_available_abilities(game_state)
        opponent_grid = self._get_opponent_grid(game_state)
        available_cells = self._get_available_cells(opponent_grid)

        def count_N(opponent_grid):
        #Returns the number of untargeted squares in the grid.
            total = 0
            for row in opponent_grid:
                for square in row:
                    if square == "N":
                        total += 1
            return total

        #first move: use SP
        if count_N(opponent_grid) == 64:
        #if blank grid, i.e. first move
            #do SP in the middleish of the board
            return {
                "combat": {
                    "cell": [0, 0],
                    "ability": {"SP": [3, 3]}
                }
            }
        
        #second move: use HS
        if count_N(opponent_grid) == 64 - 9:
            #if it's the second move, at which point we've fired at 9 cells
            return {
                "combat": {
                    "cell": [0, 0],
                    "ability": {"HS": [0, 0]}
                }
            }

        def generate_PDF(opponent_grid, ship_list):
            PDF_grid = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        ]
            return PDF_grid
        
        if available_cells:
            target = random.choice(available_cells)
        else:
            target = [random.randint(0, 7), random.randint(0, 7)]
        
        return {
            "combat": {
                "cell": target,
                "ability": {"None": {}}
            }
        }

if __name__ == '__main__':
    run_bot(MyBattleshipBot)