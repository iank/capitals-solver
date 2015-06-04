#!/usr/bin/env python
import bestword
import ocr
import pprint
import sys
import cv2

pp = pprint.PrettyPrinter(indent=4)

screenshot = cv2.imread(sys.argv[1], 1)
grid = ocr.decode_tiles(screenshot)
solns = bestword.suggest_words(grid, sys.argv[2])

ideas = [(x['word'], x['score']['connected_length'], x['score']['enemy_adjacent'], x['score']['enemycapital_adjacent']) for x in solns]
ideas = sorted(ideas, key=lambda x: x[1])
pp.pprint(ideas[-10:])
ideas = sorted(ideas, key=lambda x: x[2])
pp.pprint(ideas[-10:])
cap_adjacent = [(x['word'],x['score']['connected_length'],x['loc']) for x in solns if x['score']['enemycapital_adjacent'] > 0]
cap_adjacent = sorted(cap_adjacent, key=lambda x: x[1])
pp.pprint(cap_adjacent[-1:])
