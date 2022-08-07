# Created by Malachi English...
# Game select and help function. This is the program that is run to access the other programs.

# NOTICE: keep in mind screen size when running the program. 
# A too small screen size could result in weird/messy output, due to the borders.

# Complete project can be found here: https://replit.com/join/bbmwqkgedd-malaeng
# If running yourself, ensure all .py and .json files are located in the same directory.

import textwrap
# Imports all the classes from other files.
from mg import Mg
from gtn import Gtn
from gtdt import Gtdt
from ssq import Ssq
from utils import Display, Responses

mg = Mg()
gtn = Gtn()
gtdt = Gtdt()
ssq = Ssq()
display = Display()
responses = Responses()

class Main:
    
    def start(self):
        while True:
            print()
            print()
            print("This program uses borders")
            print("Having a small screen size could mess up the output.")
            print("Ensure the below arrow does not wrap around the screen:")
            print()
            print("<" + "-" * display.width + ">")
            print()
            print("Press Enter to continue...")
            input()
            # Asks for user's name and stores it in 'self.username'
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║{' Please Enter your name '.center((display.width))}║
                ╚{'═' * display.width}╝"""))
            self.user_name = input('> ').title()

            if self.user_name == '':
                # Ensures User does not press enter without entering a name.
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{' Invalid input '.center((display.width))}║
                    ╚{'═' * display.width}╝"""))

            else: break
        self.main()

    def main(self):
        # Says hello to user.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{(' Hello, ' + self.user_name).center((display.width))}║
            ╚{'═' * display.width}╝"""))

        # Gives options to user.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{' Please select an option using the numbers provided '.center((display.width))}║
            ╠{'═' * display.width}╣
            ║{'   (1) Help '.ljust((display.width))}║
            ║{'   (2) Guess the number '.ljust((display.width))}║
            ║{'   (3) Guess the datatype '.ljust((display.width))}║
            ║{'   (4) Software skills quiz '.ljust((display.width))}║
            ║{'   (5) Maze game '.ljust((display.width))}║
            ║{'   (6) Quit '.ljust((display.width))}║
            ╚{'═' * display.width}╝"""))

        # Runs program correlating with input number.
        while True:
            choice = input('> ')
            if choice == '1':
                self.help()
                break
            elif choice == '2':
                gtn.start(self.user_name)
                break
            elif choice == '3':
                gtdt.start(self.user_name)
                break
            elif choice == '4':
                ssq.start(self.user_name)
                break
            elif choice == '5':
                mg.start(self.user_name)
                break
            elif choice == '6' or choice in responses.quit_responses:
                quit()
            else:
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{' Invalid input '.center((display.width))}║
                    ╚{'═' * display.width}╝"""))
        self.main()

    def help(self):
        # Prints info on the program as a whole, then gives options for user to selectively learn about more in detail.
        print(f"╔{'═' * display.width}╗")
        display.split_text("This is a collection of text based games, which are played by entering numbers or letters on the keyboard to select different options.")
        display.split_text("All games have deeper explanations of the gameplay/rules when you run them. You can enter 'quit' at any time to exit the games.")
        display.split_text("Select on option to learn more about it.")
        print(textwrap.dedent(f"""\
            ║{' ' * display.width}║
            ║{'   (1) Back to game select '.ljust((display.width))}║
            ║{'   (2) Guess the number '.ljust((display.width))}║
            ║{'   (3) Guess the datatype '.ljust((display.width))}║
            ║{'   (4) Software skills quiz '.ljust((display.width))}║
            ║{'   (5) Maze game '.ljust((display.width))}║
            ╚{'═' * display.width}╝"""))

        # Gives information on the option the user selected.
        while True:
            choice = input('> ')
            if choice == '1':
                self.main()
                break
            elif choice == '2':
                print(f"╔{'═' * display.width}╗")
                display.split_text("'Guess the number' is a game where the computer has a secret random number that you have to try and guess in the least amount of attempts and in the quickest time. The computer gives you hints to help you guess the number.")
                if responses.input_continue(): return
                break
            elif choice == '3':
                print(f"╔{'═' * display.width}╗")
                display.split_text("'Guess the datatype' is a game where you are quizzed on datatypes used in python")
                if responses.input_continue(): return
                break
            elif choice == '4':
                print(f"╔{'═' * display.width}╗")
                display.split_text("'Software Skills Quiz' is a game where you are quizzed on skills needed in the software industry.")
                if responses.input_continue(): return
                break
            elif choice == '5':
                print(f"╔{'═' * display.width}╗")
                display.split_text("'Maze Game' is a game where you have to try and escape a randomly generated maze filled with loot and various monsters.")
                if responses.input_continue(): return
                break
            elif choice in responses.quit_responses:
                quit()
            else:
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{' Invalid input '.center((display.width))}║
                    ╚{'═' * display.width}╝"""))
        self.help()


# Runs the program.
if __name__ == '__main__':
    main = Main()
    main.start()