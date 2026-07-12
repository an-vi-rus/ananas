from collections import Counter
from itertools import combinations, product
from aux import show_cards

def ranks_dict(free_cards) -> dict:
    r_s = {}
    for i in range(13): r_s[i] = []
    for card in free_cards: r_s[card // 4].append(card % 4)
    return r_s
def suits_dict(free_cards) -> dict:
    s_r = {}
    for i in range(4): s_r[i] = []
    for card in free_cards: s_r[card % 4].append(card // 4)
    return s_r

def combo5(hand: list):
    rank_list = [card // 4 for card in sorted(hand, reverse=True)]
    rank_counter = Counter(rank_list).most_common()
    ranks = list(item[0] for item in rank_counter)
    match len(ranks):
        case 5: return(0, ranks)
        case 4: return(1, ranks)
        case 3: return (2, ranks) if rank_counter[1][1] == 2 else (3, ranks)
        case 2: return (6, ranks) if rank_counter[1][1] == 2 else (7, ranks)
def combo4(hand: list):
    rank_list = [card // 4 for card in sorted(hand, reverse=True)]
    rank_counter = Counter(rank_list).most_common()
    ranks = list(item[0] for item in rank_counter)
    match len(ranks):
        case 4: return(0, ranks)
        case 3: return(1, ranks)
        case 2: return (2, ranks) if rank_counter[1][1] == 2 else (3, ranks)
    return (7, ranks)
def combo3(hand: list):
    rank_list = [card // 4 for card in sorted(hand, reverse=True)]
    rank_counter = Counter(rank_list).most_common()
    ranks = list(item[0] for item in rank_counter)
    match len(ranks):
        case 3: return (0, ranks)
        case 2: return (1, ranks)
    return (3, ranks)
def combo2(hand: list):
    ranks = list(card // 4 for card in sorted(hand, reverse=True))
    return (1, [ranks[0]]) if ranks[0] == ranks[1] else (0, ranks)

def card3_combo(hand: list):
    match len(hand):
        case 1: return (0, (hand[0] // 4,))
        case 2: 
            ranks = tuple(card // 4 for card in sorted(hand, reverse=True))
            return (1, (ranks[0],)) if ranks[0] == ranks[1] else (0, ranks)
        case 3:
            rank_list = [card // 4 for card in sorted(hand, reverse=True)]
            rank_counter = Counter(rank_list).most_common()
            ranks = tuple(item[0] for item in rank_counter)
            match len(ranks):
                case 3: return (0, ranks)
                case 2: return (1, ranks)
            return (3, ranks)
    

    pass

# Max combinations noStraight, noFlush 
def max_combo4_1(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    match combo[0]:
        case 1:
            rank = combo[1][0]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (3, combo[1])
            rank = combo[1][1]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (2, combo[1])
            rank = combo[1][2]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (2, (combo[1][0], combo[1][2], combo[1][1]))
        case 2:
            rank = combo[1][0]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (6, combo[1])
            rank = combo[1][1]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (6, (combo[1][1], combo[1][0]))
        case 3:
            rank = combo[1][1]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (6, combo[1])
            rank = combo[1][0]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (7, combo[1])
        case 0:
            for rank in combo[1]:
                ranks = list(combo[1])
                ranks.remove(rank)
                for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (1, (rank, *ranks))
    return max_combos

def max_combo1_1(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    rank = combo[1][0]
    for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (1, combo[1])
    return max_combos

def max_combo1_2(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    rank = combo[1][0]
    if len(rank_suits[rank]) >=2:
        suits = list(combinations(rank_suits[rank], 2))
        for item in suits:
            key = (rank*4 + item[0], rank*4 + item[1])
            max_combos[key] = (3, (rank,))
    return max_combos

def max_combo3_1(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    match combo[0]:
        case 1:
            rank = combo[1][0]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (3, combo[1])
            rank = combo[1][1]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (2, combo[1])
        case 3:
            rank = combo[1][0]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (7, combo[1])
        case 0:
            for rank in combo[1]:
                ranks = list(combo[1])
                ranks.remove(rank)
                for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (1, (rank, *ranks))
    return max_combos
def max_combo3_2(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    match combo[0]:
        case 1:
            rank = combo[1][0]
            if len(rank_suits[rank]) == 2:
                key = tuple(rank*4 + suit for suit in rank_suits[rank])
                max_combos[key] = (7, combo[1])
            rank2 = combo[1][1]
            if len(rank_suits[rank2]) >= 2:
                suits = list(combinations(rank_suits[rank2], 2))
                for suit in suits:
                    key = tuple(rank2*4 +  item for item in suit)
                    max_combos[key] = (6, (combo[1][1], combo[1][0]))
            if len(rank_suits[rank]) >= 0 and len(rank_suits[rank2]) >= 0:
                for suit1 in rank_suits[rank]:
                    for suit2 in rank_suits[rank2]:
                        key = (rank*4 + suit1, rank2*4 + suit2)
                        max_combos[key] = (6, combo[1])
        case 0:
            for rank in combo[1]:
                if len(rank_suits[rank]) >=2:
                    suits = list(combinations(rank_suits[rank], 2))
                    for item in suits:
                        key = (rank*4 + item[0], rank*4 + item[1])
                        max_combos[key] = (3, (rank,))
            ranks = list(combinations(combo[1], 2))
            for item in ranks:
                if set(item) <= set(rank_suits.keys()):
                    for suit1 in rank_suits[item[0]]:
                        for suit2 in rank_suits[item[1]]:
                            key = (item[0]*4 + suit1, item[1]*4 + suit2)
                            max_combos[key] = (2, (*item, list(set(combo[1]) - set(item))[0]))
    return max_combos

def max_combo2_1(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    match combo[0]:
        case 1:
            rank = combo[1][0]
            for suit in rank_suits[rank]: max_combos[rank*4 + suit] = (3, combo[1])
        case 0:
            rank = combo[1][0]
            for suit in rank_suits[rank]:
                max_combos[rank*4 + suit] = (1, combo[1])
            rank = combo[1][1]
            for suit in rank_suits[rank]:
                max_combos[rank*4 + suit] = (1, (combo[1][1], combo[1][0]))
    return max_combos
def max_combo2_2(combo: tuple, rank_suits: dict) -> dict:
    max_combos = {}
    match combo[0]:
        case 1:
            rank = combo[1][0]
            if len(rank_suits[rank]) == 2:
                key = tuple(rank*4 + suit for suit in rank_suits[rank])
                max_combos[key] = (7, combo[1])
        case 0:
            if set(combo[1]) <= set(rank_suits.keys()):
                for suit1 in rank_suits[combo[1][0]]:
                    for suit2 in rank_suits[combo[1][1]]:
                        key = (combo[1][0]*4 + suit1, combo[1][1]*4 + suit2)
                        max_combos[key] = (2, combo[1])
    return max_combos

def c5_4(combo: tuple, rank: int) -> tuple:
    #rank = card // 4
    match combo[0]:
        case 1:
            if rank == combo[1][0]: return(3, combo[1])
            if rank == combo[1][1]:
                return (2, combo[1]) if combo[1][0] > combo[1][1] else (2, [combo[1][1], combo[1][0], combo[1][2]])
            if rank == combo[1][2]:
                return (2, [combo[1][0], combo[1][2], combo[1][1]]) if combo[1][0] > combo[1][2] else (2, [combo[1][2], combo[1][0], combo[1][1]])
            r = sorted(combo[1][1:3] + [rank], reverse=True)
            return (1, [combo[1][0]] + r)
        case 2:
            if rank == combo[1][0]:
                return (6, combo[1])
            if rank == combo[1][1]:
                return (6, [combo[1][1], combo[1][0]])
            return (2, combo[1] + [rank])
        case 0:
            r = combo[1][:]
            if rank in r:
                r.remove(rank)
                return (1, [rank] + r)
            r = sorted(combo[1] + [rank], reverse=True)
            return (0, r)
        case 3:
            if rank == combo[1][0]: return (7, combo[1])
            if rank == combo[1][1]: return (6, combo[1])
            return (3, combo[1] + [rank]) if combo[1][0] > rank else (3, [combo[1][0], rank, combo[1][1]])
    return combo
def c4_3(combo: tuple, rank: int) -> tuple:
    #rank = card // 4
    match combo[0]:
        case 1:
            if rank == combo[1][0]:
                return (3, combo[1])
            if rank == combo[1][1]:
                return (2, combo[1]) if combo[1][0] > combo[1][1] else (2, [combo[1][1], combo[1][0]])
            return (1, combo[1] + [rank]) if combo[1][1] > rank else (1, [combo[1][0], rank, combo[1][1]])
        case 0:
            if rank in combo[1]:
                r = combo[1][:]
                r.remove(rank)
                return (1, [rank] + r)
            r = sorted(combo[1] + [rank], reverse=True)
            return (0, r)
        case 3:
            if rank == combo[1][0]: return (7, combo[1])
            return (3, [combo[1][0], rank])
def c5_3(combo: tuple, pair: list) -> tuple:
    c4 = c4_3(combo, pair[0])
    c5 = c5_4(c4, pair[1])
    if c5 is not None:
        return c5_4(c4, pair[1])
    else:
        print(c4)
def c4_2(combo: tuple, pair: list) -> tuple:
    c3 = c3_2(combo, pair[0])
    return c4_3(c3, pair[1])

def c3_2(combo: tuple, rank: int) -> tuple:
    #rank = card // 4
    match combo[0]:
        case 0:
            if rank in combo[1]:
                r = combo[1][:]
                r.remove(rank)
                return (1, [rank] + r)
            r = sorted(combo[1] + [rank], reverse=True)
            return (0, r)
        case 1:
            if rank == combo[1][0]:
                return (3, combo[1])
            else: 
                return (1, combo[1] + [rank])
def c3_1(combo: tuple, pair: list) -> tuple:
    #rank0 = pair[0] // 4
    #rank1 = pair[1] // 4
    if pair[0] == pair[1]:
        if pair[0] == combo[1][0]: return (3, combo[1])
        else: return (1, [pair[0], combo[1][0]])
    else:
        if pair[0] == combo[1][0]: return (1, [pair[0], pair[1]])
        if pair[1] == combo[1][0]: return (1, [pair[1], pair[0]])
        r = sorted([pair[0], pair[1], combo[1][0]], reverse=True)
        return (0, r)
def c2_1(combo: tuple, card: int) -> tuple:
    rank = card // 4
    if combo[1][0] == rank: return(1, combo[1])
    return (0, [combo[1][0], rank]) if combo[1][0] > rank else (0, [rank, combo[1][0]])

def addcard(combo: tuple, rank: int) -> tuple:
    match combo[0]:
        case 6 | 7: return combo
        case 3:
            if combo[1][0] == rank: return (7, combo[1])
            if len(combo[1]) == 2 and combo[1][1] == rank: return (6, combo[1])
            return (3, combo[1] + [rank])
        case 2:
            if combo[1][0] == rank: return (6, combo[1])
            if combo[1][1] == rank: return (6, [combo[1][1], combo[1][0]])
            return (2, combo[1] + [rank])
        case 1:
            match len(combo[1]):
                case 1:
                    if combo[1][0] == rank: return (3, combo[1])
                    return (1, combo[1] + [rank])
                case 2:
                    if combo[1][0] == rank: return (3, combo[1])
                    if combo[1][1] == rank: return (2, combo[1]) if combo[1][0] > rank else (2, [rank, combo[1][0]])
                    return (1, combo[1] + [rank]) if combo[1][1] > rank else (1, [combo[1][0], rank, combo[1][1]])
                case 3:
                    if combo[1][0] == rank: return (3, combo[1])
                    if combo[1][1] == rank: return (2, combo[1]) if combo[1][0] > rank else (2, [rank, combo[1][0], combo[1][2]])
                    if combo[1][2] == rank: return (2, [combo[1][0], rank, combo[1][1]]) if combo[1][0] > rank else (2, [rank, combo[1][0], combo[1][1]])
                    return (1, sorted(combo[1][1:3] + [rank], reverse=True))
        case 0:
            if rank in combo[1]:
                temp = combo[1][:]
                temp.remove(rank)
                return (1, [rank] + temp)
            return (0, sorted(combo[1] + [rank], reverse=True))
        case -1: return (0, [rank])
def addpair(combo: tuple, pair: list) -> tuple:
    c = addcard(combo, pair[0])
    return addcard(c, pair[1]) 
def max_combo(combo: tuple) -> tuple:
    match combo[0]:
        case 6 | 7: return combo
        case 3: return (7, combo[1])
        case 2: return (6, combo[1])
        case 1:
            if len(combo[1]) < 3: return (7, combo[1])
            return (3, combo[1])
        case 0: 
            if len(combo[1]) < 3: return (7, combo[1])
            if len(combo[1]) == 3: return (3, combo[1])
            return (2, combo[1])
        case -1: return (7, [12])
    pass

def print_combo(combos: dict):
    for key in combos:
        print(f'card(s) {show_cards(list(key))}, combo {combos[key]}')



