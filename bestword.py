#!/usr/bin/env python

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
 
#print letters
#print letter_count
print possible_words
