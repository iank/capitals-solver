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

print letters
