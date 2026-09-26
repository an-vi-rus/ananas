import s2
from solver import *
from datetime import datetime as dt
import random

def s1p(hand_: Hand, c: list, sample):
    start = dt.now()
    hand = hand_.clone()
    for item in c: hand.cards.remove(item)
    cc = list(combinations(hand.cards, 2))
    if sample != 1: cc = random.sample(cc, round(len(cc) * sample))
    max_points = PENALTY * len(cc)
    p = 0

    for c0, c1 in combinations(c, 2):
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_3(h.rows[0], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))

        if hand.rows[1].cells >= 2:
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))

        if hand.rows[2].cells >= 2:
            h = hand.clone()
            add_card_5(h.rows[2], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))

        if hand.rows[0].cells and hand.rows[1].cells:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[1], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))

        if hand.rows[0].cells and hand.rows[2].cells:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))

        if hand.rows[1].cells and hand.rows[2].cells:
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))
            h = hand.clone()
            add_card_5(h.rows[1], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s2.s2_2(h, item, sample*0.5)
                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))


#    print(f's1 time {round((dt.now() - start).total_seconds(), 3)} EV = {round(max_points / len(cc), 2)} len cc {len(cc)}')
    print(f'EV {round(max_points / len(cc), 2)}')
    return p

def s1_2(hand_: Hand, c: list, sample):
    start = dt.now()
    hand = hand_.clone()
    for item in c: hand.cards.remove(item)
    cc = list(combinations(hand.cards, 2))
    cc = random.sample(cc, 1)
    max_points = PENALTY * len(cc)
    p = 0
    c0, c1 = c

    if hand.rows[0].cells >= 2:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_3(h.rows[0], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points

    if hand.rows[1].cells >= 2:
        h = hand.clone()
        add_card_5(h.rows[1], c0)
        add_card_5(h.rows[1], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points

    if hand.rows[2].cells >= 2:
        h = hand.clone()
        add_card_5(h.rows[2], c0)
        add_card_5(h.rows[2], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points

    if hand.rows[0].cells and hand.rows[1].cells:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_5(h.rows[1], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_3(h.rows[0], c1)
        add_card_5(h.rows[1], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points

    if hand.rows[0].cells and hand.rows[2].cells:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_5(h.rows[2], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_3(h.rows[0], c1)
        add_card_5(h.rows[2], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points

    if hand.rows[1].cells and hand.rows[2].cells:
        h = hand.clone()
        add_card_5(h.rows[1], c0)
        add_card_5(h.rows[2], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_5(h.rows[1], c1)
        add_card_5(h.rows[2], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s2.s2_2(h, item, sample*0.5)
            if points > max_points:
                max_points = points


    #print(f's1 time {round((dt.now() - start).total_seconds(), 3)} EV = {round(max_points / len(cc), 2)} len cc {len(cc)}')
    return max_points

def s1_n(hand: Hand, n: int):
    start = dt.now()
    ev = 0
    for _ in range(n):
        c = random.sample(hand.cards, 2)
        ev += s1_2(hand, c, 0.05)
    print(ev / n)
    print(f'time {round((dt.now() - start).total_seconds(), 2)}')
    return round(ev / n, 3)

