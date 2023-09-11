from player import Player
from battleship import Battleship


def choose_bot():
    while True:
        choice = input("Would you like to play easy or hard bot? (e/h)").lower()
        if choice == "e":
            from beginner_bot import BeginnerBot

            opponent = BeginnerBot()
            break
        elif choice == "h":
            from advanced_bot import AdvancedBot

            opponent = AdvancedBot()
            break
        else:
            print("Please enter e or h")
    return opponent


def main():
    print("Welcome to Battleship :)")
    while True:
        choice = input("Would you like to play a person or a bot? (p/b)").lower()
        if choice == "p":
            opponent = Player("Player 2")
            break
        elif choice == "b":
            opponent = choose_bot()
            break
        else:
            print("Please enter p or b")
    battleship = Battleship(opponent)
    battleship.play()


if __name__ == "__main__":
    main()
