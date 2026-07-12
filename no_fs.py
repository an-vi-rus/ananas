import random
from itertools import combinations
from copy import deepcopy
from datetime import datetime as dt
import combos

penalty = -6
premium = +6
def getpoints(combo: tuple, row: int):
    match row:
        case 2:
            match combo[0]:
                case 0 | 1 | 2 | 3: return 0
                case 5: return 4
                case 6: return 6
                case 4: return 2
                case 7: return 10
                case 8: return 15
                case 9: return 25
        case 1:
            match combo[0]:
                case 0 | 1 | 2: return 0
                case 3: return 2
                case 4: return 4
                case 5: return 8
                case 6: return 12
                case 7: return 20
                case 8: return 30
                case 9: return 50
        case 0:
            match combo[0]:
                case 0: return 0
                case 1: 
                    if combo[1][0] < 4: return 0
                    if combo[1][0] < 10: return combo[1][0] - 3
                    return combo[1][0] - 3 + premium
                case 2: return combo[1][0] + 10 + premium

class Row:
    def __init__(self, n: int):
        self.n = n
        self.reset()
    def reset(self):
        self.cells = 5 if self.n else 3
        self.combo = 0
        self.max_combo = (7, [12])
        self.points = 0
class Hand:
    def __init__(self):
        self.rows = [Row(0), Row(1), Row(2)]
        self.cards = list(range(52))
    def reset(self):
        for row in self.rows: row.reset()
        self.cards = list(range(52))
def s4(hand: Hand, deal: list):
    maxpoints = penalty
    deal = [deal[0] // 4, deal[1] // 4, deal[2] // 4]
    pairs = list(combinations(deal, 2))
    if hand.rows[0].cells == 2:
        for pair in pairs:
            combo = combos.c3_1(hand.rows[0].combo, pair)
            if combo <= hand.rows[1].combo:
                points = getpoints(combo, 0)
                if points > maxpoints: maxpoints = points
        return maxpoints + hand.rows[1].points + hand.rows[2].points if maxpoints > penalty else penalty
    if hand.rows[1].cells == 2:
        for pair in pairs:
            combo = combos.c5_3(hand.rows[1].combo, pair)
            if hand.rows[0].combo <= combo and combo <= hand.rows[2].combo:
                points = getpoints(combo, 1)
                if points > maxpoints: maxpoints = points
        return maxpoints + hand.rows[0].points + hand.rows[2].points if maxpoints > penalty else penalty
    if hand.rows[2].cells == 2:
        for pair in pairs:
            combo = combos.c5_3(hand.rows[2].combo, pair)
            if hand.rows[1].combo <= combo:
                points = getpoints(combo, 2)
                if points > maxpoints: maxpoints = points
        return maxpoints + hand.rows[0].points + hand.rows[1].points if maxpoints > penalty else penalty
    if hand.rows[0].cells and hand.rows[1].cells:
        for pair in pairs:
            combo0 = combos.c3_2(hand.rows[0].combo, pair[0])
            combo1 = combos.c5_4(hand.rows[1].combo, pair[1])
            if combo0 <= combo1 and combo1 <= hand.rows[2].combo:
                points0 = getpoints(combo0, 0)
                points1 = getpoints(combo1, 1)
                if points0 + points1 > maxpoints: maxpoints = points0 + points1
            combo0 = combos.c3_2(hand.rows[0].combo, pair[1])
            combo1 = combos.c5_4(hand.rows[1].combo, pair[0])
            if combo0 <= combo1 and combo1 <= hand.rows[2].combo:
                points0 = getpoints(combo0, 0)
                points1 = getpoints(combo1, 1)
                if points0 + points1 > maxpoints: maxpoints = points0 + points1
        return maxpoints + hand.rows[2].points if maxpoints > penalty else penalty
    if hand.rows[0].cells and hand.rows[2].cells:
        for pair in pairs:
            combo0 = combos.c3_2(hand.rows[0].combo, pair[0])
            combo2 = combos.c5_4(hand.rows[2].combo, pair[1])
            if combo0 <= hand.rows[1].combo and hand.rows[1].combo <= combo2:
                points0 = getpoints(combo0, 0)
                points2 = getpoints(combo2, 2)
                if points0 + points2 > maxpoints: maxpoints = points0 + points2
            combo0 = combos.c3_2(hand.rows[0].combo, pair[1])
            combo2 = combos.c5_4(hand.rows[2].combo, pair[0])
            if combo0 <= hand.rows[1].combo and hand.rows[1].combo <= combo2:
                points0 = getpoints(combo0, 0)
                points2 = getpoints(combo2, 2)
                if points0 + points2 > maxpoints: maxpoints = points0 + points2
        return maxpoints + hand.rows[1].points if maxpoints > penalty else penalty
    if hand.rows[1].cells and hand.rows[2].cells:
        for pair in pairs:
            combo1 = combos.c5_4(hand.rows[1].combo, pair[0])
            combo2 = combos.c5_4(hand.rows[2].combo, pair[1])
            if hand.rows[0].combo <= combo1 and combo1 <= combo2:
                points1 = getpoints(combo1, 1)
                points2 = getpoints(combo2, 2)
                if points1 + points2 > maxpoints: maxpoints = points1 + points2
            combo1 = combos.c5_4(hand.rows[1].combo, pair[1])
            combo2 = combos.c5_4(hand.rows[2].combo, pair[0])
            if hand.rows[0].combo <= combo1 and combo1 <= combo2:
                points1 = getpoints(combo1, 1)
                points2 = getpoints(combo2, 2)
                if points1 + points2 > maxpoints: maxpoints = points1 + points2
        return maxpoints + hand.rows[0].points if maxpoints > penalty else penalty
def s4p(hand: Hand, deal: list):
    maxpoints = penalty
    max_combo = (0, [0])
    placement = 0
    pairs = list(combinations(deal, 2))
    if hand.rows[0].cells == 2:
        for pair in pairs:
            combo = combos.c3_1(hand.rows[0].combo, [pair[0]//4, pair[1]//4])
            if combo <= hand.rows[1].combo:
                points = getpoints(combo, 0)
                if points >= maxpoints:
                    if points > maxpoints:
                        maxpoints = points
                        max_combo = combo
                        placement = ([pair[0], 0], [pair[1], 0])
                    else:
                        if combo > max_combo:
                            max_combo = combo
                            placement = ([pair[0], 0], [pair[1], 0])
        return placement
    if hand.rows[1].cells == 2:
        for pair in pairs:
            combo = combos.c5_3(hand.rows[1].combo, [pair[0]//4, pair[1]//4])
            if hand.rows[0].combo <= combo and combo <= hand.rows[2].combo:
                points = getpoints(combo, 1)
                if points >= maxpoints:
                    if points > maxpoints:
                        maxpoints = points
                        max_combo = combo
                        placement = ([pair[0], 1], [pair[1], 1])
                    else:
                        if combo > max_combo:
                            max_combo = combo
                            placement = ([pair[0], 1], [pair[1], 1])
        return placement
    if hand.rows[2].cells == 2:
        for pair in pairs:
            combo = combos.c5_3(hand.rows[2].combo, [pair[0]//4, pair[1]//4])
            if hand.rows[1].combo <= combo:
                points = getpoints(combo, 2)
                if points >= maxpoints:
                    if points > maxpoints:
                        maxpoints = points
                        max_combo = combo
                        placement = ([pair[0], 2], [pair[1], 2])
                    else:
                        if combo > max_combo:
                            max_combo = combo
                            placement = ([pair[0], 2], [pair[1], 2])
        return placement
    if hand.rows[0].cells and hand.rows[1].cells:
        for pair in pairs:
            combo0 = combos.c3_2(hand.rows[0].combo, pair[0] // 4)
            combo1 = combos.c5_4(hand.rows[1].combo, pair[1] // 4)
            if combo0 <= combo1 and combo1 <= hand.rows[2].combo:
                points0 = getpoints(combo0, 0)
                points1 = getpoints(combo1, 1)
                if points0 + points1 >= maxpoints:
                    if points0 + points1 > maxpoints:
                        maxpoints = points0 + points1
                        max_combo = combo0
                        placement = ([pair[0], 0], [pair[1], 1])
                    else:
                        if combo0 > max_combo:
                            max_combo = combo0
                            placement = ([pair[0], 0], [pair[1], 1])
            combo0 = combos.c3_2(hand.rows[0].combo, pair[1] // 4)
            combo1 = combos.c5_4(hand.rows[1].combo, pair[0] // 4)
            if combo0 <= combo1 and combo1 <= hand.rows[2].combo:
                points0 = getpoints(combo0, 0)
                points1 = getpoints(combo1, 1)
                if points0 + points1 >= maxpoints:
                    if points0 + points1 > maxpoints:
                        maxpoints = points0 + points1
                        max_combo = combo0
                        placement = ([pair[1], 0], [pair[0], 1])
                    else:
                        if combo0 > max_combo:
                            max_combo = combo0
                            placement = ([pair[1], 0], [pair[0], 1])
        return placement
    if hand.rows[0].cells and hand.rows[2].cells:
        for pair in pairs:
            combo0 = combos.c3_2(hand.rows[0].combo, pair[0] // 4)
            combo2 = combos.c5_4(hand.rows[2].combo, pair[1] // 4)
            if combo0 <= hand.rows[1].combo and hand.rows[1].combo <= combo2:
                points0 = getpoints(combo0, 0)
                points2 = getpoints(combo2, 2)
                if points0 + points2 > maxpoints or (points0 + points2 == maxpoints and combo0 > max_combo):
                    maxpoints = points0 + points2
                    max_combo = combo0
                    placement = ([pair[0], 0], [pair[1], 2])
            combo0 = combos.c3_2(hand.rows[0].combo, pair[1] // 4)
            combo2 = combos.c5_4(hand.rows[2].combo, pair[0] // 4)
            if combo0 <= hand.rows[1].combo and hand.rows[1].combo <= combo2:
                points0 = getpoints(combo0, 0)
                points2 = getpoints(combo2, 2)
                if points0 + points2 > maxpoints or (points0 + points2 == maxpoints and combo0 > max_combo):
                    maxpoints = points0 + points2
                    max_combo = combo0
                    placement = ([pair[1], 0], [pair[0], 2])
        return placement
    if hand.rows[1].cells and hand.rows[2].cells:
        for pair in pairs:
            combo1 = combos.c5_4(hand.rows[1].combo, pair[0] // 4)
            combo2 = combos.c5_4(hand.rows[2].combo, pair[1] // 4)
            if hand.rows[0].combo <= combo1 and combo1 <= combo2:
                points1 = getpoints(combo1, 1)
                points2 = getpoints(combo2, 2)
                if points1 + points2 > maxpoints or (points1 + points2 == maxpoints and combo1 > max_combo):
                    maxpoints = points1 + points2
                    max_combo = combo1
                    placement = ([pair[0], 1], [pair[1], 2])
            combo1 = combos.c5_4(hand.rows[1].combo, pair[1] // 4)
            combo2 = combos.c5_4(hand.rows[2].combo, pair[0] // 4)
            if hand.rows[0].combo <= combo1 and combo1 <= combo2:
                points1 = getpoints(combo1, 1)
                points2 = getpoints(combo2, 2)
                if points1 + points2 > maxpoints or (points1 + points2 == maxpoints and combo1 > max_combo):
                    maxpoints = points1 + points2
                    max_combo = combo1
                    placement = ([pair[1], 1], [pair[0], 2])
        return placement
def s3(hand:Hand, deal: list):
    for card in deal: hand.cards.remove(card)
    deal = [deal[0] // 4, deal[1] // 4, deal[2] // 4]
    pairs = list(combinations(deal, 2))
    nextdeals = list(combinations(hand.cards, 3))
    maxpoints = penalty
    s4penalty = penalty * len(nextdeals)
    if hand.rows[0].cells >= 2:
        handcopy = deepcopy(hand)
        handcopy.rows[0].cells -= 2
        for pair in pairs:
            combo = combos.addpair(hand.rows[0].combo, pair)
            handcopy.rows[0].combo = combo
            if handcopy.rows[0].cells == 0: handcopy.rows[0].points = getpoints(handcopy.rows[0].combo, 0)
            if combo <= hand.rows[1].max_combo and combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
    if hand.rows[1].cells >= 2:
        handcopy = deepcopy(hand)
        handcopy.rows[1].cells -= 2
        for pair in pairs:
            combo = combos.addpair(hand.rows[1].combo, pair)
            handcopy.rows[1].combo = combo
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo, 1)
                handcopy.rows[1].max_combo = combo
            else: handcopy.rows[1].max_combo = combos.max_combo(combo)
            if handcopy.rows[0].combo <= combo and combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
    if hand.rows[2].cells >= 2:
        handcopy = deepcopy(hand)
        handcopy.rows[2].cells -= 2
        for pair in pairs:
            combo = combos.addpair(hand.rows[2].combo, pair)
            handcopy.rows[2].combo = combo
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo, 2)
                handcopy.rows[2].max_combo = combo
            else: handcopy.rows[2].max_combo = combos.max_combo(combo)
            if handcopy.rows[1].combo <= combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
    if hand.rows[0].cells and hand.rows[1].cells:     
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[1].cells -= 1 
            combo0 = combos.addcard(hand.rows[0].combo, pair[0])
            combo1 = combos.addcard(hand.rows[1].combo, pair[1])
            handcopy.rows[0].combo = combo0
            handcopy.rows[1].combo = combo1
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo, 0)
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if combo0 <= handcopy.rows[1].max_combo and combo1 <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[1].cells -= 1
            combo0 = combos.addcard(hand.rows[0].combo, pair[1])
            combo1 = combos.addcard(hand.rows[1].combo, pair[0])
            handcopy.rows[0].combo = combo0
            handcopy.rows[1].combo = combo1
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo, 0)
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if combo0 <= handcopy.rows[1].max_combo and combo1 <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
    if hand.rows[0].cells and hand.rows[2].cells:     
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[2].cells -= 1 
            combo0 = combos.addcard(hand.rows[0].combo, pair[0])
            combo2 = combos.addcard(hand.rows[2].combo, pair[1])
            handcopy.rows[0].combo = combo0
            handcopy.rows[2].combo = combo2
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo0, 0)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if combo0 <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[2].cells -= 1
            combo0 = combos.addcard(hand.rows[0].combo, pair[1])
            combo2 = combos.addcard(hand.rows[2].combo, pair[0])
            handcopy.rows[0].combo = combo0
            handcopy.rows[2].combo = combo2
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo, 0)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if combo0 <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
    if hand.rows[1].cells and hand.rows[2].cells:     
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[1].cells -= 1
            handcopy.rows[2].cells -= 1 
            combo1 = combos.addcard(hand.rows[1].combo, pair[0])
            combo2 = combos.addcard(hand.rows[2].combo, pair[1])
            handcopy.rows[1].combo = combo1
            handcopy.rows[2].combo = combo2
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if combo0 <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
            handcopy = deepcopy(hand)
            handcopy.rows[1].cells -= 1
            handcopy.rows[2].cells -= 1 
            combo1 = combos.addcard(hand.rows[1].combo, pair[1])
            combo2 = combos.addcard(hand.rows[2].combo, pair[0])
            handcopy.rows[1].combo = combo1
            handcopy.rows[2].combo = combo2
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if combo0 <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints: maxpoints = points
    return maxpoints
def s3p(hand:Hand, deal: list):
    start = dt.now()
    #for card in deal: hand.cards.remove(card)
    #deal = [deal[0] // 4, deal[1] // 4, deal[2] // 4]
    pairs = list(combinations(deal, 2))
    nextdeals = list(combinations(hand.cards, 3))
    maxpoints = penalty
    placement = 0
    s4penalty = penalty * len(nextdeals)
    if hand.rows[0].cells >= 2:
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 2
            combo = combos.addpair(hand.rows[0].combo, [pair[0] // 4, pair[1] // 4])
            handcopy.rows[0].combo = combo
            if handcopy.rows[0].cells == 0: handcopy.rows[0].points = getpoints(handcopy.rows[0].combo, 0)
            if combo <= hand.rows[1].max_combo and combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[0], 0], [pair[1], 0])
    if hand.rows[1].cells >= 2:
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[1].cells -= 2
            combo = combos.addpair(hand.rows[1].combo, [pair[0] // 4, pair[1] // 4])
            handcopy.rows[1].combo = combo
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo, 1)
                handcopy.rows[1].max_combo = combo
            else: handcopy.rows[1].max_combo = combos.max_combo(combo)
            if handcopy.rows[0].combo <= handcopy.rows[1].max_combo and combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[0], 1], [pair[1], 1])
    if hand.rows[2].cells >= 2:
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[2].cells -= 2
            combo = combos.addpair(hand.rows[2].combo, [pair[0] // 4, pair[1] // 4])
            handcopy.rows[2].combo = combo
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo, 2)
                handcopy.rows[2].max_combo = combo
            else: handcopy.rows[2].max_combo = combos.max_combo(combo)
            if handcopy.rows[1].combo <= handcopy.rows[2].max_combo and handcopy.rows[0].combo <= handcopy.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[0], 2], [pair[1], 2])

    if hand.rows[0].cells and hand.rows[1].cells:     
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[1].cells -= 1 
            combo0 = combos.addcard(hand.rows[0].combo, pair[0] // 4)
            combo1 = combos.addcard(hand.rows[1].combo, pair[1] // 4)
            handcopy.rows[0].combo = combo0
            handcopy.rows[1].combo = combo1
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo0, 0)
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if combo0 <= handcopy.rows[1].max_combo and combo1 <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[0], 0], [pair[1], 1])
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[1].cells -= 1
            combo0 = combos.addcard(hand.rows[0].combo, pair[1] // 4)
            combo1 = combos.addcard(hand.rows[1].combo, pair[0] // 4)
            handcopy.rows[0].combo = combo0
            handcopy.rows[1].combo = combo1
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo0, 0)
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if combo0 <= handcopy.rows[1].max_combo and combo1 <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[1], 0], [pair[0], 1])
    if hand.rows[0].cells and hand.rows[2].cells:     
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[2].cells -= 1 
            combo0 = combos.addcard(hand.rows[0].combo, pair[0] // 4)
            combo2 = combos.addcard(hand.rows[2].combo, pair[1] // 4)
            handcopy.rows[0].combo = combo0
            handcopy.rows[2].combo = combo2
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo0, 0)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if combo0 <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[0], 0], [pair[1], 2])
            handcopy = deepcopy(hand)
            handcopy.rows[0].cells -= 1
            handcopy.rows[2].cells -= 1
            combo0 = combos.addcard(hand.rows[0].combo, pair[1] // 4)
            combo2 = combos.addcard(hand.rows[2].combo, pair[0] // 4)
            handcopy.rows[0].combo = combo0
            handcopy.rows[2].combo = combo2
            if handcopy.rows[0].cells == 0: 
                handcopy.rows[0].points = getpoints(combo0, 0)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if combo0 <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[1], 0], [pair[1], 2])
    if hand.rows[1].cells and hand.rows[2].cells:     
        for pair in pairs:
            handcopy = deepcopy(hand)
            handcopy.rows[1].cells -= 1
            handcopy.rows[2].cells -= 1 
            combo1 = combos.addcard(hand.rows[1].combo, pair[0] // 4)
            combo2 = combos.addcard(hand.rows[2].combo, pair[1] // 4)
            handcopy.rows[1].combo = combo1
            handcopy.rows[2].combo = combo2
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if handcopy.rows[0].combo <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[0], 1], [pair[1], 2])
            handcopy = deepcopy(hand)
            handcopy.rows[1].cells -= 1
            handcopy.rows[2].cells -= 1 
            combo1 = combos.addcard(hand.rows[1].combo, pair[1] // 4)
            combo2 = combos.addcard(hand.rows[2].combo, pair[0] // 4)
            handcopy.rows[1].combo = combo1
            handcopy.rows[2].combo = combo2
            if handcopy.rows[1].cells == 0: 
                handcopy.rows[1].points = getpoints(combo1, 1)
                handcopy.rows[1].max_combo = combo1
            else: handcopy.rows[1].max_combo = combos.max_combo(combo1)
            if handcopy.rows[2].cells == 0: 
                handcopy.rows[2].points = getpoints(combo2, 2)
                handcopy.rows[2].max_combo = combo2
            else: handcopy.rows[2].max_combo = combos.max_combo(combo2)
            if handcopy.rows[0].combo <= handcopy.rows[1].max_combo and handcopy.rows[1].combo <= hand.rows[2].max_combo:
                r = 0
                for nextdeal in nextdeals:
                    r += s4(handcopy, nextdeal)
                if r > s4penalty:
                    points = r / len(nextdeals) + handcopy.rows[0].points + handcopy.rows[1].points + handcopy.rows[2].points
                    if points > maxpoints:
                        maxpoints = points
                        placement = ([pair[1], 1], [pair[0], 2])
    print(f'elapced time {(dt.now() - start).total_seconds()}')
    return placement
