class GridTile:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight

    def __repr__(self):
        return f"GridTile({self.x}, {self.y}, {self.weight})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))