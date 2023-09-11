class Ship:
    def __init__(self, name, symbol, size):
        self.name = name
        self.symbol = symbol
        self.size = size
    
    def sunk(self):
        return self.size == 0