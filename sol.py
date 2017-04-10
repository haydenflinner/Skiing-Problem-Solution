from sympy import isprime
from collections import defaultdict, namedtuple

cols = 35
rows = 51
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
                e = Enemy(Pos(row, col), (2 * row + col) % 3)
                enemies.append(e)

    starting_loc = Pos(0,25)
    start_sim(None, starting_loc, enemies)

    answer = valid_ways_to_escape_from[starting_loc]
    poss_moves = 2**rows
    print("{} / {} = {:.2}% were valid ways!".format(answer, poss_moves, answer/poss_moves * 100))

def start_sim(prev_pos, pos, enemies):
    # Stop recursing if we've discovred this path fails
    for enemy in enemies:
        if enemy.pos == pos:
            return
    if pos.c == cols or pos.c < 0: return
    
    # If we've already reached this point, we know already know the answer from this point
    if valid_ways_to_escape_from[pos] != 0:
        valid_ways_to_escape_from[prev_pos] += valid_ways_to_escape_from[pos]
        return

    if pos.r == rows: # We made it out!
        valid_ways_to_escape_from[pos] = 1
        return

    new_ens = [next_move(e) for e in enemies]
    future = [Pos(pos.r + 1, pos.c + 1), Pos(pos.r + 1, pos.c - 1)] # Left+Down or Right+Down
    for next_pos in future:
        start_sim(pos, next_pos, new_ens)

    valid_ways_to_escape_from[prev_pos] += valid_ways_to_escape_from[pos]

def next_move(e):
    colup = 0
    if e.next_move == EAST:
        colup = 1
    if e.next_move == WEST:
        colup = -1
    newpos = Pos(e.pos.r + 1, e.pos.c + colup)
    return Enemy(newpos, (e.next_move + 1) % 3)

main()
