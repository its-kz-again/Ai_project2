class Coordinate:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __hash__(self):
        return int(str(self.x) + str(self.y))

    def __eq__(self, other):
        return (self.x, self.y) == other


class State(Coordinate):
    def __init__(self, x, y, k, red, blue):
        super().__init__(x, y)
        self.num_red_eat = red
        self.num_blue_eat = blue
        self.k = k

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)

    def heuristic(self, num_heuristic, blue_mushroom, red_mushroom):
        if num_heuristic == 1:
            return self.heuristic1()
        elif num_heuristic == 2:
            return self.heuristic2(blue_mushroom, red_mushroom)
        else:
            return self.heuristic3(blue_mushroom, red_mushroom)

    # Number of mushrooms remaining
    def heuristic1(self):
        h1 = 2 * self.k - (self.num_red_eat + self.num_blue_eat)
        return h1

    # the shortest Manhattan distance from any remaining mushroom
    def heuristic2(self, blue_mushroom, red_mushroom):
        manhatan = []
        for b in blue_mushroom:
            distance = abs(self.x - b.x) + abs(self.y - b.y)
            manhatan.append(distance)
        for r in red_mushroom:
            distance = abs(self.x - r.x) + abs(self.y - r.y)
            manhatan.append(distance)
        h2 = min(manhatan)
        return h2

    # The most Manhattan distance between two mushrooms remains
    @staticmethod
    def heuristic3(blue_mushroom, red_mushroom):
        manhatan = []
        for b in blue_mushroom + red_mushroom:
            for r in red_mushroom + blue_mushroom:
                distance = abs(b.x - r.x) + abs(b.y - r.y)
                manhatan.append(distance)
        try:
            h3 = max(manhatan)
        except (UnboundLocalError, ValueError):
            h3 = 0
        return h3

    @classmethod
    def successor(cls, x, y, b, r, k):
        return State(x, y, k, r, b)

    def check(self, action, m, n, obstacles, blue_mushroom, red_mushroom, k):

        if action == 'right':
            x = self.x + 1
            y = self.y
        elif action == 'left':
            x = self.x - 1
            y = self.y
        elif action == 'up':
            x = self.x
            y = self.y + 1
        else:
            x = self.x
            y = self.y - 1

        # Leaving the coordinates of the earth
        if (x < 1 or y < 1) or (x > n or y > m):
            x = self.x
            y = self.y

        # Dealing with the obstacle
        elif (x, y) in obstacles:
            x = self.x
            y = self.y

        b = self.num_blue_eat
        for i, item in enumerate(blue_mushroom):
            if (x, y) == item:
                b = self.num_blue_eat + 1
                blue_mushroom.pop(i)

        r = self.num_red_eat
        for j, item in enumerate(red_mushroom):
            if (x, y) == item:
                r = self.num_red_eat + 1
                red_mushroom.pop(j)

        return self.successor(x, y, b, r, k)

    def goal_test(self):
        if self.num_blue_eat >= 1 and self.num_red_eat >= 1:
            return True
        return False
