#!/usr/bin/env python
import pprint
import sys
import cv2
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import bestword
import ocr

filename = sys.argv[1]
MY_TEAM = sys.argv[2]
if (MY_TEAM == 'blue'):
    ENEMY_TEAM = 'red'
else:
    ENEMY_TEAM = 'blue'

## TODO: check args

screenshot = cv2.imread(sys.argv[1], 1)
grid = ocr.decode_tiles(screenshot)
solns = bestword.suggest_words(grid, MY_TEAM)

no_capital_detected = 1
remaining_enemy_tiles = 0
for tile in grid:
    if tile['capital'] == 1 and tile['team'] == ENEMY_TEAM:
        no_capital_detected = 0
    if tile['team'] == ENEMY_TEAM:
        remaining_enemy_tiles += 1

ideas = [(x['tiles'],x['score']['length'],x['score']['enemy_adjacent'],x['word']) for x in solns]
ideas = sorted(ideas, key=lambda x: x[2],reverse=True)
max_adj = ideas[0][2]

game_is_winnable = 0
if max_adj == remaining_enemy_tiles:
    game_is_winnable = 1

# Check if we can knock out their capital
cap_adjacent = [(x['score']['enemy_adjacent'],x['word'],x['tiles']) \
                for x in solns if x['score']['enemycapital_adjacent'] > 0]
cap_adjacent = sorted(cap_adjacent, key=lambda x: x[0], reverse=True)
if len(cap_adjacent) > 0:
    img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    cv2.drawContours(img, [x['contour'] for x in cap_adjacent[0][2]], -1, (0, 255, 0), 3 )
    plt.imshow(img)
    plt.title(cap_adjacent[0][1])
    plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
    plt.savefig('suggestions.png', bbox_inches='tight')
    print("Possible to gain extra turn: suggestions.png")
elif no_capital_detected and game_is_winnable:
    ideas = [x for x in ideas if x[2] == max_adj]
    ideas = sorted(ideas, key=lambda x: x[1],reverse=True)
    longest_best = ideas[0]
    shortest_best = ideas[-1]

    long_img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    cv2.drawContours(long_img, [x['contour'] for x in longest_best[0]], -1, (0, 255, 0), 3 )
    short_img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    cv2.drawContours(short_img, [x['contour'] for x in shortest_best[0]], -1, (0, 255, 0), 3 )
    plt.subplot(2,1,1)
    plt.imshow(long_img)
    plt.title(longest_best[3])
    plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis

    plt.subplot(2,1,2)
    plt.imshow(short_img)
    plt.title(shortest_best[3])
    plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis

    plt.savefig('suggestions.png', bbox_inches='tight', dpi=200)
    print("Game is winnable this turn: suggestions.png")

else: # can't take capital or win this turn
    # TODO: protect own capital, avoid bridging, take center
    # TODO: GA aggregate score w/ feature weights & state

    # currently just suggest words with highest self-adjacency
    ideas = [(x['word'],x['score']['connected_length'],x['score']['enemy_adjacent']) for x in solns]
    ideas = sorted(ideas, key=lambda x: x[2],reverse=True)
    ideas = sorted(ideas, key=lambda x: x[1],reverse=True)
    for k in range(0,9):
        print("word: %14s, territory gain %4d, enemy territory loss %4d" % (ideas[k]))
