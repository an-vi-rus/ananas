from itertools import combinations, product
import random
from collections import Counter
from datetime import datetime as dt
from solver import MIDDLE_ROYALTY, LOW_ROYALTY

HIGH_ROYALTY = (
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    10, 11, 12, 13, 14, 16, 16, 17, 18, 19, 20, 21, 22, 0,  0,  0
)

def row_combos(cards: list):
    cards = sorted(cards, reverse=True)

    suit_cards = [[] for _ in range(4)]
    rank_cards = [[] for _ in range(13)]
    ranks = set()

    for card in cards:
        suit_cards[card & 3].append(card)
        rank_cards[card >> 2].append(card)
        ranks.add(card >> 2)

    combos = {}

    for i in range(13):
        rank = tuple(rank_cards[i])

        if len(rank) == 4:
            combos.setdefault((7 << 4) | i, []).append(rank)
            combos.setdefault((3 << 4) | i, []).extend(combinations(rank, 3))
            combos.setdefault((1 << 4) | i, []).extend(combinations(rank, 2))

        elif len(rank) == 3:
            combos.setdefault((3 << 4) | i, []).append(rank)
            combos.setdefault((1 << 4) | i, []).extend(combinations(rank, 2))

        elif len(rank) == 2:
            combos.setdefault((1 << 4) | i, []).append(rank)

    if len(ranks) >= 5:
        for i in range(12, 2, -1):
            combos.setdefault((4 << 4) | i, []).extend(product(rank_cards[i],rank_cards[i - 1],rank_cards[i - 2],rank_cards[i - 3],rank_cards[i - 4]))

        # wheel: A-5-4-3-2
        combos.setdefault((4 << 4) | 3, []).extend(
            product(rank_cards[12],rank_cards[3],rank_cards[2],rank_cards[1],rank_cards[0]))

    # full house
    for triple_key, triples in list(combos.items()):
        if triple_key >> 4 != 3:
            continue

        triple_rank = triple_key & 0xf

        for pair_key, pairs in list(combos.items()):
            if pair_key >> 4 != 1:
                continue

            if triple_rank != (pair_key & 0xf):
                combos.setdefault(
                    (6 << 4) | triple_rank,
                    []
                ).extend(
                    triple + pair
                    for triple in triples
                    for pair in pairs
                )

    # two pair
    pairs = [
        (key, value)
        for key, value in combos.items()
        if key >> 4 == 1
    ]

    for n, (key1, pairs1) in enumerate(pairs):
        rank1 = key1 & 0xf

        for key2, pairs2 in pairs[n + 1:]:
            rank2 = key2 & 0xf

            if rank1 == rank2:
                continue

            high_rank = max(rank1, rank2)

            combos.setdefault(
                (2 << 4) | high_rank,
                []
            ).extend(
                pair1 + pair2
                for pair1 in pairs1
                for pair2 in pairs2
            )

    # flush / straight flush
    for i in range(4):
        suit = tuple(suit_cards[i])

        if len(suit) < 5:
            continue

        combos.setdefault((5 << 4) | (suit[0] >> 2), []).extend(
            combinations(suit, 5)
        )

        for j in range(4, len(suit)):
            if (suit[j - 4] >> 2) - (suit[j] >> 2) == 4:
                high_rank = suit[j - 4] >> 2

                combos.setdefault(
                    (8 << 4) | high_rank,
                    []
                ).append(suit[j - 4:j + 1])

        # wheel straight flush
        if (
            suit[0] >> 2 == 12
            and suit[-4] >> 2 == 3
        ):
            combos.setdefault((8 << 4) | 3, []).append(
                suit[0:1] + suit[-4:]
            )

    return combos

def middle_combos(cards: list):
    result = {}

    combos2 = row_combos(cards)

    for key2 in combos2:
        for item2 in combos2[key2]:
            cards_ = cards[:]

            for card in item2:
                cards_.remove(card)

            combos1 = row_combos(cards_)

            for key1 in combos1:
                if key1 <= key2:
                    result.setdefault((key1, key2), []).extend(
                        (item1, item2) for item1 in combos1[key1]
                    )

    return result

def solve(cards: list):
    max_points = 0
    p = 0
    rank_cards = [[] for _ in range(13)]

    combos = middle_combos(cards)

    for key in combos:
        for j in combos[key]:
            cards_ = cards[:]

            for card in j[0]:
                cards_.remove(card)

            for card in j[1]:
                cards_.remove(card)

            for rank_cards_ in rank_cards:
                rank_cards_.clear()

            for card in cards_:
                rank_cards[card >> 2].append(card)

            for k in range(13):
                rank = tuple(rank_cards[k])

                if len(rank) == 3:
                    if key[0] >= 48 + k:
                        points = (
                            HIGH_ROYALTY[48 + k]
                            + MIDDLE_ROYALTY[key[0]]
                            + LOW_ROYALTY[key[1]]
                        )

                        if points > max_points:
                            max_points = points
                            p = (
                                tuple((card, 0) for card in rank),
                                tuple((card, 1) for card in j[0]),
                                tuple((card, 2) for card in j[1])
                            )
                elif len(rank) == 2:
                    if key[0] >= 16 + k:
                        points = (
                            HIGH_ROYALTY[16 + k]
                            + MIDDLE_ROYALTY[key[0]]
                            + LOW_ROYALTY[key[1]]
                        )

                        if points > max_points:
                            max_points = points
                            p = (
                                tuple((card, 0) for card in rank),
                                tuple((card, 1) for card in j[0]),
                                tuple((card, 2) for card in j[1])
                            )

                else:
                    points = (
                        MIDDLE_ROYALTY[key[0]]
                        + LOW_ROYALTY[key[1]]
                    )

                    if points > max_points:
                        max_points = points
                        p = (
                            tuple((card, 0) for card in rank),
                            tuple((card, 1) for card in j[0]),
                            tuple((card, 2) for card in j[1])
                        )

    return p

def test_solve(cards: list):
    max_points = 0
    combos = row_combos(cards)
    items = []
    for kind, combinations in combos.items():
        for cards in combinations:
            items.append((kind, cards))
    items.sort(reverse=True, key=lambda item: (item[0], item[1]))
    items.append((0, tuple()))
    items3 = [item for item in items if (item[0] >> 4) in [0, 1, 3]]

    for i in range(len(items)):
        for j in range(i):
            if set(items[i][1]) & set(items[j][1]): continue
            for k in range(len(items3)):
                if set(items3[k][1]) & (set(items[i][1]) | set(items[j][1])): continue
                if items3[k][0] > items[i][0]: continue
                points = HIGH_ROYALTY[items3[k][0]] + MIDDLE_ROYALTY[items[i][0]] + LOW_ROYALTY[items[j][0]]
                if points > max_points:
                    max_points = points

    return max_points

seed = 0 
deck = list(range(52))
random.seed()
n = 10000
start = dt.now()
f = 0
#for _ in range(n):
#    sample = random.sample(deck, 17)
#    f += test_solve(sample)
#print(f'fantasy = {round(f / n, 2)}, time = {(dt.now() - start).total_seconds()}')




        