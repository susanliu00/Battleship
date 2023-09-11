from bot import Bot
import random


# Beginner bot will randomly guess from all free squares on the board
class BeginnerBot(Bot):
    def __init__(self):
        super().__init__()

    def make_guess(self, other_board):
        r, c = random.choice(self.possible_guesses)
        self.possible_guesses.remove([r, c])
        print("Bot guessed [" + str(r) + "," + str(c) + "]")
        return r, c
