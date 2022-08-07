# Created by Malachi English 22/5/22
# Guess The Number game. Program has a random secret number and user tries to guess it.

import time
import random
import textwrap
from utils import Display, Responses

display = Display()
responses = Responses()

class Gtn:
    def __init__(self):
        # Runs when Gtn() is initialized.
        # Sets up highscore once, at the start, and it is not overwritten.
        self.highscore = 0

    def start(self, name):
        # Says hello to user, explains the game.
        self.name = name
        introtext = f"Hi {self.name}. I'm thinking of a number between 1 and 100. When you are ready, enter your guesses, and I will tell you whether you are higher, lower, or have guessed my number. You score is based on the amount of guesses you make and the real time in which you guess the correct number. For a good score, aim to guess quickly but with as little guesses as possible. Press enter to continue."

        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{'Guess The Number'.center(display.width)}║
            ╠{'═' * display.width}╣"""))
        display.split_text(introtext)

        if responses.input_continue(): return

        # Starts the main game loop.
        self.game_loop()

    def game_loop(self):
        guess = 0
        secret_number = random.randint(1, 100)
        guesses = 0
        # records the time when the game loop starts.
        start = time.time()
        while True:
            guess = input('> ')
            if responses.check_for_quit(guess): return
            try:
                guess = int(guess)
                if guess > secret_number:
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║ {' LOWER '.center((display.width-2), '«')} ║
                        ╚{'═' * display.width}╝"""))

                elif guess < secret_number:
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║ {' HIGHER '.center((display.width-2), '»')} ║
                        ╚{'═' * display.width}╝"""))

                elif guess == secret_number:
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║ {' CORRECT! '.center((display.width-2), ':')} ║
                        ╚{'═' * display.width}╝"""))
                    break

                else:
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║ {' Error. Please try again. '.center((display.width-2), '!')} ║
                        ╚{'═' * display.width}╝"""))
                    # The guesses counter goes up by default, so this makes it 0 if there is an error.
                    guesses -= 1
                guesses += 1
            except ValueError:
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║ {' Invalid Input '.center((display.width-2), '!')} ║
                    ╚{'═' * display.width}╝"""))

        # Records the time when the game loop ends.
        end = time.time()
        time_elapsed = round((end - start), 2)
        if time_elapsed <= 0:
            time_elapsed = 1
        # Dividing 100 by the values makes it so a smaller value results in a better score.
        # Plus 1 negates any dividing by 0 errors (hopefully)
        score = int((100/guesses+1)*(100/time_elapsed+1))
        if score > self.highscore:
            self.highscore = score
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{'Your Score'.center(display.width)}║
            ╠{'═' * display.width}╣
            ║{(' Guesses: ' + str(guesses)).ljust(display.width)}║  
            ║{(' Time: ' + str(time_elapsed)).ljust(display.width)}║
            ║{' ' * display.width}║
            ║{(' Final Score: ' + str(score)).ljust(display.width)}║    
            ║{(' High Score: '+ str(self.highscore)).ljust(display.width)}║
            ╚{'═' * display.width}╝"""))
        time.sleep(2)

        responses.ask_to_play_again(self.start, self.name)
