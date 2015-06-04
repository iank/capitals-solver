#!/usr/bin/env python
import itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)

grid = [
{'i':-3,'j':-1,'team':'none','letter':'i','capital':0},
{'i':-3,'j':0,'team':'blue','letter':'','capital':0},
{'i':-3,'j':1,'team':'none','letter':'e','capital':0},
{'i':-3,'j':2,'team':'none','letter':'i','capital':0},
{'i':-2,'j':-2,'team':'none','letter':'u','capital':0},
{'i':-2,'j':-1,'team':'blue','letter':'','capital':1},
{'i':-2,'j':0,'team':'none','letter':'i','capital':0},
{'i':-2,'j':1,'team':'red','letter':'','capital':0},
{'i':-2,'j':2,'team':'none','letter':'e','capital':0},
{'i':-1,'j':-2,'team':'blue','letter':'','capital':0},
{'i':-1,'j':-1,'team':'blue','letter':'','capital':0},
{'i':-1,'j':0,'team':'none','letter':'f','capital':0},
{'i':-1,'j':1,'team':'none','letter':'t','capital':0},
{'i':0,'j':-3,'team':'blue','letter':'','capital':0},
{'i':0,'j':-2,'team':'blue','letter':'','capital':0},
{'i':0,'j':-1,'team':'blue','letter':'','capital':0},
{'i':0,'j':0,'team':'none','letter':'u','capital':0},
{'i':0,'j':1,'team':'none','letter':'c','capital':0},
{'i':0,'j':2,'team':'none','letter':'r','capital':0},
{'i':0,'j':3,'team':'none','letter':'r','capital':0},
{'i':1,'j':-3,'team':'none','letter':'w','capital':0},
{'i':1,'j':-2,'team':'blue','letter':'','capital':0},
{'i':1,'j':-1,'team':'none','letter':'d','capital':0},
{'i':1,'j':0,'team':'red','letter':'','capital':0},
{'i':1,'j':1,'team':'red','letter':'','capital':0},
{'i':1,'j':2,'team':'red','letter':'','capital':0},
{'i':2,'j':-3,'team':'none','letter':'t','capital':0},
{'i':2,'j':-2,'team':'none','letter':'e','capital':0},
{'i':2,'j':-1,'team':'red','letter':'','capital':0},
{'i':2,'j':0,'team':'red','letter':'','capital':0},
{'i':2,'j':1,'team':'red','letter':'','capital':1},
{'i':2,'j':2,'team':'none','letter':'g','capital':0},
{'i':3,'j':-2,'team':'none','letter':'u','capital':0},
{'i':3,'j':-1,'team':'none','letter':'o','capital':0},
{'i':3,'j':0,'team':'none','letter':'x','capital':0},
{'i':3,'j':1,'team':'red','letter':'','capital':0},
]


MY_TEAM = 'red'
ENEMY_TEAM = 'blue'

def get_tile(coords):
    # coords = (i,j)
    for tile in grid:
        if (tile['i'] == coords[0] and tile['j'] == coords[1]):
            return tile

## Determine available letters
letters = []
for tile in grid:
    if tile['team'] == 'none':
        letters.append(tile['letter'])

letter_count = {}
for letter in letters:
    if (letter in letter_count):
        letter_count[letter] = letter_count[letter] + 1
    else:
        letter_count[letter] = 1

## Determine all possible words
with open("dict.txt") as f:
    words = f.readlines()

possible_words = []
for word in words:
    ll = letter_count.copy()
    x = list(word.rstrip())
    impossible = 0
    for letter in x:
        if (letter not in ll):
            impossible = 1
        else:
            if (ll[letter] <= 0):
                impossible = 1
            else:
                ll[letter] = ll[letter] - 1
    if (impossible == 0):
        possible_words.append(word.rstrip())

## Eliminate prefixes (assume sorted dictionary)
redundant = []
for k,word in enumerate(possible_words[:-1]):
    if possible_words[k+1].startswith(word):
        redundant.append(word)

possible_words = list(set(possible_words) - set(redundant))

## Find tiles corresponding to each word- multiple permutations where possible
solns = []
for word in possible_words:
    letters = list(word)
    ll = letter_count.copy()
    tiles = []
    for letter in letters:
        # find the tile[s] corresponding to this
        tiles.append([x for x in grid if x['letter'] == letter])

    # Supposing there are 2 of one letter, and a word uses 2 of that letter, 
    # product here gives me words that use letter 1 then letter 2,
    # letter 2 then letter 1, letter 1 twice, and letter 2 twice. But all are
    # equivalent for the game
    candidates = list(itertools.product(*tiles));
    hashes = []
    for candidate in candidates:
        hashable = [(x['i'],x['j'])for x in candidate]
        # First part: make sure we haven't used same coords twice
        # Second part: order doesn't matter
        if (len(candidate) == len(list(set(hashable))) and set(hashable) not in hashes):
            hashes.append(set(hashable))
            solns.append({'word': word, 'tiles':candidate, 'loc':hashable})

## Score each word
adj = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0)]
for candidate in solns:
    candidate['score'] = {
        'length': len(list(word)),
        'connected_length': 0,
        'mycapital_adjacent': 0,
        'enemycapital_adjacent': 0,
        'enemy_adjacent': 0,
    }

    # Determine connected length
    # Start with all my tiles
    check = [(tile['i'], tile['j']) for tile in grid if tile['team'] == MY_TEAM]
    connected_loc = []

    # Find all tiles in my word connected to me
    while (len(check) > 0):
        c = check.pop(0)
        tile = get_tile(c)
        connected_loc.append(c)

        # Check six adjacent tiles
        adjacent = [(c[0] + x[0], c[1] + x[1]) for x in adj]
        for cc in adjacent:
            nt = get_tile(cc)
            if (nt == None):
                continue

            # letter tile not in list, but in word?
            in_word = cc in candidate['loc']

            if (cc in connected_loc):
                continue

            if (nt['team'] == 'none' and in_word):
                connected_loc.append(cc)
                candidate['score']['connected_length'] += 1
                check.append(cc)

    # Now that we have all connected tiles in this word, check enemy adjacency
    visited = []
    for c in connected_loc:
        # Check six adjacent tiles
        adjacent = [(c[0] + x[0], c[1] + x[1]) for x in adj]
        for cc in adjacent:
            if cc in visited:
                continue

            nt = get_tile(cc)
            if (nt == None):
                continue

            if (nt['team'] == ENEMY_TEAM):
                candidate['score']['enemy_adjacent'] += 1
            if (nt['team'] == ENEMY_TEAM and nt['capital'] == 1):
                candidate['score']['enemycapital_adjacent'] += 1
            if (nt['team'] == MY_TEAM and nt['capital'] == 1):
                candidate['score']['mycapital_adjacent'] += 1

            visited.append(cc)

## Suggest good candidates:
# TODO: better scoring, consider positions of connected tiles, etc



ideas = [(x['word'], x['score']['connected_length'], x['score']['enemy_adjacent'], x['score']['enemycapital_adjacent']) for x in solns]
ideas = sorted(ideas, key=lambda x: x[1])
pp.pprint(ideas[-10:])
ideas = sorted(ideas, key=lambda x: x[2])
pp.pprint(ideas[-10:])

cap_adjacent = [(x['word'],x['score']['connected_length'],x['loc']) for x in solns if x['score']['enemycapital_adjacent'] > 0]
cap_adjacent = sorted(cap_adjacent, key=lambda x: x[1])
pp.pprint(cap_adjacent[-1:])
