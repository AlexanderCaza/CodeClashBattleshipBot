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
            "ship_1x2": [7, 6],
            "ship_1x3": [3, 6], 
            "ship_1x4": [4, 1], 
            "ship_2x3": [3, 4]
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

        def shoot_cell_JSON(row, col):
            #TODO: double-check API coordinate logic
            return {
                "combat": {
                    "cell": [row, col],
                    "ability": {"None": {}}
                }
            }

        def is_blank(opponent_grid):
        #Returns True if the grid is blank, False otherwise.
            total = 0
            for row in opponent_grid:
                for square in row:
                    if square != "N":
                        return False
            return True
        
        is_blank = is_blank(opponent_grid)
        
        def does_ship_fit(ship_dimensions, opponent_grid, start_coords) -> bool:
            #TODO: change to row and square
            start_row = start_coords[0]
            start_square = start_coords[1]

            ship_hori = ship_dimensions[0]
            ship_verti = ship_dimensions[1]
            
            #if we've run out of rows
            if start_row + ship_verti > 8:
                return False
            #run out of columns
            if start_square + ship_hori > 8:
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
            return

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
            #TODO: there may be a bug here
            max_coords = [0, 0]
            max_val = 0
            for row in range(8):
                for square in range(8):
                    if PDF_grid[row][square] >= max_val:
                        max_val = PDF_grid[row][square]
                        max_coords = [row, square]
            return max_coords
        
        def unsunk_from_sunk(sunk_ships):
            unsunk_ships = [(4, 1), (1, 4), (2, 3), (3, 2), (1, 3), (3, 1), (1, 2), (2, 1)]
            for ship in sunk_ships:
                if ship == "ship_1x2":
                    unsunk_ships.remove((1, 2))
                    unsunk_ships.remove((2, 1))
                elif ship == "ship_1x3":
                    unsunk_ships.remove((1, 3))
                    unsunk_ships.remove((3, 1))
                elif ship == "ship_1x4":
                    unsunk_ships.remove((1, 4))
                    unsunk_ships.remove((4, 1))
                elif ship == "ship_2x3":
                    unsunk_ships.remove((2, 3))
                    unsunk_ships.remove((3, 2))
            return unsunk_ships
        
        def attack_shields(opponent_grid):
            #Returns combat JSON of shield if it exists and we should attack it
            #Returns False otherwise
            for row in range(8):
                for col in range(8):
                    if opponent_grid[row][col] == "B":
                        if random.randint(0, 2) == 2:
                            return shoot_cell_JSON(row, col)
                        else:
                            return False
                        
            return False        
        
        def get_adjacent_cells(row, column):
            adjacent_cells = []
            if (row >= 1):
                adjacent_cells.append([row - 1, column])
            if (row <= 6):
                adjacent_cells.append([row + 1, column])
            if (column >= 1):
                adjacent_cells.append([row, column - 1])
            if (column <= 6):
                adjacent_cells.append([row, column + 1])
       
        def get_opportunistic_targets(opponent_grid):
            hits_to_process = []
            cells_processed = []
            opportunity_targets = []
            sunk_ships = []
            hits_in_group = []
            for i in range(0, 7):
                row = opponent_grid[i]
                for j in range(0, 7):
                    number_of_hits_in_group = 0
                    cell = row[j]
                    if (cell == "H" or cell == "B"):
                        if ([i, j] in cells_processed): 
                            continue
                        cells_to_check = [[0, 0]] #get_adjacent_cells(i, j)
                        number_of_hits_in_group += 1
                        for cell_being_processed in cells_to_check:
                            cell_row = cell_being_processed[0]
                            cell_column = cell_being_processed[1]
                            cell_content = opponent_grid[cell_row][cell_column]
                            if (cell_content == "H"):
                                if (cell_being_processed in cells_processed):
                                    continue
                                number_of_hits_in_group += 1
                                cells_processed.append(cell_being_processed)
                                hits_in_group.append(cell_being_processed)
                                for adj_cell in get_adjacent_cells(cell_row, cell_column):
                                    cells_to_check.append(adj_cell)    
                            elif (cell_content == "M"):
                                continue
                            elif (cell_content == "N" or cell == "B"):
                                if (cell_being_processed in cells_processed):
                                    continue
                                opportunity_targets.append(cell_being_processed)
                                cells_processed.append(cell_being_processed)
                    if not opportunity_targets: # Group is a sunk ship or ships
                        if (number_of_hits_in_group == 2):
                            sunk_ships.append("ship_1x2")
                        elif (number_of_hits_in_group == 3):
                            sunk_ships.append("ship_1x3")
                        elif (number_of_hits_in_group == 4): 
                            sunk_ships.append("ship_1x4")
                        elif (number_of_hits_in_group == 6): 
                            min_row = 9
                            max_row = -1
                            min_column = 9
                            max_column = -1
                            for hit in hits_in_group:
                                row = hit[0]
                                column = hit[1]
                                if (min_row > row):
                                    min_row = row
                                if (max_row < row):
                                    max_row = row
                                if (min_column > column):
                                    min_column = column
                                if (max_column < column):
                                    max_column = column
                                if (max_row - min_row > 3 or max_column - min_column > 3):
                                    sunk_ships.append("ship_1x2")
                                    sunk_ships.append("ship_1x4")
                                else:
                                    sunk_ships.append("ship_2x3")
                        elif (number_of_hits_in_group == 7): 
                            sunk_ships.append("ship_1x3")
                            sunk_ships.append("ship_1x4")
                        elif (number_of_hits_in_group == 9): 
                            sunk_ships.append("ship_1x3") # Doesn't matter if it's 2 + 4 + 3 or 6 + 3 sunk
                        elif (number_of_hits_in_group == 10): 
                            sunk_ships.append("ship_1x4")
                            sunk_ships.append("ship_2x3")
                        elif (number_of_hits_in_group == 11): 
                            sunk_ships.append("ship_1x2")
                            sunk_ships.append("ship_1x3")
                            sunk_ships.append("ship_2x3")
                        elif (number_of_hits_in_group == 12): 
                            sunk_ships.append("ship_1x2")
                            sunk_ships.append("ship_1x4")
                            sunk_ships.append("ship_2x3")
                        elif (number_of_hits_in_group == 13): 
                            sunk_ships.append("ship_1x3")
                            sunk_ships.append("ship_1x4")
                            sunk_ships.append("ship_2x3")
                    hits_to_process.clear()
            return opportunity_targets, sunk_ships
        
        def select_next_target(opportunity_grid, target_list):
            #TODO: dummy function, fill with actual computation
            return shoot_cell_JSON(0, 0)
        
        #first move: use SP
        #INTEGRATED
        if is_blank and "SP" in available_abilities:
        #if blank grid, i.e. first move
            #do SP in the middleish of the board
            return {
                "combat": {
                    "cell": [0, 0],
                    "ability": {"SP": [3, 3]}
                }
            }

        #second turn: parse sonar and fire at any hits
        #INTEGRATED
        if is_blank and not ("SP" in available_abilities):
            #get sonar data
            SP_json = game_state.get("player_abilities")[0]
            info = SP_json.get("info").get("SP") #3-by-3 array
            for row in info:
                for json_col in row:
                    #if sonar detects a ship, shoot it
                    if row.get("result") == "Ship":
                        return shoot_cell_JSON(row.get("cell")[0], row.get("cell")[0])
                    else:
                        opponent_grid[row.get("cell")[0]][row.get("cell")[1]] = "M"
       
        #Use HS if we haven't already (i.e. if sonar didn't turn up ships)
        if "HS" in available_abilities:
            return {
                "combat": {
                    "cell": [0, 0],
                    "ability": {"HS": [0, 0]}
                }
            }
        
        #subsequent turns
        #1. look for shields
        #Integrated
        attack_shields_result = attack_shields(opponent_grid)
        if (attack_shields_result):
            return attack_shields_result
        
        #TODO: fill out select_next_target
        target_list, sunk_ships = get_opportunistic_targets(opponent_grid)
        if (target_list):
            return select_next_target(opponent_grid, target_list)

        #4. if no target lists
        PDF_grid = generate_PDF(opponent_grid, unsunk_from_sunk(sunk_ships))
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
