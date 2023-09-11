from player import Player
from battleship import Battleship


def main():
    print("Welcome to Battleship :)")
    while True:
        choice = input("Would you like to play a person or a bot? (p/b)").lower()
        if choice == "p":
            opponent = Player("Player 2")
            break
        elif choice == "b":
            from bot import Bot

            opponent = Bot()
            break
        else:
            print("Please enter p or b")
    battleship = Battleship(opponent)
    battleship.play()


if __name__ == "__main__":
    main()
