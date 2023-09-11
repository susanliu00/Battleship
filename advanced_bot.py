from bot import Bot
import random


# Advanced Bot logic:
# It's better to spread out hits when looking for a ship, so it will avoid selecting an adjacent square
# to a previous miss, unless all possible guessing squares are next to a miss
#   - implemented by keeping a list of all possible guessing squares, and good_choices which holds squares
#     next to no misses
# When it hits a ship for the first time, it will guess in one of four directions
# When a ship has more than 1 hit, it determines it's direction and
#   - if there's a gap between the hits (very unlikely, but possible with this algorithm), it will
#     aim for the gap
#   - otherwise it selects a hit in either direction (up/down or left/right)
class AdvancedBot(Bot):
    def __init__(self):
        super().__init__()
        self.found = {}  # holds ships it has found and their coordinates
        self.good_choices = [
            [r, c] for r in range(self.board_size) for c in range(self.board_size)
        ]
        self.prev_guess = None

    def make_guess(self, other_board):
        if not self.prev_guess:
            r, c = self.random_choice()
        else:
            r, c = self.prev_guess
            if other_board[r][c] == "X":
                for i, j in self.directions:
                    # The previous hit was a miss, so remove all squares next to it from good_choices
                    if [r + i, c + j] in self.good_choices:
                        self.good_choices.remove([r + i, c + j])
                # If we've found a ship before, target it
                if self.found:
                    r, c = self.target_ship(next(iter(self.found)))
                else:
                    r, c = self.random_choice()
            else:
                # Previous hit was a ship
                ship = other_board[r][c]
                if ship in self.found:
                    # Check if the previous hit sank the ship
                    if len(self.found[ship]) + 1 == self.ship_map[ship]:
                        del self.found[ship]
                        if self.found:
                            r, c = self.target_ship(next(iter(self.found)))
                        else:
                            r, c = self.random_choice()
                    else:
                        # Otherwise try to sink it
                        self.insert_ship_coordinate(ship, r, c)
                        r, c = self.target_ship(ship)
                else:
                    self.found[ship] = [[r, c]]
                    r, c = self.target_ship(ship)
        self.possible_guesses.remove([r, c])
        if [r, c] in self.good_choices:
            self.good_choices.remove([r, c])
        print("Bot guessed [" + str(r) + "," + str(c) + "]")
        self.prev_guess = [r, c]
        return r, c

    # Add coordinate to self.found, which holds known sorted ship coordinates
    def insert_ship_coordinate(self, ship, r, c):
        if self.found[ship][0][0] == r:
            for i in range(len(self.found[ship])):
                if self.found[ship][i][1] > c:
                    self.found[ship].insert(i, [r, c])
                    return
            self.found[ship].append([r, c])
        else:
            for i in range(len(self.found[ship])):
                if self.found[ship][i][0] > r:
                    self.found[ship].insert(i, [r, c])
                    return

            self.found[ship].append([r, c])

    # If there's no ship information, guess a square next to no misses if possible
    def random_choice(self):
        if not self.good_choices:
            r, c = random.choice(self.possible_guesses)
        else:
            r, c = random.choice(self.good_choices)
        return r, c

    def target_ship(self, ship):
        # If it has length 1, we don't know direction so guess in one of four
        if len(self.found[ship]) == 1:
            for r, c in self.directions:
                if [
                    self.found[ship][0][0] + r,
                    self.found[ship][0][1] + c,
                ] in self.possible_guesses:
                    return [self.found[ship][0][0] + r, self.found[ship][0][1] + c]
        # Otherwise determine it's direction
        if self.found[ship][0][0] == self.found[ship][1][0]:
            # Look for gap
            for i in range(1, len(self.found[ship])):
                if self.found[ship][i][1] > self.found[ship][i - 1][1] + 1:  # found gap
                    return [self.found[ship][0][0], self.found[ship][i][1] - 1]
            # Otherwise try in one of two directions
            if [
                self.found[ship][0][0],
                self.found[ship][0][1] - 1,
            ] in self.possible_guesses:
                return [self.found[ship][0][0], self.found[ship][0][1] - 1]
            else:
                return [self.found[ship][-1][0], self.found[ship][-1][1] + 1]
        else:  # same code but for vertical
            for i in range(1, len(self.found[ship])):
                if self.found[ship][i][0] > self.found[ship][i - 1][0] + 1:  # found gap
                    return [self.found[ship][i][0] - 1, self.found[ship][0][1]]
            if [
                self.found[ship][0][0] - 1,
                self.found[ship][0][1],
            ] in self.possible_guesses:
                return [self.found[ship][0][0] - 1, self.found[ship][0][1]]
            else:
                return [self.found[ship][-1][0] + 1, self.found[ship][0][1]]
