#!/usr/bin/env python
import random
import bestword
import numpy as np

#import pprint
#pp = pprint.PrettyPrinter(indent=2)

#gc.set_debug(gc.DEBUG_LEAK)

adj = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0)]

def oob(coord):
    i,j = coord
    # is tile out of bounds?
    if (i < -3 or i > 3):
        return True
    if (i == -3 and (j < -1 or j > 4)):
        return True
    if (i == -2 and (j < -2 or j > 4)):
        return True
    if (i == -1 and (j < -2 or j > 3)):
        return True
    if (i ==  0 and (j < -3 or j > 3)):
        return True
    if (i ==  1 and (j < -3 or j > 2)):
        return True
    if (i ==  2 and (j < -4 or j > 2)):
        return True
    if (i ==  3 and (j < -4 or j > 1)):
        return True

    return False


def other_team(team):
    if (team == 'red'):
        return 'blue'
    else:
        return 'red'

# http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Error"

# http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
def gen_letter():
    return weighted_choice([
        ('e', .1202), ('t', .0910), ('a', .0812), ('o', .0768), ('i', .0731),
        ('n', .0695), ('s', .0628), ('r', .0602), ('h', .0592), ('d', .0432),
        ('l', .0398), ('u', .0288), ('c', .0271), ('m', .0261), ('f', .0230),
        ('y', .0211), ('w', .0209), ('g', .0203), ('p', .0182), ('b', .0149),
        ('v', .0111), ('k', .0069), ('x', .0017), ('q', .0011), ('j', .0010),
        ('z', .0007),
    ])

def score_word_by_model(soln, model):
    x = np.array([
        soln['score']['length'],
        soln['score']['connected_length'],
        soln['score']['mycapital_adjacent'],
        soln['score']['enemycapital_adjacent'],
        soln['score']['enemy_adjacent']
    ])
    return np.sum(x*model)
    

def pick_move(solns, grid, model):
    ideas = []
    for soln in solns:
        ideas.append((soln, score_word_by_model(soln, model)))

    ideas = sorted(ideas, key=lambda x: x[1],reverse=True)
    return ideas[0][0]

def initialize_grid():
    grid = []
    blue_capital = {
        'letter':'', 
        'team':'blue',
        'capital':1,
        'i':-2,
        'j':-1
    }
    red_capital = {
        'letter':'', 
        'team':'red',
        'capital':1,
        'i':2,
        'j':1
    }
    grid.append(blue_capital)
    grid.append(red_capital)

    for c in adj:
        grid.append({
            'letter': gen_letter(),
            'team': 'none',
            'capital':0,
            'i': (-2 + c[0]),
            'j': (-1 + c[1]),
        })
        grid.append({
            'letter': gen_letter(),
            'team': 'none',
            'capital':0,
            'i': (2 + c[0]),
            'j': (1 + c[1]),
        })

    return grid

def get_owned_tiles(grid, team):
    l = []
    for tile in grid:
        if (tile['team'] == team):
            l.append(tile)
    return l

# Returns capital tile or None
def get_capital(grid, team):
    my_tiles = get_owned_tiles(grid, team)
    assert len(my_tiles) > 0, "Undetected win condition"
    for tile in my_tiles:
        if (tile['capital'] == 1):
            return tile
    return None

def get_glyph(grid, coords):
    for tile in grid:
        if tile['i'] == coords[0] and tile['j'] == coords[1]:
            if (tile['capital'] == 1):
                return '*'
            if (tile['team'] == 'none'):
                return tile['letter']
            elif (tile['team'] == 'blue'):
                return '&'
            elif (tile['team'] == 'red'):
                return '#'
    return ' '

def get_tile(grid, c):
    for tile in grid:
        if tile['i'] == c[0] and tile['j'] == c[1]:
            return tile
    return None

def do_move(grid, move, team):
    tiles = move['tiles']
    # first pass: find all connected tiles, mark as team
    # second pass: find all enemy tiles adjacent to team tiles, destroy these
    #              find all empty tiles adjacent to team tiles, create these
    # third pass: any remaining tiles that weren't part of the word, shuffle

    # first pass
    for c in move['connected_loc']:
        tile = get_tile(grid, c)
        tile['team'] = team
        tile['letter'] = ''
        tile['capital'] = 0
    # Second pass, a
    for c in move['enemy_adj']:
        tile = get_tile(grid, c)
        tile['team'] = 'none'
        tile['letter'] = gen_letter()
        tile['capital'] = 0
    # Second pass, b
    for tile in get_owned_tiles(grid, team):
        for c in adj:
            cc = (tile['i'] + c[0], tile['j'] + c[1])
            if (get_tile(grid, cc) == None and not oob(cc)):
                grid.append({
                    'team': 'none', 'letter': gen_letter(),
                    'i':cc[0],'j':cc[1], 'capital':0
                })

    # Third pass
    remaining = list(set(move['loc']) - set(move['connected_loc']))
    for c in remaining:
        tile = get_tile(grid, c)
        assert tile['team'] == 'none', "Tile should be un-owned"
        tile['letter'] = gen_letter()
        

def print_grid(grid):
    glyphs = [get_glyph(grid, x) for x in [(-2,-2),(0,-3),(2,-4)]]
    print(" %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-3,-1),(-1,-2),(1,-3),(3,-4)]]
    print("%s %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-2,-1),(0,-2),(2,-3)]]
    print(" %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-3, 0),(-1,-1),(1,-2),(3,-3)]]
    print("%s %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-2, 0),(0,-1),(2,-2)]]
    print(" %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-3, 1),(-1, 0),(1,-1),(3,-2)]]
    print("%s %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-2, 1),(0, 0),(2,-1)]]
    print(" %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-3, 2),(-1, 1),(1, 0),(3,-1)]]
    print("%s %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-2, 2),(0, 1),(2, 0)]]
    print(" %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-3, 3),(-1, 2),(1, 1),(3, 0)]]
    print("%s %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-2, 3),(0, 2),(2, 1)]]
    print(" %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-3, 4),(-1, 3),(1, 2),(3, 1)]]
    print("%s %s %s %s" % tuple(glyphs))
    glyphs = [get_glyph(grid, x) for x in [(-2, 4),(0, 3),(2, 2)]]
    print(" %s %s %s" % tuple(glyphs))

def capitals(model1, model2, verbose=False):
    grid = initialize_grid()
    if (verbose):
        print_grid(grid)

    round = 1
    winner = 'none'
    CURRENT_TEAM = random.choice(["red","blue"])
    extra_turn = 0
    models = {'red':model1, 'blue':model2}

    while (winner == 'none' and round < 30):
        # create my capital if it doesn't exist
        if (get_capital(grid, CURRENT_TEAM) == None):
            my_tiles = get_owned_tiles(grid, CURRENT_TEAM)
            my_tiles[0]['capital'] = 1
            
        # Get possible moves
        solns = bestword.suggest_words(grid, CURRENT_TEAM)

        # Pick best move
        move = pick_move(solns,grid,models[CURRENT_TEAM])
        solns = []
        if (verbose):
            print("%s team plays: [%s]" % (CURRENT_TEAM, move['word']))
        do_move(grid, move, CURRENT_TEAM)
        move = []
        if (verbose):
            print_grid(grid)

        round += 1

        # Have we won?
        if (len(get_owned_tiles(grid, other_team(CURRENT_TEAM))) == 0):
            winner = CURRENT_TEAM
            break

        # Did we get an extra turn?
        if (get_capital(grid, other_team(CURRENT_TEAM)) == None and extra_turn == 0):
            extra_turn = 1
            pass
        else:
            CURRENT_TEAM = other_team(CURRENT_TEAM)
            extra_turn = 0

    return winner
