from player import Player


class Battleship:
    def __init__(self, opponent):
        self.player1 = Player("Player 1")
        self.player2 = opponent
        self.current = self.player1
        self.nonCurrent = self.player2

    def switch(self):
        self.current, self.nonCurrent = self.nonCurrent, self.current

    def play(self):
        self.player1.place_ships()
        self.player2.place_ships()
        while not self.current.lost():
            print("///////////////////////////////")
            print(self.current.name + "'s Turn")
            self.nonCurrent.print_display_board()
            row, col = self.current.make_guess(self.nonCurrent.display_board)
            self.nonCurrent.check_guess(row, col)
            self.nonCurrent.print_display_board()
            self.switch()
        print(self.nonCurrent.name + " won!")
