from datetime import datetime as dt
from solver import *

CC = [None] * (2 ** 12)
CC2 = [None] * (2 ** 12)

def select_ss(h: Hand):
    if h.rows[0].cells:
        if h.rows[0].cells == 2: return s00
        if h.rows[1].cells: return s01
        return s02
    if h.rows[1].cells:
        if h.rows[1].cells == 2: return s11
        return s12
    return s22
def select_ss_(h: Hand):
    if h.rows[0].cells:
        if h.rows[0].cells == 2: return s00_
        if h.rows[1].cells: return s01_
        return s02_
    if h.rows[1].cells:
        if h.rows[1].cells == 2: return s11_
        return s12_
    return s22_
def s3p(hand: Hand, c: list):
    start = dt.now()
    for item in c: hand.cards.remove(item)
    ccc = list(combinations(hand.cards, 3))
    max_points = PENALTY * len(ccc)
    placement = 0
    if hand.rows[0].cells >= 2:
        h = hand.clone()
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c[0])
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c[1])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 0), (c[1], 0))
        h = hand.clone()
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c[0])
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c[2])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 0), (c[2], 0))
        h = hand.clone()
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c[1])
        h.rows[0].cells -= 1
        add_card3(h.rows[0], c[2])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 0), (c[2], 0))
    if hand.rows[1].cells >= 2:
        h = hand.clone()
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c[0])
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c[1])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 1), (c[1], 1))
        h = hand.clone()
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c[0])
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c[2])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 1), (c[2], 1))
        h = hand.clone()
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c[1])
        h.rows[1].cells -= 1
        add_card5(h.rows[1], c[2])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 1), (c[2], 1))
    if hand.rows[2].cells >= 2:
        h = hand.clone()
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c[0])
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c[1])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 2), (c[1], 2))
        h = hand.clone()
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c[0])
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c[2])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 2), (c[2], 2))
        h = hand.clone()
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c[1])
        h.rows[2].cells -= 1
        add_card5(h.rows[2], c[2])
        ss = select_ss(h)
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 2), (c[2], 2))
    if hand.rows[0].cells and hand.rows[1].cells:
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        ss = select_ss(h)
        add_card3(h.rows[0], c[0])
        add_card5(h.rows[1], c[1])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 0), (c[1], 1))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        add_card3(h.rows[0], c[0])
        add_card5(h.rows[1], c[2])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 0), (c[2], 1))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        add_card3(h.rows[0], c[1])
        add_card5(h.rows[1], c[0])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 0), (c[0], 1))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        add_card3(h.rows[0], c[1])
        add_card5(h.rows[1], c[2])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 0), (c[2], 1))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        add_card3(h.rows[0], c[2])
        add_card5(h.rows[1], c[0])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[2], 0), (c[0], 1))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[1].cells -= 1
        add_card3(h.rows[0], c[2])
        add_card5(h.rows[1], c[1])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[2], 0), (c[1], 1))

    if hand.rows[0].cells and hand.rows[2].cells:
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        ss = select_ss(h)
        add_card3(h.rows[0], c[0])
        add_card5(h.rows[2], c[1])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 0), (c[1], 2))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        add_card3(h.rows[0], c[0])
        add_card5(h.rows[2], c[2])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 0), (c[2], 2))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        add_card3(h.rows[0], c[1])
        add_card5(h.rows[2], c[0])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 0), (c[0], 2))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        add_card3(h.rows[0], c[1])
        add_card5(h.rows[2], c[2])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 0), (c[2], 2))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        add_card3(h.rows[0], c[2])
        add_card5(h.rows[2], c[0])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[2], 0), (c[0], 2))
        h = hand.clone()
        h.rows[0].cells -= 1
        h.rows[2].cells -= 1
        add_card3(h.rows[0], c[2])
        add_card5(h.rows[2], c[1])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[2], 0), (c[1], 2))

    if hand.rows[1].cells and hand.rows[2].cells:
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        ss = select_ss(h)
        add_card5(h.rows[1], c[0])
        add_card5(h.rows[2], c[1])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 1), (c[1], 2))
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        add_card5(h.rows[1], c[0])
        add_card5(h.rows[2], c[2])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[0], 1), (c[2], 2))
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        add_card5(h.rows[1], c[1])
        add_card5(h.rows[2], c[0])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 1), (c[0], 2))
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        add_card5(h.rows[1], c[1])
        add_card5(h.rows[2], c[2])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[1], 1), (c[2], 2))
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        add_card5(h.rows[1], c[2])
        add_card5(h.rows[2], c[0])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[2], 1), (c[0], 2))
        h = hand.clone()
        h.rows[1].cells -= 1
        h.rows[2].cells -= 1
        add_card5(h.rows[1], c[2])
        add_card5(h.rows[2], c[1])
        if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
            points = 0
            for item in ccc: points += ss(h, item)
            if points > max_points:
                max_points = points
                placement = ((c[2], 1), (c[1], 2))
    print(f'triple time {(dt.now() - start).total_seconds()}, EV={max_points / len(ccc)}')
    return placement

def s3p_(hand: Hand, c: list):
    start = dt.now()
    for item in c: hand.cards.remove(item)
    cc = list(combinations(hand.cards, 2))
    max_points = PENALTY * len(cc)
    p = 0

    for c0, c1 in combinations(c, 2):
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c0)
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c1)
            ss = select_ss_(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))

        if hand.rows[1].cells >= 2:
            h = hand.clone()
            h.rows[1].cells -= 1
            add_card5(h.rows[1], c0)
            h.rows[1].cells -= 1
            add_card5(h.rows[1], c1)
            ss = select_ss_(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))

        if hand.rows[2].cells >= 2:
            h = hand.clone()
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c0)
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c1)
            ss = select_ss_(h)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))

        if hand.rows[0].cells and hand.rows[1].cells:
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c0)
            add_card5(h.rows[1], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            add_card3(h.rows[0], c1)
            add_card5(h.rows[1], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))

        if hand.rows[0].cells and hand.rows[2].cells:
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c0)
            add_card5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            add_card3(h.rows[0], c1)
            add_card5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))

        if hand.rows[1].cells and hand.rows[2].cells:
            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card5(h.rows[1], c0)
            add_card5(h.rows[2], c1)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))
            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            add_card5(h.rows[1], c1)
            add_card5(h.rows[2], c0)
            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                points = 0
                for item in cc: points += ss(h, item)
                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))

    print(f'elapsed time {(dt.now() - start).total_seconds()}')
    print(f'double version EV={max_points / len(cc)}')
    return p

def s3p_2(hand: Hand, c: list):
    start = dt.now()
    for item in c:
        hand.cards.remove(item)

    cc = list(combinations(hand.cards, 2))
    ccc = list(combinations(hand.cards, 3))
    max_points = PENALTY * len(ccc)
    p = 0

    for c0, c1 in combinations(c, 2):

        # 00
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c0)
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c1)
            ss = select_ss_(h)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))

        # 11
        if hand.rows[1].cells >= 2:
            h = hand.clone()
            h.rows[1].cells -= 1
            add_card5(h.rows[1], c0)
            h.rows[1].cells -= 1
            add_card5(h.rows[1], c1)
            ss = select_ss_(h)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))

        # 22
        if hand.rows[2].cells >= 2:
            h = hand.clone()
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c0)
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c1)
            ss = select_ss_(h)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))

        # 01
        if hand.rows[0].cells and hand.rows[1].cells:
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c0)
            add_card5(h.rows[1], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c1)
            add_card5(h.rows[1], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))

        # 02
        if hand.rows[0].cells and hand.rows[2].cells:
            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c0)
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))

        # 12
        if hand.rows[1].cells and hand.rows[2].cells:
            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card5(h.rows[1], c0)
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))

            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card5(h.rows[1], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))

    print(f'from doubles time {(dt.now() - start).total_seconds()}, EV={max_points / len(ccc)}')
    return p

def s3(hand: Hand, c: list):
    for item in c:
        hand.cards.remove(item)

    cc = list(combinations(hand.cards, 2))
    ccc = list(combinations(hand.cards, 3))
    max_points = PENALTY * len(ccc)
    p = 0

    for c0, c1 in combinations(c, 2):

        # 00
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c0)
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c1)
            ss = select_ss_(h)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

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
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

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
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

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
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c1)
            add_card5(h.rows[1], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

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
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card3(h.rows[0], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

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
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points

            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            ss = select_ss_(h)
            add_card5(h.rows[1], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    CC[(pair[0] << 6) + pair[1]] = ss(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC[(t0 << 6) + t1]
                    p1 = CC[(t0 << 6) + t2]
                    p2 = CC[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2
                    points += max_p

                if points > max_points:
                    max_points = points

    return max_points / len(ccc)

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

def s2p(hand: Hand, c: list):
    start = dt.now()

    for item in c:
        hand.cards.remove(item)

    cc = list(combinations(hand.cards, 2))
    ccc = list(combinations(hand.cards, 3))
    max_points = PENALTY * len(ccc)
    p = 0
    iterations = 0
    calls = 0
    for c0, c1 in combinations(c, 2):

        # 00
        if hand.rows[0].cells >= 2:
            h = hand.clone()
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c0)
            h.rows[0].cells -= 1
            add_card3(h.rows[0], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 0))
        # 11
        if hand.rows[1].cells >= 2:
            h = hand.clone()
            h.rows[1].cells -= 1
            add_card5(h.rows[1], c0)
            h.rows[1].cells -=1
            add_card5(h.rows[1], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 1))

        # 22
        if hand.rows[2].cells >= 2:
            h = hand.clone()
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c0)
            h.rows[2].cells -= 1
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c0, 2), (c1, 2))

        # 01
        if hand.rows[0].cells and hand.rows[1].cells:

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            add_card3(h.rows[0], c0)
            add_card5(h.rows[1], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 1))

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[1].cells -= 1
            add_card3(h.rows[0], c1)
            add_card5(h.rows[1], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 1))

        # 02
        if hand.rows[0].cells and hand.rows[2].cells:

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            add_card3(h.rows[0], c0)
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c0, 0), (c1, 2))

            h = hand.clone()
            h.rows[0].cells -= 1
            h.rows[2].cells -= 1
            add_card3(h.rows[0], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c1, 0), (c0, 2))

        # 12
        if hand.rows[1].cells and hand.rows[2].cells:

            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            add_card5(h.rows[1], c0)
            add_card5(h.rows[2], c1)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c0, 1), (c1, 2))

            h = hand.clone()
            h.rows[1].cells -= 1
            h.rows[2].cells -= 1
            add_card5(h.rows[1], c1)
            add_card5(h.rows[2], c0)

            if h.rows[0].idx <= h.rows[1].max_idx and h.rows[1].idx <= h.rows[2].max_idx:
                for pair in cc:
                    calls += 1
                    CC2[(pair[0] << 6) + pair[1]] = s3_pair(h, pair)

                points = 0
                for t0, t1, t2 in ccc:
                    p0 = CC2[(t0 << 6) + t1]
                    p1 = CC2[(t0 << 6) + t2]
                    p2 = CC2[(t1 << 6) + t2]

                    if p0 > p1:
                        max_p = p0 if p0 > p2 else p2
                    else:
                        max_p = p1 if p1 > p2 else p2

                    points += max_p
                    iterations += 1

                if points > max_points:
                    max_points = points
                    p = ((c1, 1), (c0, 2))

    print(f'elapsed time {(dt.now() - start).total_seconds()}, iterations {iterations}, calls {calls}')
    print(f's2p EV={max_points / len(ccc)}')

    return p

