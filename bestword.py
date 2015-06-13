#!/usr/bin/env python
import itertools

def get_tile(grid,coords,mapping):
    if coords in mapping:    
        return grid[mapping[coords]]
    else:
        return None

def map_tiles(grid):
    mapping = {}
    for k,tile in enumerate(grid):
        mapping[(tile['i'], tile['j'])] = k
    return mapping

def suggest_words(grid, MY_TEAM):
    if (MY_TEAM == 'blue'):
        ENEMY_TEAM = 'red'
    else:
        ENEMY_TEAM = 'blue'

    ## Save time
    mapping = map_tiles(grid)

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
            'length': len(list(candidate['word'])),
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
            tile = get_tile(grid, c, mapping)
            connected_loc.append(c)

            # Check six adjacent tiles
            adjacent = [(c[0] + x[0], c[1] + x[1]) for x in adj]
            for cc in adjacent:
                nt = get_tile(grid, cc, mapping)
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

                nt = get_tile(grid, cc, mapping)
                if (nt == None):
                    continue

                if (nt['team'] == ENEMY_TEAM):
                    candidate['score']['enemy_adjacent'] += 1
                if (nt['team'] == ENEMY_TEAM and nt['capital'] == 1):
                    candidate['score']['enemycapital_adjacent'] += 1
                if (nt['team'] == MY_TEAM and nt['capital'] == 1):
                    candidate['score']['mycapital_adjacent'] += 1

                visited.append(cc)

    # TODO: better scoring, consider positions of connected tiles, etc

    return solns
