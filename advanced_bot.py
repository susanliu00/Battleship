from bot import Bot
import random


class AdvancedBot(Bot):
    def __init__(self):
        super().__init__()
        self.found = {}
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
                    if [r + i, c + j] in self.good_choices:
                        self.good_choices.remove([r + i, c + j])
                if self.found:
                    r, c = self.target_ship(next(iter(self.found)))
                else:
                    r, c = self.random_choice()
            else:
                ship = other_board[r][c]
                if ship in self.found:
                    if len(self.found[ship]) + 1 == self.ship_map[ship]:
                        del self.found[ship]  # sank already
                        if self.found:
                            r, c = self.target_ship(next(iter(self.found)))
                        else:
                            r, c = self.random_choice()
                    else:
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

    def insert_ship_coordinate(self, ship, r, c):
        if self.found[ship][0][0] == r:
            for i in range(len(self.found[ship])):
                if self.found[ship][i][1] > c:
                    self.found[ship].insert(i, [r, c])
        else:
            for i in range(len(self.found[ship])):
                if self.found[ship][i][0] > r:
                    self.found[ship].insert(i, [r, c])

    def random_choice(self):
        if not self.good_choices:
            r, c = random.choice(self.possible_guesses)
        else:
            r, c = random.choice(self.good_choices)
        return r, c

    def target_ship(self, ship):
        if len(self.found[ship]) == 1:
            for r, c in self.directions:
                if [
                    self.found[ship][0][0] + r,
                    self.found[ship][0][1] + c,
                ] in self.possible_guesses:
                    return [self.found[ship][0][0] + r, self.found[ship][0][1] + c]
        if self.found[ship][0][0] == self.found[ship][1][0]:
            for i in range(1, len(self.found[ship])):
                if self.found[ship][i][1] > self.found[ship][i - 1][1] + 1:  # found gap
                    return [self.found[ship][0][0], self.found[ship][i][1] - 1]
            if [
                self.found[ship][0][0],
                self.found[ship][0][1] - 1,
            ] in self.possible_guesses:
                return [self.found[ship][0][0], self.found[ship][0][1] - 1]
            else:
                return [self.found[ship][-1][0], self.found[ship][-1][1] + 1]
        else:
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
