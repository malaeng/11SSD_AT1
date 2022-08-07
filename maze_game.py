
health = 300
maxhealth = 100
attack = 300
defence = 5
# combine attack and defence into 'combat ability' or something. Simplifies it a bit.

# After some reflection, top down seems more easier to understand, and implement (depending on how I do it)
# make the game 'endless', with high score? keeps getting harder and harder and stuff.
# a high score system would be cool at least, considering the context of the game. even if it's not endless.


# current_movement_options = ['(f)orward', '(b)ack', '(l)eft', '(r)ight']

# forward --> -rowlength
# backward --> +rowlength
# left --> -1
# right --> +1
mazemap = [
6, 2, 5, 
3, 0, 1,
7, 8, 4
]

maze_size = 3
mazelocation = 7
mazeview = 8

(13 * mazelocation) + 2
current_graphic = []
current_movement_options = []

def update_graphic():
    global GUI
    global current_movement_options
    current_graphic = []
    current_movement_options = []
    current_movement_options_brackets = ["", "", "", ""]
    with open('AT1/maze_graphics.txt') as graphics:
        lines = graphics.readlines()
        for line in lines[(14 * mazeview) + 1:(14 * mazeview) + 2]:
            current_movement_options = line.strip().split(", ")

            # Adds brackets to first character of each item in current_movement_options
            for i in range(len(current_movement_options)): 
                current_movement_options_brackets[i] = '(' + current_movement_options[i][0] + ')' + current_movement_options[i][1:]

            # Ensures list has length of 4
            while True: 
                if len(current_movement_options) < 4: current_movement_options.append("")
                else: break

        for line in lines[(14 * mazeview) + 2:(14 * mazeview) + 13]:
            current_graphic.append(line[:-1])
    graphics.close()
    GUI = f"""
888888888[Graphic]88888888888888888[STATS]8888888888
88    {current_graphic[0]}    88                       88 
88    {current_graphic[1]}    88  health:  {(str(health) + "/" + str(maxhealth)).ljust(7)}     88
88    {current_graphic[2]}    88  attack:  {str(attack).ljust(5)}       88
88    {current_graphic[3]}    88  defence: {str(defence).ljust(4)}        88
88    {current_graphic[4]}    88                       88
88    {current_graphic[5]}    88888[Movement options]8888
88    {current_graphic[6]}    88                       88
88    {current_graphic[7]}    88  {current_movement_options_brackets[0].ljust(9)} {current_movement_options_brackets[1].ljust(9)}  88
88    {current_graphic[8]}    88                       88
88    {current_graphic[9]}    88  {current_movement_options_brackets[2].ljust(9)} {current_movement_options_brackets[3].ljust(9)}  88
88    {current_graphic[10]}    88                       88
8888888888888888888888888888888888888888888888888888
"""
    print(GUI)

def start():
    print(r"""
====================================================
 _   _                                     
| |_| |__   ___    _ __ ___   __ _ _______ 
| __| '_ \ / _ \  | '_ ` _ \ / _` |_  / _ \
| |_| | | |  __/  | | | | | | (_| |/ /  __/
 \__|_| |_|\___|  |_| |_| |_|\__,_/___\___|

====================================================                                       
    """)


def navigation():
    global mazelocation
    global mazeview
    toskipforward = []
    toskipbackward = []
    togoback = []
    togoforward = []
    valid_options = list(filter(None, current_movement_options))
    for i in range(len(valid_options)):
        valid_options.append(current_movement_options[i][0])
    while True:
        direction = input("> ").lower()
        if direction in valid_options:
            if direction == "f" or direction == "forward":
                mazelocation -= maze_size
            elif direction == "b" or direction == "back":
                mazelocation += maze_size
                toskipforward = [1, 4]
                toskipbackward = [3, 7]
            elif direction == "l" or direction == "left":
                mazelocation -= 1
                togoback = [2, 3, 6, 7]
            elif direction == "r" or direction == "right":
                mazelocation += 1
                togoforward = [1, 2, 4, 5]
            break
        else:
            print("error. Please try again.")

    if mazemap[mazelocation] in togoback:
        mazeview = mazemap[mazelocation] - 1
    elif mazemap[mazelocation] in togoforward:
        mazeview = mazemap[mazelocation] + 1
    elif mazemap[mazelocation] in toskipforward:
        mazeview = mazemap[mazelocation] + 2
    elif mazemap[mazelocation] in toskipbackward:
        mazeview = mazemap[mazelocation] - 2
    else: 
        mazeview = mazemap[mazelocation]
        

start()
while True:
    update_graphic()
    navigation()
    print(mazeview)
