# Created by Malachi English 22/5/22
# Maze Game with a randomly generated navigatable maze and random events.

import random
import json
import textwrap
import time
from utils import Display, Responses
display = Display()
responses = Responses()

class Mg:
    def main(self):
        # Runs the actual game loop.
        self.display_main()
        while self.game_running:
            self.navigation()
            if self.game_running: # Checks game is running again because player may have died in navigation.
                self.display_main()

    def start(self,name):
        # Runs before main to set up various variables and introduce the game.
        self.name = name
        self.player_health = 100
        self.player_combat_ability = 5
        self.player_gold = 0

        self.rooms_explored = 0
        self.fights = 0

        self.game_running = True

        self.mazesize = 9
        self.halfmazesize = int((self.mazesize / 2) - 0.5)
        self.halfmazesize2 = int((self.mazesize) - 0.5)
        # Player_location[0] = y (vertical), player_location[1] = x (horizontal)
        self.player_location = [self.halfmazesize, self.halfmazesize2]

        # not currently used.
        self.exit_pairs = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

        self.tile_exits = {
            '┼': ['n', 's', 'e', 'w', 'north', 'south', 'east', 'west'],
            '│': ['n', 's', 'north', 'south'],
            '┤': ['n', 's', 'w', 'north', 'south', 'west'],
            '┐': ['s', 'w', 'south', 'west'],
            '└': ['n', 'e', 'north', 'east'],
            '┴': ['n', 'e', 'w', 'north', 'east', 'west'],
            '┬': ['s', 'e', 'w', 'south', 'east', 'west'],
            '├': ['n', 's', 'e', 'north', 'south', 'east'],
            '─': ['e', 'w', 'east', 'west'],
            '┘': ['n', 'w', 'north', 'west'],
            '┌': ['s', 'e', 'south', 'east'],
            ' ': []
        }

        self.tiles = list(self.tile_exits)

        # Creates the maze grid
        self.mazemap = []
        for i in range(self.mazesize):
            self.mazemap.append([])
            for j in range(self.mazesize*2-1):
                self.mazemap[i].append(' ')

        # Starting tile is always a crossroads.
        self.change_map_tile('┼', False, False)

        self.introtext = f"Hi {self.name}. This is a game where you navigate a procedurally generated maze to try to get to the end. You start in the middle of the maze and can win by getting to any of the four edges. The maze is {self.mazesize} tiles across (vertically and horizontally). To navigate the maze, use the four cardinal directions ('n', 's', 'e', 'w'). Along the way, you may encounter various items or enemies, where you will be given a choice. Wisdom, Strategy, and a bit of luck will get you to the end. Good luck, {self.name}."

        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{'Maze Game'.center(display.width)}║
            ╠{'═' * display.width}╣"""))
        display.split_text(self.introtext)
        if responses.input_continue(): return

        self.main()

    def get_map_tile(self):
        # Returns the string representing the map tile that the player is currently on.
        # Looks through the mazemap variable at the player's x and y locations.
        return self.mazemap[self.player_location[0]][self.player_location[1]]

    def change_map_tile(self, tile, wc, ec):
        # Runs during generation. Also when marking player location. 

        # Replaces current tile with new tile.
        self.mazemap[self.player_location[0]][self.player_location[1]] = tile

        # Adds 'bridges' to the left and right if needed.
        if self.mazemap[self.player_location[0]][self.player_location[1] - 2] != ' ' and wc:
            self.mazemap[self.player_location[0]][self.player_location[1] - 1] = '─'

        elif self.mazemap[self.player_location[0]][self.player_location[1] + 2] != ' ' and ec:
            self.mazemap[self.player_location[0]][self.player_location[1] + 1] = '─'


    def navigation(self):

        while True:
            # Gets user input. Expecting 'n', 'north', 's', 'south', etc.
            direction = input('> ').lower()

            if responses.check_for_quit(direction):
                # Quits to menu if user inputs a quit keyword. 
                self.game_running = False
                return

            if direction in self.tile_exits[self.get_map_tile()]:
                try:
                    if direction == 'n' or direction == 'north':
                        self.player_location[0] -= 1

                        # Checks if player has reached the top of the maze.
                        if self.player_location[0] < 0:
                            print(textwrap.dedent(f"""\
                                ╔{'═' * display.width}╗
                                ║{("You have reached the end of the maze!").center(display.width)}║
                                ╚{'═' * display.width}╝"""))

                            time.sleep(1)
                            self.end_game("win")
                            break

                        self.generate_tile('n')
                        break

                    elif direction == 's' or direction == 'south':
                        self.player_location[0] += 1
                        self.generate_tile('s')
                        break

                    # East and West go forward/back by 2, because there is a divider between tiles to make the map look more square.
                    elif direction == 'e' or direction == 'east':
                        self.player_location[1] += 2
                        self.generate_tile('e')
                        break

                    elif direction == 'w' or direction == 'west':
                        self.player_location[1] -= 2

                        # Checks if user has reached the far left of the maze.
                        if self.player_location[1] < 0:
                            print(textwrap.dedent(f"""\
                                ╔{'═' * display.width}╗
                                ║{("You have reached the end of the maze!").center(display.width)}║
                                ╚{'═' * display.width}╝"""))

                            time.sleep(1)
                            self.end_game("win")
                            break

                        self.generate_tile('w')
                        break

                except IndexError:
                    # This will run if the user has reached the bottom or far right of the maze,
                    # because the function will try and call a number that is too high.
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║{("You have reached the end of the maze!").center(display.width)}║
                        ╚{'═' * display.width}╝"""))
                    time.sleep(1)
                    self.end_game("win")
                    break

            elif self.get_map_tile() == ' ':
                # This should never happen. 
                self.unlucky_event()
            else:
                # Runs if user has not inputted one of the four cardinal directions or cannot go in the inputted diretion.
                valid_exits = []
                for i in self.tile_exits[self.get_map_tile()]:
                    if len(i) == 1: valid_exits.append(i)
                valid_exits_string = ', '.join(valid_exits)
                print(textwrap.dedent(f"""
                        ╔{'═' * display.width}╗
                        ║{(' Invalid input. ').center(display.width)}║
                        ║{' ' * display.width}║
                        ║{(' The current valid movement options are: ' + valid_exits_string).center(display.width)}║
                        ╚{'═' * display.width}╝"""))


    def generate_tile(self, direction):

        # Don't generate a tile if there is already one there.
        if self.get_map_tile() != ' ':
            return

        self.rooms_explored += 1

        needed_exits = []
        invalid_exits = []

        west_connection = True
        east_connection = True

        west_tile = self.mazemap[self.player_location[0]][self.player_location[1] - 2]
        east_tile = self.mazemap[self.player_location[0]][self.player_location[1] + 2]
        north_tile = self.mazemap[self.player_location[0] - 1][self.player_location[1]]
        south_tile = self.mazemap[self.player_location[0] + 1][self.player_location[1]]

        # The current location is the tile that needs to be generated.
        # The program checks all the surrounding tiles.
        # If a tile contains an exit towards the current tile, an exit is needed there.
        # If a tile has been generated but there is no exit towards the current tile, 
        # an exit can't go there, and a connection isn't placed (for vertical connections)
        # With this information, random tiles are tested until one is found that fits the 
        # requirements, at which point it is placed on the map (more detail below)

        # Checks tile to the west
        if 'e' in self.tile_exits[west_tile]:
            needed_exits.append('w')
        elif west_tile != ' ':
            invalid_exits.append('w')
            west_connection = False

        # Checks tile to the east
        if 'w' in self.tile_exits[east_tile]:
            needed_exits.append('e')
        elif east_tile != ' ':
            invalid_exits.append('e')
            east_connection = False

        # Checks tile to the north
        if 's' in self.tile_exits[north_tile]:
            needed_exits.append('n')
        elif north_tile != ' ':
            invalid_exits.append('n')

        # Checks tile to the south
        if 'n' in self.tile_exits[south_tile]:
            needed_exits.append('s')
        elif south_tile != ' ':
            invalid_exits.append('s')
        
        for i in range(999):
            # Generates a random tile
            # If the tile meets the tile_exits requirements (needed_exits and invalid_exits),
            # the tile is placed. Otherwise a new random tile is tested.
            tile = random.choice(self.tiles)

            if all(i in self.tile_exits[tile] for i in needed_exits): # Checks tile has all needed exits
                if not any(i in self.tile_exits[tile] for i in invalid_exits): # Checks tile has no invalid exits
                    self.change_map_tile(tile, west_connection, east_connection) # If all above requirements have been met, place tile.
                    break

            elif i == 999:
                #  if gets to the end of loop, special event. Only if all three surrounding
                #  tiles have no tile_exits, or extreme unlikely rng
                self.unlucky_event()

        # After the tile is generated, the event function is run.
        self.event()
        
    def display_main(self):
        # doors default as closed.
        n, s, e, w = "─", "─", "│", "│"
        # If the doors are in the tile_exits, replace with door character.
        doors = self.tile_exits[self.get_map_tile()]
        if "n" in doors:
            n = "■"
        if "s" in doors:
            s = "■"
        if "e" in doors:
            e = "■"
        if "w" in doors:
            w = "■"

        # '\n' doesn't work in f-strings.
        nl = '\n'
        room = textwrap.dedent(f"""\
            {' ' + nl * int((self.mazesize - 5) / 2 - 1)}
            ┌───{n}───┐
            │       │
            {w}       {e}
            │       │
            └───{s}───┘{(' ' + nl) * int((self.mazesize - 5) / 2)}""")

        split_room = room.split('\n')

        self.mark_player_location()

        split_map = []

        # Converts maze into a list containing a string for each row in the maze.
        mazeline = ''
        for i in range(self.mazesize):
            for j in range(self.mazesize*2-1):
                mazeline += self.mazemap[i][j]
            split_map.append(mazeline)
            mazeline = ''

        self.unmark_player_location()

        # Prints the headings
        print(textwrap.dedent(f"""\
            ╔{'═' * display.halfwidth}╦{'═' * display.halfwidth}╗ 
            ║{' CURRENT ROOM '.center(display.halfwidth)}║{' MAP '.center(display.halfwidth)}║ 
            ╠{'═' * display.halfwidth}╬{'═' * display.halfwidth}╣"""))

        # Prints the current room and the maze.
        # Output will be as tall as the maze. 'split_room' has already been made to have an equal height as the maze.
        for i in range(self.mazesize):
            print(f"║{split_room[i].center(display.halfwidth)}║{split_map[i].center(display.halfwidth)}║")

        # Prints stats - health, combat ability, gold
        print(textwrap.dedent(f"""\
            ╠{'═' * display.halfwidth}╩{'═' * display.halfwidth}╣
            ║{' ' * display.width}║
            ║  {('Health: ' + str(self.player_health) + '/100' + '   ' + 'Comabt Ability: ' + str(self.player_combat_ability) + '   ' + 'Gold: ' + str(self.player_gold)).ljust(display.width - 2)}║
            ║{' ' * display.width}║
            ╚{'═' * display.width}╝"""))


    
    def mark_player_location(self):
        # Stores the current tile as a global variable, so it can be replaced later.
        global replaced_tile
        # Checks player is in the bounds of the maze, and that the tile has not already been marked.
        if self.get_map_tile() != '■' and self.player_location[0] >= 0 and self.player_location[1] >= 0:
            replaced_tile = self.get_map_tile()
            # Changes player tile to '■'
            self.change_map_tile('■', False, False)


    def unmark_player_location(self):
        # Checks that the maze tile has been marked
        if self.get_map_tile() == '■':
            # Replaces tile with global variable defined in mark_player_location
            self.change_map_tile(replaced_tile, False, False)

    def combat(self, enemy, enemy_skill):
        # If player's combat ability is equal to the enemy's, the player loses 15 health.
        # If enemy is more or less skilled than the player, the player loses more or less than 15 health respectively.
        damage_taken = round((enemy_skill / self.player_combat_ability) * 15)
        self.player_health -= damage_taken

        # Player's combat ability increases based on the enemy's skill
        skill_increase = round(enemy_skill / 10) + 1
        self.player_combat_ability += skill_increase

        # Player earns gold based on the enemy's skill.
        gold_earned = random.randint(1, enemy_skill) * 5
        self.player_gold += gold_earned

        # Fixes grammatical issue.
        if enemy == "witches": enemy = "group of witches"

        # Gives player feedback on the encounter.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{f"You fight against a level {enemy_skill} {enemy} and lose {damage_taken} health.".center(display.width)}║
            ║{f"You now have {self.player_health} health remaining.".center(display.width)}║
            ║{f"Your Comabat ability has increased by {skill_increase}.".center(display.width)}║
            ║{f"You gain {gold_earned} gold.".center(display.width)}║"""))
        if responses.input_continue(): return

        self.fights += 1

    def flee(self, enemy, enemy_skill):
        escape_chance = random.randint(0, 100)
        damage_taken = 0

        # 65% chance to escape
        if escape_chance > 35: 
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║{("You Escape").center(display.width)}║"""))
            if responses.input_continue(): return

        # 5% chance to lose half of all health.    
        elif escape_chance < 5:
            print(f"╔{'═' * display.width}╗")
            display.split_text(f"You try to run, but you are not fast enough. The {enemy} catches up and overwhelms you.")
            if responses.input_continue(): return
            damage_taken = round(self.player_health / 2)
            self.player_health -= damage_taken

        # 30% chance to be forced into combat.    
        else:
            print(f"╔{'═' * display.width}╗")
            display.split_text(f"The {enemy} catches up to you, and, turning around to defend yourself, you are forced into combat.")
            if responses.input_continue(): return
            self.combat(enemy, enemy_skill)
            

    def riddle(self, enemy, enemy_skill):
        file = open("./maze_riddles.json")
        riddle_data = json.load(file)
        riddle = random.choice(riddle_data)
        file.close()

        # Prints the riddle
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║ {f" {enemy}'s riddle ".center((display.width-2), ':')} ║
            ║{' ' * display.width}║"""))
        display.split_text(riddle[0])
        print(f"╚{'═' * display.width}╝")

        response = input('> ').lower()

        # quits to menu if user entered a quit keyword.
        if responses.check_for_quit(response): 
            self.game_running = False
            return

        # Checks if response is correct
        if response in riddle[1]:
            # allow vs allows. English is a difficult language.
            if enemy == "witches": plural = ''
            elif enemy == "sphynx": plural = 's'

            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║{(f"The {enemy} allow{plural} you to pass.").center(display.width)}║"""))
            if responses.input_continue(): return

        else:
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║{("You answered incorrectly").center(display.width)}║
                ║{("The correct answer is " + riddle[1][1]).center(display.width)}║"""))

            if responses.input_continue(): return

            self.combat(enemy, enemy_skill)

    def end_game(self, winorlose):
        # Checks if player has won or lost.
        if winorlose == "win":
            message = " You Win! "
        elif winorlose == "lose":
            message = " You Lose. "

        # Prints win/lose message and stats
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{message.center(display.width, ':')}║
            ║{' ' * display.width}║
            ║{"    Stats".center(display.width)}║
            ║{("    Gold: " + str(self.player_gold)).ljust(display.width)}║
            ║{("    Rooms explored: " + str(self.rooms_explored)).ljust(display.width)}║
            ║{("    Monsters fought: " + str(self.fights)).ljust(display.width)}║
            ║{("    Combat ability: " + str(self.player_combat_ability)).ljust(display.width)}║"""))

        if responses.input_continue(): return
        # Sets game_running to false, meaning the main game loop with stop.
        self.game_running = False

        responses.ask_to_play_again(self.start, self.name)

    def unlucky_event(self):
        # Used in some places to try and avoid bugs. e.g. when cannot generate a tile.
        # Ends the game.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{("You get struck by lightning and die.").center(display.width)}║
            ╚{'═' * display.width}╝"""))
        self.end_game("lose")        

    def event(self):
        event_chance = random.randint(1, 10)
        # 20% chance for an event not to occur.
        if event_chance > 8: return

        file = open("./maze_encounters.json")
        event_data = json.load(file)
        this_event = random.choice(event_data)
        file.close()

        # Prints the event text.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║ {(' ' + this_event["name"] + ' ').center((display.width-2), ':')} ║
            ║{' ' * display.width}║"""))
        display.split_text(this_event["text"])

        # Gets both options from the data file.
        option_1 = this_event["option1"]
        option_2 = this_event["option2"]

        # Prints both of the options
        print(textwrap.dedent(f"""\
            ╠{'═' * display.halfwidth}╦{'═' * display.halfwidth}╣
            ║{("(1) " + option_1).center(display.halfwidth)}║{("(2) " + option_2).center(display.halfwidth)}║
            ╚{'═' * display.halfwidth}╩{'═' * display.halfwidth}╝"""))

        while True:
            response = input('> ')

            if responses.check_for_quit(response): 
                self.game_running = False
                return

            if response == '1' or response == this_event['option1']:
                outcome = this_event['option1_outcomes']
                break

            elif response == '2' or response == this_event['option2']:
                outcome = this_event['option2_outcomes']
                break

            else:
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{(" Invalid Input. Please Try Again.").center(display.width)}║
                    ╚{'═' * display.width}╝"""))

        if outcome[0] == 'INCREASE_STAT':
            # Checks the second item in the 'outcome' list to see what stat to increase.

            # Increase combat_ability
            if outcome[1] == 'COMBAT_ABILITY':
                increase = round(this_event['basecombatincrease'] * random.randint(5, 15) / 10)
                self.player_combat_ability += increase

                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{("Combat ability increased by " + str(increase)).center(display.width)}║
                    ╚{'═' * display.width}╝"""))

            # Increases Gold
            elif outcome[1] == "GOLD":
                increase = round(this_event['basegoldincrease'] * random.randint(5, 15))
                self.player_gold += increase

                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{("Gold increased by " + str(increase)).center(display.width)}║
                    ╚{'═' * display.width}╝"""))

            # Increases Health.
            elif outcome[1] == "HEALTH":
                increase = round(this_event['basehealthincrease'] * random.randint(5, 15) / 5)
                self.player_health += increase

                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{("Health increased by " + str(increase)).center(display.width)}║
                    ╚{'═' * display.width}╝"""))

        elif outcome[0] == "COMBAT":
            # Gets difficulty from data file and runs combat method.
            difficulty = round(random.randint(this_event['difficultyrange'][0], this_event['difficultyrange'][1]))
            self.combat(this_event['name'], difficulty)

        elif outcome[0] == "FLEE":
            # Gets difficulty from data file and runs flee method.
            difficulty = round(random.randint(this_event['difficultyrange'][0], this_event['difficultyrange'][1]))
            self.flee(this_event['name'], difficulty)

        elif outcome[0] == "RIDDLE":
            # Gets difficulty from data file and runs riddle method.
            difficulty = round(random.randint(this_event['difficultyrange'][0], this_event['difficultyrange'][1]))
            self.riddle(this_event['name'], difficulty)

        else: 
            # If a function was not provided to be run, print the text instead.
            print(f"╔{'═' * display.width}╗")
            display.split_text(outcome[0])
            if responses.input_continue(): return

        # After the event has occured, checks if player has died.
        if self.player_health < 0:
            self.end_game("lose")
