from player import Player


class Bot(Player):
    def __init__(self):
        super().__init__("Bot")
        self.possible_guesses = [
            [r, c] for r in range(self.board_size) for c in range(self.board_size)
        ]

    # A bot always randomly places ships
    def place_ships(self):
        self.place_random_ships()
