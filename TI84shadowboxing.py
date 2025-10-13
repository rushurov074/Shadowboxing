import random
import time

directions = ["up", "down", "left", "right"]

def get_player_direction(action, last_dir=None):
    while True:
        choice = input(f"{action} (up/down/left/right): ").strip().lower()
        if choice not in directions:
            print("Invalid direction. Try again.")
        elif choice == last_dir:
            print(f"You cannot choose the same direction as last time ({last_dir}).")
        else:
            return choice

def shadowboxing():
    combo = 0
    combo_owner = None
    player_turn = True  # True = player points first
    last_player_dir = None
    last_computer_dir = None

    print("Shadowboxing")
    print("First to 3 hits in a row wins!")
    input("Press Enter to start...")

    while combo < 3:
        if player_turn:
            print("\nYour turn to POINT!")
            pointer = get_player_direction("Point!", last_player_dir)
            last_player_dir = pointer

            # Computer reacts
            computer_look = random.choice([d for d in directions if d != last_computer_dir])
            last_computer_dir = computer_look

            print(f"You pointed {pointer.upper()}")
            print(f"Computer looked {computer_look.upper()}")

            if pointer == computer_look:
                combo_owner = "Player"
                combo += 1
                print("Hit!")
            else:
                combo_owner = None
                combo = 0
                print("Miss!")
                player_turn = False

        else:
            print("\nComputer points!")
            computer_point = random.choice([d for d in directions if d != last_computer_dir])
            last_computer_dir = computer_point

            player_look = get_player_direction("Look!", last_player_dir)
            last_player_dir = player_look

            print(f"Computer pointed {computer_point.upper()}")
            print(f"You looked {player_look.upper()}")

            if computer_point == player_look:
                combo_owner = "Computer"
                combo += 1
                print("Hit!")
            else:
                combo_owner = None
                combo = 0
                print("Miss!")
                player_turn = True

        print(f"Combo: {combo} ({combo_owner if combo_owner else 'None'})")
        time.sleep(1)

    print("\nGame Over!")
    winner = combo_owner
    print(f"{winner} wins with 3 hits in a row!")

shadowboxing()