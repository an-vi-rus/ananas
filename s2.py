from itertools import combinations
from datetime import datetime as dt
import random
from solver import *

CC = [None] * (2 ** 12)

def s3_pair(hand: Hand, c: tuple):

    cc = list(combinations(hand.cards, 2))
    max_points = PENALTY * len(cc)

    c0, c1 = c

    # 00
    if hand.rows[0].cells >= 2:
        h = hand.clone()
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c0)
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c1)
        ss = select_ss_(h)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

    # 11
    if hand.rows[1].cells >= 2:
        h = hand.clone()
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c0)
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c1)
        ss = select_ss_(h)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

    # 22
    if hand.rows[2].cells >= 2:
        h = hand.clone()
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c0)
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c1)
        ss = select_ss_(h)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

    # 01
    if hand.rows[0].cells and hand.rows[1].cells:
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        ss = select_ss_(h)
        add_card3(h.rows[0], c0)
        add_card5(h.rows[1], c1)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        ss = select_ss_(h)
        add_card3(h.rows[0], c1)
        add_card5(h.rows[1], c0)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

    # 02
    if hand.rows[0].cells and hand.rows[2].cells:
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        ss = select_ss_(h)
        add_card3(h.rows[0], c0)
        add_card5(h.rows[2], c1)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        ss = select_ss_(h)
        add_card3(h.rows[0], c1)
        add_card5(h.rows[2], c0)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

    # 12
    if hand.rows[1].cells and hand.rows[2].cells:
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        ss = select_ss_(h)
        add_card5(h.rows[1], c0)
        add_card5(h.rows[2], c1)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        ss = select_ss_(h)
        add_card5(h.rows[1], c1)
        add_card5(h.rows[2], c0)

        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for pair in cc:
                points += ss(h, pair)
            if points > max_points:
                max_points = points

    return max_points / len(cc)

def s2p(hand: Hand, c: list, sample=0):
    start = dt.now()

    for item in c: hand.cards.remove(item)
    cc = list(combinations(hand.cards, 2))
    ccc = list(combinations(hand.cards, 3))
    if sample: ccc = random.sample(ccc, sample)
    max_points = PENALTY * len(ccc)
    p = 0

    for c0, c1 in combinations(c, 2):
####################
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c0)
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))
####################
        if hand.rows[1].cells >= 2:
            h = hand.clone()
            h.rows[1].cells -= 1
            add_card5(h.rows[1], c0)
            h.rows[1].cells -=1
            add_card5(h.rows[1], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0 
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))
####################
        if hand.rows[2].cells >= 2:
            h = hand.clone()
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c0)
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))
####################
        if hand.rows[0].cells and hand.rows[1].cells:
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            add_card3(h.rows[0], c0)
            add_card5(h.rows[1], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            add_card3(h.rows[0], c1)
            add_card5(h.rows[1], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))
####################
        if hand.rows[0].cells and hand.rows[2].cells:
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            add_card3(h.rows[0], c0)
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            add_card3(h.rows[0], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))
####################
        if hand.rows[1].cells and hand.rows[2].cells:
            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            add_card5(h.rows[1], c0)
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))

            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            add_card5(h.rows[1], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc: CC[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)
                points = 0
                for t0, t1, t2 in ccc:
                    p0, p1, p2 = CC[(t0 << 6) + t1], CC[(t0 << 6) + t2], CC[(t1 << 6) + t2]
                    max_p = max(p0, p1, p2)
                    points += max_p
                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))

    print(f'elapsed time {(dt.now() - start).total_seconds()}, ccc size {len(ccc)}')
    print(f's2p EV={max_points / len(ccc)}')

    return p