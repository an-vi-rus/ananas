from datetime import datetime as dt
from itertools import combinations
import random
from solver import *
import s4

def select_ss(h: Hand):
    if h.rows[0].cells:
        if h.rows[0].cells == 2: return s4.s00_2
        if h.rows[1].cells: return s4.s01_2
        return s4.s02_2
    if h.rows[1].cells:
        if h.rows[1].cells == 2: return s4.s11_2
        return s4.s12_2
    return s4.s22_2

def s3(hand_: Hand, c: list):
    start = dt.now()
    hand = hand_.clone()
    for item in c: hand.cards.remove(item)
    cc = list(combinations(hand.cards, 2))
    max_points = PENALTY * len(cc)
    p = 0

    for c0, c1 in combinations(c, 2):
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_3(h.rows[0], c1)
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))

        if hand.rows[1].cells >= 2:
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[1], c1)
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))

        if hand.rows[2].cells >= 2:
            h = hand.clone()
            add_card_5(h.rows[2], c0)
            add_card_5(h.rows[2], c1)
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))

        if hand.rows[0].cells and hand.rows[1].cells:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[1], c1)
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[1], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))

        if hand.rows[0].cells and hand.rows[2].cells:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[2], c1)
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))

        if hand.rows[1].cells and hand.rows[2].cells:
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[2], c1)
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))
            h = hand.clone()
            add_card_5(h.rows[1], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))

    #print(f'double time {(dt.now() - start).total_seconds()} EV= {max_points / len(cc)}')
    return p

def s3_2(hand_: Hand, c: list, sample):
    hand = hand_.clone()  
    for item in c: hand.cards.remove(item)  
    cc = list(combinations(hand.cards, 2))
    if sample != 1: cc = random.sample(cc, round(len(cc) * sample))
    max_points = PENALTY * len(cc)
    c0, c1 = c

    if hand.rows[0].cells >= 2:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_3(h.rows[0], c1)
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points

    if hand.rows[1].cells >= 2:
        h = hand.clone()
        add_card_5(h.rows[1], c0)
        add_card_5(h.rows[1], c1)
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points

    if hand.rows[2].cells >= 2:
        h = hand.clone()
        add_card_5(h.rows[2], c0)
        add_card_5(h.rows[2], c1)
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points

    if hand.rows[0].cells and hand.rows[1].cells:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_5(h.rows[1], c1)
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_3(h.rows[0], c1)
        add_card_5(h.rows[1], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points

    if hand.rows[0].cells and hand.rows[2].cells:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_5(h.rows[2], c1)
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_3(h.rows[0], c1)
        add_card_5(h.rows[2], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points

    if hand.rows[1].cells and hand.rows[2].cells:
        h = hand.clone()
        add_card_5(h.rows[1], c0)
        add_card_5(h.rows[2], c1)
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_5(h.rows[1], c1)
        add_card_5(h.rows[2], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += ss(h, item)
            if points > max_points:
                max_points = points

    return max_points / len(cc)

def s3p(hand_: Hand, c: list):
    start = dt.now()
    hand = hand_.clone()
    for item in c: hand.cards.remove(item)
    ccc = list(combinations(hand.cards, 3))
    cc = list(combinations(hand.cards, 2))
    CC = [[None] * 64 for _ in range(64)]
    pairs = list(combinations(c, 2))
    max_points = PENALTY * len(ccc)
    placement = 0

    if hand.rows[0].cells >= 2:
        max_combo0 = hand.rows[0].idx
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[0])
            add_card_3(h.rows[0], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 0), (pair[1], 0))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((pair[0], 0), (pair[1], 0))
                        max_combo0 = h.rows[0].idx

    if hand.rows[1].cells >= 2:
        max_combo1 = hand.rows[1].idx
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[1], pair[0])
            add_card_5(h.rows[1], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 1), (pair[1], 1))
                        max_combo1 = h.rows[1].idx
                    elif h.rows[1].idx > max_combo1:
                        placement = ((pair[0], 1), (pair[1], 1))
                        max_combo1 = h.rows[1].idx

    if hand.rows[2].cells >= 2:
        max_combo2 = hand.rows[2].idx
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[2], pair[0])
            add_card_5(h.rows[2], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 2), (pair[1], 2))
                        max_combo2 = h.rows[2].idx
                    elif h.rows[2].idx > max_combo2:
                        placement = ((pair[0], 2), (pair[1], 2))
                        max_combo2 = h.rows[2].idx

    if hand.rows[0].cells and hand.rows[1].cells:
        max_combo0 = hand.rows[0].idx
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[0])
            add_card_5(h.rows[1], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 0), (pair[1], 1))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((pair[0], 0), (pair[1], 1))
                        max_combo0 = h.rows[0].idx
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[1])
            add_card_5(h.rows[1], pair[0])
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 1), (pair[1], 0))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((pair[0], 1), (pair[1], 0))
                        max_combo0 = h.rows[0].idx

    if hand.rows[0].cells and hand.rows[2].cells:
        max_combo0 = hand.rows[0].idx
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[0])
            add_card_5(h.rows[2], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 0), (pair[1], 2))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((pair[0], 0), (pair[1], 2))
                        max_combo0 = h.rows[0].idx
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[1])
            add_card_5(h.rows[2], pair[0])
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 2), (pair[1], 0))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((pair[0], 2), (pair[1], 0))
                        max_combo0 = h.rows[0].idx

    if hand.rows[1].cells and hand.rows[2].cells:
        max_combo1 = hand.rows[1].idx
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[1], pair[0])
            add_card_5(h.rows[2], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 1), (pair[1], 2))
                        max_combo1 = h.rows[1].idx
                    elif h.rows[1].idx > max_combo1:
                        placement = ((pair[0], 1), (pair[1], 2))
                        max_combo1 = h.rows[1].idx
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[1], pair[1])
            add_card_5(h.rows[2], pair[0])
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((pair[0], 2), (pair[1], 1))
                        max_combo1 = h.rows[1].idx
                    elif h.rows[1].idx > max_combo1:
                        placement = ((pair[0], 2), (pair[1], 1))
                        max_combo1 = h.rows[1].idx
    print(f's3p time {(dt.now() - start).total_seconds()}, EV={max_points / len(ccc)}')
    return placement

def s3_3(hand_: Hand, c: list, sample):
    hand = hand_.clone()
    for item in c: hand.cards.remove(item)
    ccc = list(combinations(hand.cards, 3))
    if sample != 1: ccc = random.sample(ccc, round(len(ccc) * sample))
    cc = list(combinations(hand.cards, 2))
    CC = [[None] * 64 for _ in range(64)]
    pairs = list(combinations(c, 2))
    max_points = PENALTY * len(ccc)

    if hand.rows[0].cells >= 2:
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[0])
            add_card_3(h.rows[0], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points: max_points = points

    if hand.rows[1].cells >= 2:
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[1], pair[0])
            add_card_5(h.rows[1], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points: max_points = points

    if hand.rows[2].cells >= 2:
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[2], pair[0])
            add_card_5(h.rows[2], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points: max_points = points

    if hand.rows[0].cells and hand.rows[1].cells:
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[0])
            add_card_5(h.rows[1], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points:
                    max_points = points
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[1])
            add_card_5(h.rows[1], pair[0])
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points:
                    max_points = points

    if hand.rows[0].cells and hand.rows[2].cells:
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[0])
            add_card_5(h.rows[2], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points:
                    max_points = points
        for pair in pairs:
            h = hand.clone()
            add_card_3(h.rows[0], pair[1])
            add_card_5(h.rows[2], pair[0])
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points:
                    max_points = points

    if hand.rows[1].cells and hand.rows[2].cells:
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[1], pair[0])
            add_card_5(h.rows[2], pair[1])
            ss = select_ss(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points:
                    max_points = points
        for pair in pairs:
            h = hand.clone()
            add_card_5(h.rows[1], pair[1])
            add_card_5(h.rows[2], pair[0])
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: CC[item[0]][item[1]] = ss(h, item)
                for t in ccc:
                    p0, p1, p2 = CC[t[0]][t[1]], CC[t[0]][t[2]], CC[t[1]][t[2]]
                    points += max(p0, p1, p2)
                if points > max_points:
                    max_points = points

    return round(max_points / len(ccc), 3)


