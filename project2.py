from problem import State, Coordinate
import re
import time
import random

# select heuristic
print("select heuristic:")
print('1.Number of mushrooms remaining')
print('2.the shortest Manhattan distance from any remaining mushroom')
print('3.The most Manhattan distance between two mushrooms remains')

num_heuristic = int(input())

# read from file
red_mushroom = []
blue_mushroom = []
obstacle = []
with open('Mario.txt', 'r') as file:
    lines = list(filter(lambda x: x != '\n', file.readlines()))
    n = int(lines[0])
    m = int(lines[1])
    coordinate = re.findall(r'\d+', lines[2])
    start = Coordinate(coordinate[0], coordinate[1])

    mushroom = int(lines[3])
    blue_number = 0
    red_number = 0
    sp = State(coordinate[0], coordinate[1], mushroom, red_number, blue_number)

    for i in range(mushroom):
        c = re.findall(r'\d+', lines[4 + i])
        red_mushroom.append(Coordinate(c[0], c[1]))
    for j in range(mushroom):
        c = re.findall(r'\d+', lines[5 + i + j])
        blue_mushroom.append(Coordinate(c[0], c[1]))
    for k in lines[6 + i + j:]:
        t = re.findall(r'\d+', k)
        obstacle.append(Coordinate(t[0], t[1]))


def LRTA_star_cost(s, a, sprin, H):
    if not sprin:
        return s.heuristic(num_heuristic, blue_mushroom, red_mushroom)
    else:
        return H[sprin] + 1


def LRTA_star(spirin, counter=0):
    """
    :param counter: a counter
    :param spirin: current state
    :var result: dict, initially empty
    :var H: dict, initially empty
    :var s: previous state
    :var a: previous action
    """

    result = {}
    H = {}
    s = None
    a = None

    while True:
        if spirin.goal_test():
            print(counter)
            exit()

        if spirin not in H.keys():
            H[spirin] = spirin.heuristic(num_heuristic, blue_mushroom, red_mushroom)

        if s:
            result[(s, a)] = spirin
            cost = []
            for action in ['right', 'left', 'up', 'down']:
                try:
                    cur = result[(s, action)]
                except KeyError:
                    cur = None
                cost.append(LRTA_star_cost(s, action, cur, H))

            H[s] = min(cost)

        cost = {}
        for action in ['right', 'left', 'up', 'down']:
            try:
                nxt = result[(spirin, action)]
            except KeyError:
                nxt = None

            cost[action] = LRTA_star_cost(spirin, action, nxt, H)

        min_value = min(cost.values())
        choices = []
        for key, v in cost.items():
            if min_value == v:
                choices.append(key)

        a = random.choice(choices)
        s = spirin

        spirin = spirin.check(a, m, n, obstacle, blue_mushroom, red_mushroom, mushroom)

        counter += 1

        print('*' * 25)
        print('action = ' + a)
        print('result((' + str(s.x) + ',' + str(s.y) + '), ' + a + ')' + ' = ' + '(' + str(spirin.x) + ',' + str(
            spirin.y) + ')')

        print('before action :')
        print('H[({0},{1})] ='.format(s.x, s.y), H[s])
        print('after action :')
        cost = []
        for z in filter(lambda x: x if x != a else None,
                        ['right', 'left', 'up', 'down']):
            if z is not None:
                try:
                    current = result[(s, z)]
                except KeyError:
                    current = None
                cost.append(LRTA_star_cost(s, z, current, H))
        cost.append(spirin.heuristic(num_heuristic, blue_mushroom, red_mushroom) + 1)
        print('H[({0},{1})] ='.format(s.x, s.y), min(cost))

        print('blue mushroom eaten :', spirin.num_blue_eat)
        print('red mushroom eaten :', spirin.num_red_eat)
        print('*' * 25)


LRTA_star(sp)
