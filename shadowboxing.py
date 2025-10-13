import os
import time
import random
import sys

if os.name == "nt":
    import msvcrt
else:
    import tty
    import termios

def clear():
    os.system("cls" if os.name == "nt" else "clear")

directions = ["up", "down", "left", "right"]

def get_direction(player, action, last_dir):
    arrow_keys = {
        b'H': "up",
        b'P': "down",
        b'K': "left",
        b'M': "right"
    }
    if os.name != "nt":
        arrow_keys = {
            '\x1b[A': "up",
            '\x1b[B': "down",
            '\x1b[D': "left",
            '\x1b[C': "right"
        }

    print(f"Player {player}, {action}. Press an arrow key to choose a direction.")

    while True:
        if os.name == "nt":
            first_char = msvcrt.getch()
            if first_char == b'\xe0' or first_char == b'\x00':
                second_char = msvcrt.getch()
                key = second_char
            else:
                key = first_char
            direction = arrow_keys.get(key)
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch1 = sys.stdin.read(1)
                if ch1 == '\x1b':
                    ch2 = sys.stdin.read(1)
                    ch3 = sys.stdin.read(1)
                    key = ch1 + ch2 + ch3
                    direction = arrow_keys.get(key)
                else:
                    direction = None
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if direction is None:
            continue
        if direction == last_dir:
            print("You cannot choose the same direction as last time. Try again.")
            continue
        return direction

def shadowboxing():
    combo_player = 0
    combo_computer = 0
    turn = "player"  # player starts by pointing first
    last_player_dir = None
    last_computer_dir = None
    clear()
    print("SHADOWBOXING")
    print("You and the Computer take turns pointing and looking in directions.")
    print("If the look direction matches the point direction, that's a Hit.")
    print("Get 3 hits in a row to win!\n")
    input("Press Enter to start...")

    while combo_player < 3 and combo_computer < 3:
        clear()
        print(f"Your combo: {combo_player} | Computer combo: {combo_computer}\n")

        if turn == "player":
            print("Your turn to point.\n")
            point_dir = get_direction(1, "point", last_player_dir)
            last_player_dir = point_dir

            look_dir = random.choice(directions)
            while look_dir == last_computer_dir:
                look_dir = random.choice(directions)
            last_computer_dir = look_dir

            print(f"\nYou pointed {point_dir.upper()}")
            print(f"Computer looked {look_dir.upper()}")
            time.sleep(0.5)

            if look_dir == point_dir:
                print("\nHit!")
                combo_player += 1
                combo_computer = 0
                time.sleep(0.5)
            else:
                print("\nMiss!")
                combo_player = 0
                turn = "computer"
                time.sleep(0.5)
        else:
            print("Computer's turn to point.\n")
            point_dir = random.choice(directions)
            while point_dir == last_computer_dir:
                point_dir = random.choice(directions)
            last_computer_dir = point_dir

            look_dir = get_direction(1, "look", last_player_dir)
            last_player_dir = look_dir

            print(f"\nComputer pointed {point_dir.upper()}")
            print(f"You looked {look_dir.upper()}")
            time.sleep(0.5)

            if look_dir == point_dir:
                print("\nComputer Hit!")
                combo_computer += 1
                combo_player = 0
                time.sleep(0.5)
            else:
                print("\nComputer Missed!")
                combo_computer = 0
                turn = "player"
                time.sleep(0.5)

    clear()
    if combo_player == 3:
        print("3 Hits! You won!\n")
    else:
        print("3 Hits! You lose!\n")
    input("Press Enter to quit.")

if __name__ == "__main__":
    shadowboxing()