#!/usr/bin/env python
import itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)

grid = [
{'i':0,'j':0,'team':'blue','letter':'','capital':0},
{'i':1,'j':0,'team':'none','letter':'y','capital':0},
{'i':0,'j':1,'team':'none','letter':'n','capital':0},
{'i':-1,'j':1,'team':'none','letter':'e','capital':0},
{'i':-1,'j':0,'team':'blue','letter':'','capital':0},
{'i':0,'j':-1,'team':'blue','letter':'','capital':0},
{'i':1,'j':-1,'team':'blue','letter':'','capital':0},
{'i':0,'j':-2,'team':'blue','letter':'','capital':0},
{'i':1,'j':-2,'team':'blue','letter':'','capital':0},
{'i':2,'j':-2,'team':'none','letter':'u','capital':0},
{'i':2,'j':-1,'team':'none','letter':'n','capital':0},
{'i':2,'j':0,'team':'red','letter':'','capital':0},
{'i':1,'j':1,'team':'red','letter':'','capital':0},
{'i':0,'j':2,'team':'red','letter':'','capital':0},
{'i':0,'j':3,'team':'none','letter':'m','capital':0},
{'i':1,'j':2,'team':'none','letter':'g','capital':0},
{'i':2,'j':1,'team':'red','letter':'','capital':1},
{'i':2,'j':2,'team':'none','letter':'c','capital':0},
{'i':3,'j':1,'team':'red','letter':'','capital':0},
{'i':3,'j':0,'team':'red','letter':'','capital':0},
{'i':3,'j':-1,'team':'none','letter':'r','capital':0},
{'i':-1,'j':3,'team':'none','letter':'l','capital':0},
{'i':-1,'j':2,'team':'none','letter':'f','capital':0},
{'i':-2,'j':2,'team':'none','letter':'s','capital':0},
{'i':-2,'j':1,'team':'blue','letter':'','capital':0},
{'i':-2,'j':0,'team':'blue','letter':'','capital':0},
{'i':-2,'j':-1,'team':'blue','letter':'','capital':1},
{'i':-2,'j':-2,'team':'blue','letter':'','capital':0},
{'i':-1,'j':-2,'team':'blue','letter':'','capital':0},
{'i':0,'j':-3,'team':'blue','letter':'','capital':0},
{'i':1,'j':-3,'team':'blue','letter':'','capital':0},
{'i':2,'j':-4,'team':'none','letter':'a','capital':0},
{'i':2,'j':-3,'team':'none','letter':'e','capital':0},
{'i':-3,'j':-1,'team':'blue','letter':'','capital':0},
{'i':-3,'j':0,'team':'blue','letter':'','capital':0},
{'i':-3,'j':1,'team':'none','letter':'a','capital':0},
{'i':-3,'j':2,'team':'none','letter':'o','capital':0},
{'i':-1,'j':-1,'team':'blue','letter':'','capital':0}];

def get_tile(eye, jay):
    for tile in grid:
        if (tile['i'] == eye and tile['j'] == jay):
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
solns = {}
#for word in possible_words:
word = possible_words[12]
if 1==1:
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
    solns = []
    hashes = []
    for candidate in candidates:
        hashable = [(x['i'],x['j'])for x in candidate]
        # First part: make sure we haven't used same coords twice
        # Second part: order doesn't matter
        if (len(candidate) == len(list(set(hashable))) and set(hashable) not in hashes):
            hashes.append(set(hashable))
            solns.append({'word': word, 'tiles':candidate})

## Score each word
for candidate in solns:
    candidate['score'] = {
        'length': len(list(word)),
        'connected_length': 0,
        'mycapital_adjacent': 0,
        'enemycapital_adjacent': 0,
        'blue_adjacent': 0,
    }

    # Determine connected length
    # Start w/ all red tiles
    #     Check 6 adjacent- if letter, 
#    list = [tile in grid if tile['team'] == 'red']
#    while (len(list) > 0):
#        tile = list.pop(0)
        
    # pop(0) == unshift
