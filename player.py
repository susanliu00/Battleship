import random
from ship import Ship


class Player:
    def __init__(self, name):
        self.name = name
        self.board_size = 3
        self.board = [
            ["." for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        self.display_board = [
            ["." for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        self.ships = {}
        self.required_ships = [
            # Ship("Carrier", "C", 5),
            # Ship("Battleship", "B", 4),
            # Ship("Destroyer", "D", 3),
            # Ship("Submarine", "S", 3),
            Ship("Patrol Boat", "P", 2),
        ]

    def reset_board(self):
        self.board = [
            ["." for _ in range(self.board_size)] for _ in range(self.board_size)
        ]

    def place_ships(self):
        while True:
            choice = input(
                "Would you like to place ships or randomly generate them? (p/r)"
            ).lower()
            if choice == "p":
                self.input_ships()
                break
            elif choice == "r":
                while True:
                    self.place_random_ships()
                    self.print_board()
                    choice = input("Would you like to regenerate? (y/n)").lower()
                    if choice == "y":
                        self.reset_board()
                        continue
                    elif choice == "n":
                        return
                    else:
                        print("Please enter y or n")
                        self.reset_board()
                        break
            else:
                print("Please enter p or r")

    def input_ships(self):
        for ship in self.required_ships:
            while True:
                try:
                    start_row = int(
                        input(
                            f"Enter the starting row (0-{self.board_size - 1}) for {ship.name} of length {ship.size}: "
                        )
                    )
                    start_col = int(
                        input(
                            f"Enter the starting column (0-{self.board_size - 1}) for {ship.name} of length {ship.size}: "
                        )
                    )
                except ValueError:
                    print("Please enter valid integers.")
                    continue
                if (
                    start_row < 0
                    or start_row >= self.board_size
                    or start_col < 0
                    or start_col >= self.board_size
                ):
                    print("Please enter a coordinate on the board")
                elif self.board[start_row][start_col] != ".":
                    print("There's already a ship there")
                else:
                    break
            while True:
                try:
                    end_row = int(
                        input(
                            f"Enter the ending row (0-{self.board_size - 1}) for {ship.name} of length {ship.size}: "
                        )
                    )
                    end_col = int(
                        input(
                            f"Enter the ending column (0-{self.board_size - 1}) for {ship.name} of length {ship.size}: "
                        )
                    )
                except ValueError:
                    print("Please enter valid integers.")
                    continue
                msg = self.validate_and_place_ship(
                    [start_row, start_col], [end_row, end_col], ship
                )
                if msg != "Valid":
                    print(msg)
                else:
                    break

    def validate_and_place_ship(self, ship, start, end):
        if (
            end[0] < 0
            or end[0] >= self.board_size
            or end[1] < 0
            or end[1] >= self.board_size
        ):
            return "Please enter a coordinate on the board"
        if start[0] != end[0] and start[1] != end[1]:
            return "Start and end points must share a row or column"
        if start[1] == end[1]:
            if abs(start[0] - end[0]) + 1 != ship.size:
                return ship.name + " must be " + str(ship.size) + " units long"
            for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                if self.board[i][start[1]] != ".":
                    return "It must not overlap with other ships"
            for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.board[i][start[1]] = ship.symbol
        else:
            if abs(start[1] - end[1]) + 1 != ship.size:
                return ship.name + " must be " + str(ship.size) + " units long"
            for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if self.board[start[0]][i] != ".":
                    return "It must not overlap with other ships"
            for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.board[start[0]][i] = ship.symbol
        self.ships[ship.symbol] = ship
        return "Valid"

    def place_random_ships(self):
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        for s in self.required_ships:
            while True:
                r = random.randint(0, self.board_size - 1)
                c = random.randint(0, self.board_size - 1)
                dir = random.randint(0, 3)
                msg = self.validate_and_place_ship(
                    s,
                    [r, c],
                    [
                        r + directions[dir][0] * (s.size - 1),
                        c + directions[dir][1] * (s.size - 1),
                    ],
                )
                if msg == "Valid":
                    break

    def print_board(self):
        for row in self.board:
            print(" ".join(row))

    def print_display_board(self):
        for row in self.display_board:
            print(" ".join(row))

    def make_guess(self, other_board):
        while True:
            try:
                row = int(input(f"Enter the row for your guess: "))
                col = int(input(f"Enter the column for your guess: "))
            except ValueError:
                print("Please enter valid integers.")
                continue
            if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
                print("Please enter a coordinate on the board")
            elif other_board[row][col] != ".":
                print("You already guessed there")
            else:
                return row, col

    def check_guess(self, r, c):
        s = self.board[r][c]
        if s == ".":
            self.display_board[r][c] = "X"
            print("Missed!")
        else:
            ship = self.ships[s]
            self.display_board[r][c] = s
            print("Hit the " + ship.name + "!")
            ship.size -= 1
            if ship.sunk():
                print("Sank the " + ship.name + "!")
                del self.ships[s]

    def lost(self):
        return self.ships == {}
