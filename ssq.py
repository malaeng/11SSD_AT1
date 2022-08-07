# Created by Malachi English 22/5/22
# Software Skills Quiz. Program asks multiple choice questions about skills used in software development.

import json
import random
import textwrap
import time
from utils import Display, Responses
display = Display()
responses = Responses()

class Ssq():
    def __init__(self):
        # Runs when Display() is initialized.
        # Sets up highscore once, at the start, and it is not overwritten.
        self.highscore = 0

    def main(self):
        # Runs the main game loop.
        # Asks questions num_questions times, and then runs the end() method.
        for i in range(self.num_questions):
            self.quiz()
        self.end()

    def start(self, name):
        # Sets up various variables.
        self.name = name
        self.score = 0
        self.num_questions = 5
        self.questions_not_done = []

        # Opens the questions file, and loads in the question bank.
        file = open("./quiz_questions.json")
        question_bank = json.load(file)
        for i in range(len(question_bank)):
            self.questions_not_done.append(i)
        file.close()

        self.introtext = f"Hi {self.name}. This is a quiz consisting of {self.num_questions} questions designed to test you on important skills in the software industry. You will be asked multiple choice questions and can answer either with the letter or number corresponding to your answer."

        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{'Software Skills Quiz'.center(display.width)}║
            ╠{'═' * display.width}╣"""))
        display.split_text(self.introtext)
        if responses.input_continue(): return

        self.main()


    def quiz(self):
        # Assumes that questions will only have a maximum of 6 answers.
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f']

        file = open("./quiz_questions.json")
        question_bank = json.load(file)
        question_index = random.choice(self.questions_not_done)
        question = question_bank[question_index]
        # Ensures program does not pick the same question more than once.
        self.questions_not_done.remove(question_index)
        
        # In the json file, the correct answer is always the first one.
        correct_answer = question[1][0]
        file.close()

        print(f"╔{'═' * display.width}╗")
        display.split_text(question[0])
        print(f"║{' ' * display.width}║")
        # Answers are shuffled.
        random.shuffle(question[1])
        for i in range(len(question[1])):
            display.split_text(alphabet[i] + ') ' + question[1][i])
        print(f"╚{'═' * display.width}╝")


        while True:
            answer = input('> ')
            if responses.check_for_quit(answer): return
            try:
                # Checks for character input (1, 2, 3, etc) - integer input
                # Checks that the number is within the correct range, and assigns the answer they picked to answer_text
                if int(answer) <= len(question[1]):
                    answer_text = question[1][int(answer)-1]
                    break
                else:
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║ {' ERROR. PLEASE TRY AGAIN '.center((display.width-2), '!')} ║
                        ╚{'═' * display.width}╝"""))
            except ValueError:
                # Checks for character input ('a', 'b', etc) - string input
                # Makes sure character is one of the options, and assigns the answer they picked to answer_text
                if answer in alphabet[:len(question[1])]:
                    answer_text = question[1][alphabet.index(answer)] 
                    break
                else:
                    print(textwrap.dedent(f"""\
                        ╔{'═' * display.width}╗
                        ║ {' ERROR. PLEASE TRY AGAIN '.center((display.width-2), '!')} ║
                        ╚{'═' * display.width}╝"""))

        if answer_text == correct_answer:
            self.score += 1
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║ {' CORRECT! '.center((display.width-2), ':')} ║
                ║{' ' * display.width}║"""))
        else:
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║ {' INCORRECT '.center((display.width-2), ':')} ║
                ║{' ' * display.width}║"""))
        # Provides a breif explanation of the answer.
        display.split_text(question[2])
        if responses.input_continue(): return

    def end(self):
        # Calculates score percentage.
        score_percent = (self.score / self.num_questions) * 100
        print(textwrap.dedent(f"""
            ╔{'═' * display.width}╗
            ║ {' SCORE '.center((display.width-2), ':')} ║
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
