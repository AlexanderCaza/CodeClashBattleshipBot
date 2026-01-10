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

        def shoot_cell_JSON(cell_x, cell_y):
            return {
                "combat": {
                    "cell": [cell_x, cell_y],
                    "ability": {"None": {}}
                }
            }
        
        def get_unsunk_ships(board): 
            for i in range(1, 8):
                row = board[i]
                for j in range(1, 8):
                    cell = row[j]

            

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
        
        def does_ship_fit(ship_dimensions, opponent_grid, start_coords) -> bool:
            #TODO: change to row and square
            start_row = start_coords[0]
            start_square = start_coords[1]

            ship_hori = ship_dimensions[0]
            ship_verti = ship_dimensions[1]
            
            #if we've run out of rows
            if start_row + ship_verti[0] > 8:
                return False
            #run out of columns
            if start_square[1] + ship_hori[1] > 8:
                return False
            
            #check horizontal space
            for i in range(ship_hori):
                for j in range(ship_verti):
                    if opponent_grid[start_row + j][start_square + i] != "N":
                        return False
            return True
        
        def add_ship_to_PDF(ship_dimensions, PDF_grid, opponent_grid):
            #TODO: change to row and square
            for x in range(8):
                for y in range(8):
                    if does_ship_fit(ship_dimensions, opponent_grid, (x, y)):
                        for i in range(x):
                            for j in range(y):
                                PDF_grid[y][x] = PDF_grid[y][x] + 1

        def generate_PDF(opponent_grid, ship_list):
            #Returns the PDF grid
            PDF_grid = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        ]
            for ship in ship_list:
                #TODO: transform ship name into dimensions
                add_ship_to_PDF(ship, PDF_grid, opponent_grid) 
            return PDF_grid
        
        def get_max_PDF_coords(PDF_grid):
            max_coords = []
            max_val = 0
            for row in range(8):
                for square in range(8):
                    if PDF_grid[row][square] >= max_val:
                        max_val = PDF_grid[row][square]
                        max_coords = [row, square]
            return max_coords
        
        def attack_shields(sonar_result, opponent_grid):
            #Returns coordinates of shield if it exists and we should attack it
            #Returns False otherwise
            for row in range(8):
                for col in range(8):
                    if opponent_grid[row][col] == "S":
                        if random.randint(0, 2) == 2:
                            return (row, col)
                        else:
                            return False
                        
            return False
        
        sonar_result = get_sonar_result(<info>)
        attack_shields_result = attack_shields(sonar_result, opponent_grid)
        if (attack_shields_result):
            return attack_shields_result
        target_list, sunk_ships = get_opportunistic_targets(opponent_grid)
        if (target_list):
            return select_next_target(opponent_grid, target_list)

        
        PDF_grid = generate_PDF(opponent_grid, ship_list)
        target_coords = get_max_PDF_coords(PDF_grid)
        return {
            "combat": {
                "cell": target_coords,
                "ability": {"None": {}}
            }
        }
    
        
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