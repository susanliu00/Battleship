from player import Player
import random


class Bot(Player):
    def __init__(self):
        super().__init__("Bot")

    def place_ships(self):
        self.place_random_ships()

    def make_guess(self, other_board):
        while True:
            r = random.randint(0, self.board_size - 1)
            c = random.randint(0, self.board_size - 1)
            if other_board[r][c] == ".":
                break
        print("Bot guessed [" + str(r) + "," + str(c) + "]")
        return r, c
