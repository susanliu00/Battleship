from player import Player
import random


class Bot(Player):
    def __init__(self):
        super().__init__("Bot")
        self.possible_guesses = [
            [r, c] for r in range(self.board_size) for c in range(self.board_size)
        ]

    def place_ships(self):
        self.place_random_ships()
