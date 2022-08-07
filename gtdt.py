# Created by Malachi English 22/5/22
# Guess The Data Type game. Program gives an example of a data type and user has to try and guess it.

import random
import time
import textwrap
import json
from utils import Display, Responses
display = Display()
responses = Responses()

class Gtdt:
    def __init__(self):
        self.highscore = 0

        # Questions that could be asked. Ideally this would be in a separat json file, but
        # use of random numbers makes that more complicated to do.
        self.question_bank = [
        "'one'", "'word'", '"False"', "'9.5'", '"[1, 2, 3]"', f'"{random.randint(1, 100)}"', '"""Hello world"""',
        random.randint(-10, 10), random.randint(-100, 100), random.randint(1, 1000),
        random.randint(100, 10000) / 100, random.randint(100, 1000) / 100,
        True, False,
        [1, 2, 3], ['a', 'b', 'c'], ["one", 1, "two", 2],
        {'one':'two', 'three':'four'}, {"year": 2022, "income": 1234},
        ('one', 'two'), (1, 2, 3),
        {1, 2, 3}, {'a', 'b', 'c'}
        ]

        file = open("./gtdt_data.json")
        self.correct_responses = json.load(file)
        file.close()

    def start(self, name):
        self.name = name
        self.score = 0
        introtext = f"Hi {self.name}. This is a quiz game where you have to enter the data type displayed to you. Data types being tested in this game are: ... You will have 3 tries for each question. Your score will be a percentage of how many you got correct. Press enter to begin."

        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{'Guess The Data Type'.center(display.width)}║
            ╠{'═' * display.width}╣"""))

        display.split_text(introtext)

        if responses.input_continue(): return

        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║ {' Enter The Number of Questions '.center((display.width-2), ':')} ║
            ║{' ' * display.width}║"""))

        display.split_text("Maximum 50 questions. You can always enter 'Q' to quit.")

        print(textwrap.dedent(f"""\
            ║{' ' * display.width}║
            ╚{'═' * display.width}╝"""))
        while True:
            # Checks input is an integer, and clamps it to the min/max values of 1 and 50
            self.num_questions = input('> ')
            if responses.check_for_quit(self.num_questions): return
            try:
                plural = 's'
                self.num_questions = int(self.num_questions)
                if self.num_questions > 50:
                    self.num_questions = 50
                elif self.num_questions <= 1:
                    # Ensures input is not negative or zero
                    self.num_questions = 1
                    # Removes the 's' to keep the message grammatically correct.
                    plural = ''
                
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║{' ' * display.width}║
                    ║{f"You will be asked {self.num_questions} question{plural}.".center(display.width)}║
                    ║{' ' * display.width}║
                    ╚{'═' * display.width}╝"""))

                for i in range(self.num_questions):
                    self.ask_question()
                self.finish()
                break

            except ValueError:
                    # Runs if input cannot be converted to int
                    print(textwrap.dedent(f"""
                        ╔{'═' * display.width}╗
                        ║ {' Invalid Input '.center((display.width-2), '!')} ║
                        ╚{'═' * display.width}╝"""))

    def ask_question(self):
        chancescounter = 0
        # Gets a random question from the question bank.
        question = random.choice(self.question_bank)

        print(textwrap.dedent(f"""
            ╔{'═' * display.width}╗
            ║ {' What data type is this? '.center((display.width-2), ':')} ║
            ║{' ' * display.width}║
            ║{str(question).center(display.width)}║
            ║{' ' * display.width}║
            ╚{'═' * display.width}╝"""))

        while True:
            answer = input('> ')
            if responses.check_for_quit(answer): return
            # Looks up the type of the data type in the correct_responses dictionary.
            # Checks if user input is in the dictionary (if it is correct)
            elif answer in self.correct_responses[str(type(question))][0]:
                self.score += 1
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║ {' Correct! '.center((display.width-2), ':')} ║
                    ║{' ' * display.width}║"""))

                # Provides a breif explanation of the data type using data from the json file.
                display.split_text(str(self.correct_responses[str(type(question))][1]).center(display.width))
                print(f"╚{'═' * display.width}╝")
                time.sleep(2)
                break

            elif chancescounter < 2:
                # This runs for the user's first and second chances.
                # For each time they get it wrong, one-third of a point is removed from the whole point they get if they get it correct.
                self.score -= (1/3)
                chancescounter +=1
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║ {' Incorrect. '.center((display.width-2), ':')} ║
                    ║{' ' * display.width}║
                    ║{f"you have used up {chancescounter}/3 chances.".center(display.width)}║
                    ║{' ' * display.width}║
                    ╚{'═' * display.width}╝"""))

            else:
                # The last chance has been used up.
                # By this point, 2/3 points have been removed, so this makes sure negative points aren't being taken away.
                # If the user had gotten their second or last chance correct, 1 point would have been added to the negative number making it positive.
                self.score += (2/3)
                correct_answer = self.correct_responses[str(type(question))][0][0]
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║ {' Incorrect. '.center((display.width-2), ':')} ║
                    ║{' ' * display.width}║
                    ║{f"you have used up 3/3 chances.".center(display.width)}║
                    ║{' ' * display.width}║
                    ║{f"The correct answer is: {correct_answer}.".center(display.width)}║"""))

                # Provides a brief explanation of the data type.
                display.split_text(str(self.correct_responses[str(type(question))][1]).center(display.width))
                print(f"╚{'═' * display.width}╝")
                time.sleep(2)
                break

    def finish(self):
        # Calculates the score percentage
        score_percent = (self.score / self.num_questions) * 100
        print(textwrap.dedent(f"""
            ╔{'═' * display.width}╗
            ║ {' Score '.center((display.width-2), ':')} ║
            ║{' ' * display.width}║
            ║{f"You scored {round(score_percent, 2)}%".center(display.width)}║"""))
        # Provides a message based on the users score.
        if score_percent < 15:
            display.split_text("Bad luck. Keep practicing, and you will do better.".center(display.width))
        elif score_percent < 50:
            display.split_text("A good effort, but still with room to improve.".center(display.width))
        elif score_percent < 80:
            display.split_text("A good score.".center(display.width))
        elif score_percent < 100:
            display.split_text("Amazing! pat yourself on the back.".center(display.width))
        elif score_percent > 99:
            display.split_text("A perfect score! well done.".center(display.width))
        else:
            display.split_text("That's a weird score.".center(display.width))
        print(textwrap.dedent(f"""\
            ║{' ' * display.width}║
            ╚{'═' * display.width}╝"""))
        time.sleep(2)

        responses.ask_to_play_again(self.start, self.name)

