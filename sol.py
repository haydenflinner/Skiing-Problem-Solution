from sympy import isprime
from collections import defaultdict, namedtuple

cols = 51
rows = 35
EAST, WEST, STOP = 0,1,2

valid_ways_to_escape_from = defaultdict(lambda: 0)
Enemy = namedtuple('Enemy', ['pos', 'next_move'])
Pos = namedtuple('Pos', ['r', 'c'])

def main():
    # Initialize the field
    enemies = []
    for row in range(rows):
        for col in range(cols):
            if isprime(10 * row + col):
                enemies.append(Enemy(Pos(row, col), (2 * row + col) % 3))

    answer = start_sim(None, Pos(0,25), enemies)
    print("{} / {} = {:.2}% were valid ways!".format(answer, 2**rows, answer/2**rows * 100))

def start_sim(prev_pos, pos, enemies):
    # Stop recursing if we've discovered this path fails
    for enemy in enemies:
        if enemy.pos == pos:
            return 0

    if pos.c == cols or pos.c < 0:
        return 0
    
    # If we've already reached this point, we already know the answer from this point
    if valid_ways_to_escape_from[pos] != 0:
        return valid_ways_to_escape_from[pos]

    if pos.r == rows: # We made it out!
        return 1

    new_enemies = [next_move(e) for e in enemies]
    future = [Pos(pos.r + 1, pos.c + 1), Pos(pos.r + 1, pos.c - 1)] # Left+Down or Right+Down
    for next_pos in future:
        valid_ways_to_escape_from[pos] += start_sim(pos, next_pos, new_enemies)

    return valid_ways_to_escape_from[pos]

def next_move(e):
    colup = 0
    if e.next_move == EAST:
        colup = 1
    if e.next_move == WEST:
        colup = -1
    newpos = Pos(e.pos.r + 1, e.pos.c + colup)
    return Enemy(newpos, (e.next_move + 1) % 3)

main()
