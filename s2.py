from itertools import combinations
from datetime import datetime as dt
import random
from solver import *
import s3

def s2p(hand_: Hand, c: list, sample):
    start = dt.now()
    hand = hand_.clone()
    for item in c: hand.cards.remove(item)
    cc = list(combinations(hand.cards, 2))
    if sample != 1: cc = random.sample(cc, round(len(cc) * sample))
    pairs = list(combinations(c, 2))
    max_points = PENALTY * len(cc)
    placement = 0
    
    for pair in pairs:
        c0, c1 = pair
        if hand.rows[0].cells >= 2:
            max_combo0 = hand.rows[0].idx
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_3(h.rows[0], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 0), (c1, 0))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((c0, 0), (c1, 0))
                        max_combo0 = h.rows[0].idx

        if hand.rows[1].cells >= 2:
            max_combo1 = hand.rows[1].idx
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 1), (c1, 1))
                        max_combo1 = h.rows[1].idx
                    elif h.rows[1].idx > max_combo1:
                        placement = ((c0, 1), (c1, 1))
                        max_combo1 = h.rows[1].idx

        if hand.rows[2].cells >= 2:
            max_combo2 = hand.rows[2].idx
            h = hand.clone()
            add_card_5(h.rows[2], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 2), (c1, 2))
                        max_combo2 = h.rows[2].idx
                    elif h.rows[2].idx > max_combo2:
                        placement = ((c0, 2), (c1, 2))
                        max_combo2 = h.rows[2].idx

        if hand.rows[0].cells and hand.rows[1].cells:
            max_combo0 = hand.rows[0].idx
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 0), (c1, 1))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((c0, 0), (c1, 1))
                        max_combo0 = h.rows[0].idx
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[1], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 1), (c1, 0))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((c0, 1), (c1, 0))
                        max_combo0 = h.rows[0].idx

        if hand.rows[0].cells and hand.rows[2].cells:
            max_combo0 = hand.rows[0].idx
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 0), (c1, 2))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((c0, 0), (c1, 2))
                        max_combo0 = h.rows[0].idx
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 2), (c1, 0))
                        max_combo0 = h.rows[0].idx
                    elif h.rows[0].idx > max_combo0:
                        placement = ((c0, 2), (c1, 0))
                        max_combo0 = h.rows[0].idx

        if hand.rows[1].cells and hand.rows[2].cells:
            max_combo1 = hand.rows[1].idx
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 1), (c1, 2))
                        max_combo1 = h.rows[1].idx
                    elif h.rows[1].idx > max_combo1:
                        placement = ((c0, 1), (c1, 2))
                        max_combo1 = h.rows[1].idx
            h = hand.clone()
            add_card_5(h.rows[1], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points >= max_points:
                    if points > max_points:
                        max_points = points
                        placement = ((c0, 2), (c1, 1))
                        max_combo1 = h.rows[1].idx
                    elif h.rows[1].idx > max_combo1:
                        placement = ((c0, 2), (c1, 1))
                        max_combo1 = h.rows[1].idx

    print(f's2p time {(dt.now() - start).total_seconds()}, EV={max_points / len(cc)}, ccc {len(cc)}')
    return placement


def s2(hand_: Hand, c: list, sample):
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
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))

        if hand.rows[1].cells >= 2:
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))

        if hand.rows[2].cells >= 2:
            h = hand.clone()
            add_card_5(h.rows[2], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))


        if hand.rows[0].cells and hand.rows[1].cells:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[1], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))

        if hand.rows[0].cells and hand.rows[2].cells:
            h = hand.clone()
            add_card_3(h.rows[0], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))
            h = hand.clone()
            add_card_3(h.rows[0], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))

        if hand.rows[1].cells and hand.rows[2].cells:
            h = hand.clone()
            add_card_5(h.rows[1], c0)
            add_card_5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))
            h = hand.clone()
            add_card_5(h.rows[1], c1)
            add_card_5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += s3.s3_2(h, item, sample)
                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))

    print(f'double time {(dt.now() - start).total_seconds()} EV= {max_points / len(cc)}')
    return p

def s2_2(hand_: Hand, c: list, sample):
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
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points

    if hand.rows[1].cells >= 2:
        h = hand.clone()
        add_card_5(h.rows[1], c0)
        add_card_5(h.rows[1], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points

    if hand.rows[2].cells >= 2:
        h = hand.clone()
        add_card_5(h.rows[2], c0)
        add_card_5(h.rows[2], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points

    if hand.rows[0].cells and hand.rows[1].cells:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_5(h.rows[1], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_3(h.rows[0], c1)
        add_card_5(h.rows[1], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points

    if hand.rows[0].cells and hand.rows[2].cells:
        h = hand.clone()
        add_card_3(h.rows[0], c0)
        add_card_5(h.rows[2], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_3(h.rows[0], c1)
        add_card_5(h.rows[2], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points

    if hand.rows[1].cells and hand.rows[2].cells:
        h = hand.clone()
        add_card_5(h.rows[1], c0)
        add_card_5(h.rows[2], c1)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points
        h = hand.clone()
        add_card_5(h.rows[1], c1)
        add_card_5(h.rows[2], c0)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in cc: points += s3.s3_2(h, item, sample)
            if points > max_points:
                max_points = points

    return max_points / len(cc)


