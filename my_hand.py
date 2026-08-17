from itertools import combinations
from datetime import datetime as dt
from lut import LUT3_5, C_IND

penalty = -6
premium = 6
HIGH_ROW_PAIR = (0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7+premium, 8+premium, 9+premium)
MIDDLE_ROW_ROYALTY = (0, 0, 0, 2, 4, 8, 12, 20, 30, 50)
LOW_ROW_ROYALTY = (0, 0, 0, 0, 2, 4, 6, 10, 15, 25)
MASK = list([2 << i for i in range(13)])
MASK[12] |= 1
MASK5 = list([31 << i for i in range(10)])

def lut3_6():
    global C_INDEX, C_VALUES, D_INDEX, D_VALUES
    C_INDEX = {}
    C_VALUES = []
    D_INDEX = {}
    D_VALUES = []

    for idx, c in enumerate(combinations(range(12, -1, -1), 3)):
        C_INDEX[c] = idx
        C_VALUES.append(c)

    idx = 0
    for d0 in range(12, -1, -1):
        for d1 in range(d0, -1, -1):
            for d2 in range(d1, -1, -1):
                t = (d0, d1, d2)
                D_INDEX[t] = idx
                D_VALUES.append(t)
                idx += 1

    LUT = []
    for c in C_VALUES:
        row = []
        for d in D_VALUES:
            row.append(c3_6(c, d))
        LUT.append(row)
    return LUT  

def is_straight(combo: list):
    if combo[0] - combo[-1] <= 4: return min(combo[-1] + 4, 12)
    if combo[0] == 12 and combo[1] <= 3: return 3
    return 0
def get_points(combo: tuple, row: int):
    if not row:
        if not combo[0]: return 0
        if combo[0] == 1:
            if combo[1][0] < 4: return 0
            if combo[1][0] < 10: return combo[1][0] - 3
            return combo[1][0] - 3 + premium
        return combo[1][0] + 10 + premium
    if row == 1:
        if combo[0] < 3: return 0
        if combo[0] == 3: return 2
        if combo[0] == 4: return 4
        if combo[0] == 5: return 8
        if combo[0] == 6: return 12
        if combo[0] == 7: return 20
        if combo[0] == 8: return 30 if combo[1][0] < 12 else 50
    if combo[0] == 5: return 4
    if combo[0] == 6: return 6
    if combo[0] < 4: return 0
    if combo[0] == 4: return 2
    if combo[0] == 7: return 10
    if combo[0] == 8: return 15 if combo[1][0] < 12 else 25
def rank5(row: Row, card):
    rank = card // 4
    match row.cells:
        case 0:
            match row.combo[0]:
                case 1:
                    if row.combo[1][0] == rank: return (3, row.combo[1])
                    if row.combo[1][1] == rank: return (2, row.combo[1]) if row.combo[1][0] > rank else (2, [rank, row.combo[1][0], row.combo[1][2]])
                    if row.combo[1][2] == rank: return (2, [row.combo[1][0], rank, row.combo[1][1]]) if row.combo[1][0] > rank else (2, [rank, row.combo[1][0], row.combo[1][1]])
                    return (1, sorted(row.combo[1] + [rank], reverse=True))
                case 2:
                    if row.combo[1][0] == rank: return (6, row.combo[1])
                    if row.combo[1][1] == rank: return (6, [row.combo[1][1], row.combo[1][0]])
                    return (2, row.combo[1] + [rank])
                case 0:
                    if rank in row.combo[1]:
                        r = row.combo[1][:]
                        r.remove(rank)
                        return (1, [rank] + r)
                    return (0, sorted(row.combo[1] + [rank], reverse=True))
                case 3:
                    if row.combo[1][0] == rank: return (7, row.combo[1])
                    if row.combo[1][1] == rank: return (6, row.combo[1])
                    return row.combo
                case 7: return row.combo
        case 1:
            match row.combo[0]:
                case 1:
                    if rank == row.combo[1][0]: return (3, row.combo[1])
                    if rank == row.combo[1][1]: return (2, row.combo[1]) if row.combo[1][0] > rank else (2, [row.combo[1][1], row.combo[1][0]])
                    return (1, row.combo[1] + [rank]) if row.combo[1][1] > rank else (1, [row.combo[1][0], rank, row.combo[1][1]])
                case 0: 
                    if rank in row.combo[1]:
                        r = row.combo[1][:]
                        r.remove(rank)
                        return (1, [rank] + r)
                    return (0, sorted(row.combo[1] + [rank], reverse=True))
                case 3: return (7, row.combo[1]) if row.combo[1][0] == rank else (3, row.combo[1])
        case 2:
            if row.combo[0]: return (3, [rank]) if rank == row.combo[1][0] else (1, row.combo[1] + [rank])
            if rank == row.combo[1][0]: return (1, row.combo[1])
            if rank == row.combo[1][1]: return (1, [rank, row.combo[1][0]])
            return (0, sorted(row.combo[1] + [rank], reverse=True))
        case 3:
            if rank == row.combo[1][0]: return (1, [rank])
            return (0, [row.combo[1][0], rank]) if row.combo[1][0] > rank else (0, [rank, row.combo[1][0]])
        case 4: return (0, [rank])
def add_card3(row: Row, card):
    rank = card // 4
    kind, cards = row.combo
    match row.cells:
        case 0:
            if kind:
                if rank != cards[0]:
                    row.combo = (1, (cards[0], rank))
                    row.points = HIGH_ROW_PAIR[cards[0]]
                    return
                row.combo = (3, (rank,))
                row.points = rank + 10 + premium
                return
            else:
                if rank == cards[0]:
                    row.combo = (1, (rank, cards[1]))
                    row.points = HIGH_ROW_PAIR[rank]
                    return
                if rank == cards[1]:
                    row.combo = (1, (cards[1], cards[0]))
                    row.points = HIGH_ROW_PAIR[cards[1]]
                    return
                if rank > cards[0]: 
                    row.combo = (0, (rank, cards[0], cards[1]))
                    return
                elif rank > cards[1]:
                    row.combo = (0, (cards[0], rank, cards[1]))
                    return
                else:
                    row.combo = (0, (cards[0], cards[1], rank))
                    return
        case 1:
            if rank == cards[0]:
                row.combo = (1, (rank,))
                return
            row.combo = (0, (cards[0], rank)) if cards[0] > rank else (0, (rank, cards[0]))
            return
        case 2: row.combo = (0, (rank,))
def add_card_classic(row: Row, card: int):
    rank = card // 4
    kind, cards = row.combo
    match row.cells:
        case 0:
            match kind:
                case 1:
                    if rank == cards[0]:
                        row.combo = (3, (rank,))
                        row.max_combo = row.combo
                        if row.row == 1: row.points = 2
                        return
                    if rank == cards[1]:
                        row.combo = (2, (cards[0], rank, cards[2])) if rank < cards[0] else (2, (rank, cards[0], cards[2]))
                        row.max_combo = row.combo
                        return
                    if rank == cards[2]:
                        row.combo = (2, (cards[0], rank, cards[1])) if rank < cards[0] else (2, (rank, cards[0], cards[1]))
                        row.max_combo = row.combo
                        return
                    if rank > cards[1]: row.combo = (1, (cards[0], rank, cards[1], cards[2]))
                    elif rank > cards[2]: row.combo = (1, (cards[0], cards[1], rank, cards[2]))
                    else: row.combo = (1, (cards[0], cards[1], cards[2], rank))
                    row.max_combo = row.combo
                    return
                case 2:
                    if rank == cards[0]:
                        row.combo = (6, (rank, cards[1]))
                        row.max_combo = row.combo
                        row.points = 12 if row.row == 1 else 6
                        return
                    if rank == cards[1]:
                        row.combo = (6, (rank, cards[0]))
                        row.max_combo = row.combo
                        row.points = 12 if row.row == 1 else 6
                        return
                    row.combo = (2, (cards[0], cards[1], rank))
                    row.max_combo = row.combo
                    return
                case 0:
                    if rank >= cards[0]:
                        if rank > cards[0]:
                            row.combo = (0, (rank, cards[0], cards[1], cards[2], cards[3]))
                            row.max_combo = row.combo
                            return
                        row.combo = (1, (rank, cards[1], cards[2], cards[3]))
                        row.max_combo = row.combo
                        return
                    if rank >= cards[1]:
                        if rank > cards[1]:
                            row.combo = (0, (cards[0], rank, cards[1], cards[2], cards[3]))
                            row.max_combo = row.combo
                            return
                        row.combo = (1, (rank, cards[0], cards[2], cards[3]))
                        row.max_combo = row.combo
                        return
                    if rank >= cards[2]:
                        if rank > cards[2]:
                            row.combo = (0, (cards[0], cards[1], rank, cards[2], cards[3]))
                            row.max_combo = row.combo
                            return
                        row.combo = (1, (rank, cards[0], cards[1], cards[3]))
                        row.max_combo = row.combo
                        return
                    if rank >= cards[3]:
                        if rank > cards[3]:
                            row.combo = (0, (cards[0], cards[1], cards[2], rank, cards[3]))
                            row.max_combo = row.combo
                            return
                        row.combo = (1, (rank, cards[0], cards[1], cards[2]))
                        row.max_combo = row.combo
                        return
                    row.combo = (0, (cards[0], cards[1], cards[2], cards[3], rank))
                    row.max_combo = row.combo
                    return
                case 3:
                    if rank == cards[1]:
                        row.combo = (6, (cards[0], cards[1]))
                        row.max_combo = row.combo
                        row.points = 12 if row.row == 1 else 6
                        return
                    if rank == cards[0]:
                        row.combo = (7, (rank,))
                        row.max_combo = row.combo
                        row.points = 20 if row.row == 1 else 10
                        return
                    row.combo = (3, (cards[0],))
                    row.max_combo = row.combo
                    return#
            return
        case 1:
            match kind:
                case 1:
                    if rank == cards[0]:
                        row.combo = (3, (rank, cards[1]))
                        row.max_combo = (7, (rank,))
                        return
                    if rank == cards[1]:
                        row.combo = (2, (cards[0], rank)) if rank < cards[0] else (2, (rank, cards[0]))
                        row.max_combo = (6, (cards[0], cards[1]))
                        return
                    row.combo = (1, (cards[0], cards[1], rank)) if rank < cards[1] else (1, (cards[0], rank, cards[1]))
                    row.max_combo = (3, (cards[0],))
                    return
                case 0: 
                    if rank >= cards[0]:
                        if rank > cards[0]:
                            row.combo = (0, (rank, cards[0], cards[1], cards[2]))
                            row.max_combo = (1, (rank, cards[0], cards[1], cards[2]))
                            return
                        row.combo = (1, (rank, cards[1], cards[2]))
                        row.max_combo = (3, (rank,))
                        return
                    if rank >= cards[1]:
                        if rank > cards[1]:
                            row.combo = (0, (cards[0], rank, cards[1], cards[2]))
                            row.max_combo = (1, (cards[0], rank, cards[1], cards[2]))
                            return
                        row.combo = (1, (rank, cards[0], cards[2]))
                        row.max_combo = (3, (rank,))
                        return
                    if rank >= cards[2]:
                        if rank > cards[2]:
                            row.combo = (0, (cards[0], cards[1], rank, cards[2]))
                            row.max_combo = (1, (cards[0], cards[1], rank, cards[2]))
                            return
                        row.combo = (1, (rank, cards[0], cards[1]))
                        row.max_combo = (3, (rank,))
                        return
                    row.combo = (0, (cards[0], cards[1], cards[2], rank))
                    row.max_combo = (1, (cards[0], cards[1], cards[2], rank))
                    return 
                case 3:
                    if rank != cards[0]:
                        row.combo = (3, (cards[0], rank))
                        row.max_combo = (7, (cards[0]))
                        return
                    row.combo = (7, (rank,))
                    row.max_combo = row.combo
                    row.points = 20 if row.row == 1 else 10
                    return
        case 2:
            if kind == 1:
                if rank != cards[0]:
                    row.combo = (1, (cards[0], rank))
                    row.max_combo = (7, (cards[0],))
                    return
                row.combo = (3, (rank,))
                row.max_combo = (7, (rank,))
                return
            if rank >= cards[0]:
                if rank > cards[0]:
                    row.combo = (0, (rank, cards[0], cards[1]))
                    row.max_combo = (3, (rank,))
                    return
                row.combo = (1, (rank, cards[1]))
                row.max_combo = (7, (rank,))
                return
            if rank >= cards[1]:
                if rank > cards[1]:
                    row.combo = (0, (cards[0], rank, cards[1]))
                    row.max_combo = (3, (cards[0],))
                    return
                row.combo = (1, (rank, cards[0]))
                row.max_combo = (7, (rank,))
                return
            row.combo = (0, (cards[0], cards[1], rank))
            row.max_combo = (3, (cards[0],))
            return

def add_card_f(row: Row, card: int):
    match row.cells:
        case 0:
            combo = c4_5(row.combo, card // 4)
            if combo[0]:
                row.combo = combo
                row.max_combo = row.combo
                return
            if row.flush == card % 4:
                row.combo = (5, combo[1])
                row.max_combo = row.combo
                row.points = 4 if row.row == 2 else 8
                return
            row.combo = combo
            row.max_combo = row.combo
            return
        case 1:
            combo = c3_4(row.combo, card // 4)
            row.combo = combo
            if combo[0]:
                row.add_card = add_card_classic
                row.max_combo = (3, (combo[1][0],))
                return
            if row.flush != card % 4:
            #if row.flush == card % 4:
            #    row.max_combo = (5, (12, 12))
            #    return
                row.add_card = add_card_classic
                row.max_combo = (1, combo[1])
            return
        case 2:
            combo = c2_3(row.combo, card // 4)
            row.combo = combo
            if combo[0]:
                row.add_card = add_card_classic
                row.max_combo = (7, (combo[1][0],))
                return
            if row.flush != card % 4:
                row.add_card = add_card_classic
                row.max_combo = (3, (combo[1][0],))
def add_card_s(row: Row, card: int):
    match row.cells:
        case 0:
            combo = c4_5(row.combo, card // 4)
            if combo[0]:
                row.combo = combo
                row.max_combo = row.combo
                return
            if combo[1][0] - combo[1][-1] ==4:
                row.combo = (4, (combo[1][0],))
                row.max_combo = row.combo
                row.points = 2 if row.row == 2 else 4
                return
            if combo[1][0] == 12 and combo[1][1] == 3:
                row.combo = (4, (3,))
                row.max_combo = row.combo
                row.points = 2 if row.row == 2 else 4
                return
            row.combo = combo
            row.max_combo = row.combo
            return
        case 1:
            combo = c3_4(row.combo, card // 4)
            row.combo = combo
            if combo[0]:
                row.add_card = add_card_classic
                row.max_combo = (3, (combo[1][0],))
                return
            if combo[1][0] - combo[1][-1] <=4:
                row.max_combo = (4, (min(12, combo[1][-1] + 4),))
                return
            if combo[1][0] == 12 and combo[1][1] <= 3:
                row.max_combo = (4, (3,))
                return
            row.add_card = add_card_classic
            row.max_combo = (1, combo[1])
            return
        case 2:
            combo = c2_3(row.combo, card // 4)
            row.combo = combo
            if combo[0]:
                row.add_card = add_card_classic
                row.max_combo = (7, (combo[1][0],))
                return
            if combo[1][0] - combo[1][-1] <=4:
                row.max_combo = (4, (min(12, combo[1][-1] + 4),))
                return
            if combo[1][0] == 12 and combo[1][1] <= 3:
                row.max_combo = (4, (3,))
                return
            row.add_card = add_card_classic
            row.max_combo = (3, (combo[1][0],))

def add_card_fs(row: Row, card):
    match row.cells:
        case 0:
            combo = c4_5(row.combo, card // 4)
            if combo[0]:
                row.combo = combo
                row.max_combo = row.combo
                return
            if combo[1][0] - combo[1][-1] == 4:
                if row.flush == card % 4:
                    row.combo = (8, (combo[1][0],))
                    row.max_combo = row.combo
                    if row.combo[1][0] < 12:
                        row.points = 15 if row.row == 2 else 30
                        return
                    row.points = 25 if row.row == 2 else 50
                    return
                row.combo = (4, (combo[1][0],))
                row.max_combo = row.combo
                row.points = 2 if row.row == 2 else 4
                return
            if combo[1][0] == 12 and combo[1][1] == 3:
                if row.flush == card % 4:
                    row.combo = (8, (3,))
                    row.max_combo = row.combo
                    row.points = 15 if row.row == 2 else 30
                    return
                row.combo = (4, (3,))
                row.max_combo = row.combo
                row.points = 2 if row.row == 2 else 4
                return
            if row.flush == card % 4:
                row.combo = (5, combo[1])
                row.max_combo = row.combo
                row.points = 4 if row.row == 2 else 8
                return
            row.combo = combo
            row.max_combo = row.combo
            return
        case 1:
            combo = c3_4(row.combo, card // 4)
            row.combo = combo
            if combo[0]:
                row.add_card = add_card_classic
                row.max_combo = (3, (combo[1][0],))
                return
            if combo[1][0] - combo[1][-1] <= 4:
                if row.flush == card % 4:
                    row.max_combo = (8, (min(12, combo[1][-1] + 4),))
                    return
                row.max_combo = (4, (min(12, combo[1][-1] + 4),))
                row.add_card = add_card_s
                return
            if combo[1][0] == 12 and combo[1][1] <=3:
                if row.flush == card % 4:
                    row.max_combo = (8, (3,))
                    return
                row.max_combo = (4, (3,))
                row.add_card = add_card_s
                return
            if row.flush == card % 4:
                row.max_combo = (5, (12, 12))
                row.add_card = add_card_f
                return
            row.max_combo = (1, combo[1])
            row.add_card = add_card_classic
            return
        case 2:
            combo = c2_3(row.combo, card // 4)
            row.combo = combo
            if combo[0]:
                row.add_card = add_card_classic
                row.max_combo = (7, (combo[1][0],))
                return
            if combo[1][0] - combo[1][-1] <= 4:
                if row.flush == card % 4:
                    row.max_combo = (8, (min(12, combo[1][-1] + 4),))
                    return
                row.max_combo = (4, (min(12, combo[1][-1] + 4),))
                row.add_card = add_card_s
                return
            if combo[1][0] == 12 and combo[1][1] <=3:
                if row.flush == card % 4:
                    row.max_combo = (8, (3,))
                    return
                row.max_combo = (4, (3,))
                row.add_card = add_card_s
                return
            if row.flush == card % 4:
                row.max_combo = (5, (12, 12))
                row.add_card = add_card_f
                return
            row.max_combo = (3, (combo[1][0],))
            row.add_card = add_card_classic
            return
        case 3:
            rank = card // 4
            if rank == row.combo[1][0]:
                row.combo = (1, row.combo[1])
                row.max_combo = (7, row.combo[1])
                row.add_card = add_card_classic
                return
            combo = (0, (row.combo[1][0], rank)) if row.combo[1][0] > rank else (0, (rank, row.combo[1][0]))
            row.combo = combo
            if combo[1][0] - combo[1][-1] <= 4:
                if row.flush == card % 4:
                    row.max_combo = (8, (min(12, combo[1][-1] + 4),))
                    return
                row.max_combo = (7, (combo[1][0],))
                row.add_card = add_card_s
                return
            if combo[1][0] == 12 and combo[1][1] <=3:
                if row.flush == card % 4:
                    row.max_combo = (8, (3,))
                    return
                row.max_combo = (7, (combo[1][0],))
                row.add_card = add_card_s
                return
            if row.flush == card % 4:
                row.max_combo = (7, (combo[1][0],))
                row.add_card = add_card_f
                return
            row.max_combo = (7, (combo[1][0],))
            row.add_card = add_card_classic
            return
        case 4:
            row.flush = card % 4
            row.combo = (0, (card // 4,))
            row.max_combo = (8, (min(12, row.combo[1][0] + 4)))
            return

            


def final_pair3(row: Row, pair: list):
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    if rank0 == rank1:
        if rank0 == row.combo[1][0]: return (3, [rank0])
        return (1, [rank0, row.combo[1][0]])
    if rank0 == row.combo[1][0]: return (1, [rank0, rank1])
    if rank1 == row.combo[1][0]: return (1, [rank1, rank0])
    return (0, sorted([rank0, rank1, row.combo[1][0]], reverse=True))
def final_pair5(row: Row, pair: list):
    pass
def final_fs1(row: Row, card: int):
    suit = card % 4
    combo = rank5(row, card)
    s = is_straight(combo[1])
    if s > 0 and row.flush == suit:
        if s < 12: return 30 if hand.rows[2].max_combo >= (8, [s]) else penalty
        return 50 if hand.rows[2].max_combo == (9, [12]) else penalty
    if row.flush == suit: return 8 if hand.rows[2].max_combo >= (5, combo[1]) else penalty
    if s > 0:
        return 4 if hand.rows[2].max_combo >= (4, [s]) else penalty
    return 0 if hand.rows[2].combo >= combo else penalty
def final_fs2(row: Row, card: int):
    suit = card % 4
    combo = rank5(row, card)
    s = is_straight(combo[1])
    if s > 0 and row.flush == suit:
        if s < 12: return 15
        return 25
    if row.flush == suit: return 4
    if s > 0:
        return 2
    return 0
def c2_3(combo: tuple, rank: int) -> tuple:
    match combo[0]:
        case 0:
            if rank >= combo[1][0]:
                return (1, combo[1]) if rank == combo[1][0] else (0, (rank, combo[1][0], combo[1][1]))
            if rank >= combo[1][1]:
                return (1, (rank, combo[1][0])) if rank == combo[1][1] else (0, (combo[1][0], rank, combo[1][1]))
            return (0, (combo[1][0], combo[1][1], rank))    
        case 1:
            if rank == combo[1][0]: return (3, combo[1]) 
            return (1, (combo[1][0], rank))
def c1_3(combo: tuple, pair: list) -> tuple:
    if pair[0] == pair[1]:
        if pair[0] == combo[1][0]: return (3, combo[1])
        else: return (1, [pair[0], combo[1][0]])
    if pair[0] == combo[1][0]: return (1, [pair[0], pair[1]])
    if pair[1] == combo[1][0]: return (1, [pair[1], pair[0]])
    return (0, sorted([pair[0], pair[1], combo[1][0]], reverse=True))
def c1_2(combo: tuple, rank: int) -> tuple:
    if combo[1][0] == rank: return(1, combo[1])
    return (0, [combo[1][0], rank]) if combo[1][0] > rank else (0, [rank, combo[1][0]])
def c3_4(combo: tuple, rank: int) -> tuple:
    match combo[0]:
        case 1:
            if rank == combo[1][0]:
                return (3, combo[1])
            if rank == combo[1][1]:
                return (2, combo[1]) if combo[1][0] > rank else (2, (rank, combo[1][0]))
            return (1, (combo[1][0], combo[1][1], rank)) if combo[1][1] > rank else (1, (combo[1][0], rank, combo[1][1]))
        case 0:
            if rank >= combo[1][0]:
                return (1, combo[1]) if rank == combo[1][0] else (0, (rank, combo[1][0], combo[1][1], combo[1][2]))
            if rank >= combo[1][1]:
                return (1, (rank, combo[1][0], combo[1][2])) if rank == combo[1][1] else (0, (combo[1][0], rank, combo[1][1], combo[1][2]))
            if rank >= combo[1][2]:
                return (1, (rank, combo[1][0], combo[1][1])) if rank == combo[1][2] else (0, (combo[1][0], combo[1][1], rank, combo[1][2]))
            return (0, (combo[1][0], combo[1][1], combo[1][2], rank))
        case 3:
            if rank == combo[1][0]: return (7, combo[1])
            return (3, (combo[1][0], rank))
def c4_5(combo: tuple, rank: int) -> tuple:
    match combo[0]:
        case 1:
            if rank >= combo[1][0]:
                return (3, (combo[1][0],)) if rank == combo[1][0] else (1, (combo[1][0], rank, combo[1][1], combo[1][2]))
            if rank >= combo[1][1]:
                if rank > combo[1][1]: return (1, (combo[1][0], rank, combo[1][1], combo[1][2]))
                return (2, combo[1]) if combo[1][0] > rank else (2, (rank, combo[1][0], combo[1][2]))
            if rank >= combo[1][2]:
                if rank > combo[1][2]: return (1, (combo[1][0], combo[1][1], rank, combo[1][2]))
                return (2, (combo[1][0], rank, combo[1][1])) if combo[1][0] > rank else (2, (rank, combo[1][0], combo[1][1]))
            return (1, (combo[1][0], combo[1][1], combo[1][2], rank))
        case 2:
            if rank == combo[1][0]:
                return (6, combo[1])
            if rank == combo[1][1]:
                return (6, (combo[1][1], combo[1][0]))
            return (2, (combo[1][0], combo[1][1], rank))
        case 0:
            if rank >= combo[1][0]:
                return (1, combo[1]) if rank == combo[1][0] else (0, (rank, combo[1][0], combo[1][1], combo[1][2], combo[1][3]))
            if rank >= combo[1][1]:
                return (1, (rank, combo[1][0], combo[1][2], combo[1][3])) if rank == combo[1][1] else (0, (combo[1][0], rank, combo[1][1], combo[1][2], combo[1][3]))
            if rank >= combo[1][2]:
                return (1, (rank, combo[1][0], combo[1][1], combo[1][3])) if rank == combo[1][2] else (0, (combo[1][0], combo[1][1], rank, combo[1][2], combo[1][3]))
            if rank >= combo[1][3]:
                return (1, (rank, combo[1][0], combo[1][1], combo[1][2])) if rank == combo[1][3] else (0, (combo[1][0], combo[1][1], combo[1][2], rank, combo[1][3]))
            return (0, (combo[1][0], combo[1][1], combo[1][2], combo[1][3], rank))
        case 3:
            if rank == combo[1][0]: return (7, combo[1])
            if rank == combo[1][1]: return (6, combo[1])
            return (3, (combo[1][0],))
def c3_6(c: tuple, d: tuple) -> tuple:
    match (d[0] == d[1]) + (d[1] == d[2]):
        case 0:
            if d[0] == c[0]:
                if d[1] == c[1] or d[2] == c[1]: return (2, (c[0], c[1], c[2]))
                if d[1] == c[2] or d[2] == c[2]: return (2, (c[0], c[2], c[1]))
                if d[1] > c[1]: return (1, (c[0], d[1], c[1], c[2]))
                if d[1] > c[2]: return (1, (c[0], c[1], d[1], c[2]))
                return (1, (c[0], c[1], c[2], d[1]))
            if d[0] == c[1]:
                if d[1] == c[2] or d[2] == c[2]: return (2, (c[1], c[2], c[0]))
                return (1, (c[1], c[0], d[1], c[2])) if d[1] > c[2] else (1, (c[1], c[0], c[2], d[1]))
            if d[0] == c[2]: return (1, (c[2], c[0], c[1], d[1]))
            if d[1] == c[0]:
                if d[2] == c[1]: return (2, (c[0], c[1], c[2]))
                if d[2] == c[2]: return (2, (c[0], c[2], c[1]))
                return (1, (c[0], d[0], c[1], c[2]))
            if d[1] == c[1]:
                if d[2] == c[2]: return (2, (c[1], c[2], c[0]))
                return (1, (c[1], d[0], c[0], c[2])) if d[0] > c[0] else (1, (c[1], c[0], d[0], c[2]))
            if d[1] == c[2]:
                if d[0] > c[0]: return (1, (c[2], d[0], c[0], c[1]))
                return (1, (c[2], c[0], d[0], c[1])) if d[0] > c[1] else (1, (c[2], c[0], c[1], d[0]))
            if d[2] == c[0]: return (1, (c[0], d[0], c[1], c[2]))
            if d[2] == c[1]: 
                return (1, (c[1], d[0], c[0], c[2])) if d[0] > c[0] else (1, (c[1], c[0], d[0], c[2]))
            if d[2] == c[2]:
                if d[0] > c[0]: return (1, (c[2], d[0], c[0], c[1]))
                return (1, (c[2], c[0], d[0], c[1])) if d[0] > c[1] else (1, (c[2], c[0], c[1], d[0]))
            if d[0] > c[0]:
                if d[1] > c[0]: return (0, (d[0], d[1], c[0], c[1], c[2]))
                if d[1] > c[1]: return (0, (d[0], c[0], d[1], c[1], c[2]))
                if d[1] > c[2]: return (0, (d[0], c[0], c[1], d[1], c[2]))
                return (0, (d[0], c[0], c[1], c[2], d[1]))
            if d[0] > c[1]:
                if d[1] > c[1]: return (0, (c[0], d[0], d[1], c[1], c[2]))
                return (0, (c[0], d[0], c[1], d[1], c[2])) if d[1] > c[2] else (0, (c[0], d[0], c[1], c[2], d[1]))
            if d[0] > c[2]:
                return (0, (c[0], c[1], d[0], d[1], c[2])) if d[1] > c[2] else (0, (c[0], c[1], d[0], c[2], d[1]))
            return (0, (c[0], c[1], c[2], d[0], d[1])) 
        case 1:
            if d[1] == c[0] or d[1] == c[1] or d[1] == c[2]: return (3, (d[1],))
            d0 = d[2] if d[2] != d[1] else d[0]
            if d0 < d[1]: return (1, (d[1], c[0], c[1], c[2]))
            if d0 == c[0]:
                    if d[1] > c[1]: return (1, (c[0], d[1], c[1], c[2]))
                    if d[1] > c[2]: return (1, (c[0], c[1], d[1], c[2]))
                    return (1, (c[0], c[1], c[2], d[1]))
            if d0 == c[1]: return (1, (c[1], c[0], d[1], c[2])) if d[1] > c[2] else (1, (c[1], c[0], c[2], d[1]))
            if d0 == c[2]: return (1, (c[2], c[0], c[1], d[1]))
            return (1, (d[1], c[0], c[1], c[2]))
        case 2:
            if d[1] == c[0] or d[1] == c[1] or d[1] == c[2]: return (3, (d[1],))
            return (1, (d[1], c[0], c[1], c[2]))
LUT3_6 = lut3_6()
def final_22(pair: list):
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    combo = c4_5(c3_4(hand.rows[2].combo, rank0), rank1)
    if hand.rows[2].add_card is add_card_classic:
        if combo >= hand.rows[1].combo:
            if combo[0] == 6: return 6
            elif combo[0] == 7: return 10
            else: return 0
        return penalty
    if hand.rows[2].add_card is add_card_f:
        if pair[0] % 4 == hand.rows[2].flush and pair[1] % 4 == hand.rows[2].flush:
            return 4 if (5, combo[1]) >= hand.rows[1].combo else penalty
        return 0 if combo >= hand.rows[1].combo else penalty
    if hand.rows[2].add_card is add_card_s:
        if combo[0] == 0:
            s = is_straight(combo[1])
            if s: return 2 if (4, [s]) >= hand.rows[1].combo else penalty
        return 0 if combo >= hand.rows[1].combo else penalty
    if hand.rows[2].add_card is add_card_fs:
        if pair[0] % 4 == hand.rows[2].flush and pair[1] % 4 == hand.rows[2].flush:
            s = is_straight(combo[1])
            if s == 12: return 25
            if s > 0: return 15 if (8, [s]) >= hand.rows[1].combo else penalty
            return 4 if (5, combo[1]) >= hand.rows[1].combo else penalty
        if combo[0] == 0:
            s = is_straight(combo[1])
            if s: return 2 if (4, [s]) >= hand.rows[1].combo else penalty
        return 0 if combo >= hand.rows[1].combo else penalty
def final_11(pair: list):
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    combo = c4_5(c3_4(hand.rows[1].combo, rank0), rank1)
    if hand.rows[1].add_card is add_card5:
        if hand.rows[2].combo >= combo and combo >= hand.rows[0].combo:
            if combo[0] < 3: return 0
            if combo[0] == 3: return 2
            if combo[0] == 6: return 12
            if combo[0] == 7: return 20
        return penalty
    if hand.rows[1].add_card is add_card_f:
        if pair[0] % 4 == hand.rows[1].flush and pair[1] % 4 == hand.rows[1].flush:
            return 8 if (5, combo[1]) <= hand.rows[2].combo else penalty
        return 0 if combo <= hand.rows[2].combo and combo >= hand.rows[0].combo else penalty
    if hand.rows[1].add_card is add_card_s:
        if combo[0] == 0:
            s = is_straight(combo[1])
            if s: return 4 if (4, [s]) <= hand.rows[2].combo else penalty
        return 0 if combo <= hand.rows[2].combo and combo >= hand.rows[0].combo else penalty
    if hand.rows[1].add_card is add_card_fs:
        if pair[0] % 4 == hand.rows[1].flush and pair[1] % 4 == hand.rows[1].flush:
            s = is_straight(combo[1])
            if s == 12: return 50 if hand.rows[2].combo == (8, [12]) else penalty
            if s > 0: return 30 if (8, [s]) <= hand.rows[2].combo else penalty
            return 8 if (5, combo[1]) <= hand.rows[2].combo else penalty
        if combo[0] == 0:
            s = is_straight(combo[1])
            if s: return 4 if (4, [s]) <= hand.rows[2].combo else penalty
        return 0 if combo >= hand.rows[0].combo and combo <= hand.rows[2].combo else penalty       
def final_00(pair):
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    combo = c1_3(hand.rows[0].combo, [rank0, rank1])
    if combo <= hand.rows[1].combo:
        if combo < (1, [4]): return 0
        if combo < (1, [10]): return combo[1][0] - 3
        if combo[0] == 1: return combo[1][0] - 3 + premium
        return combo[1][0] + 10 + premium
    return penalty
def final_12(card, i):
    rank = card // 4
    combo = c4_5(hand.rows[i].combo, rank)
    if hand.rows[i].add_card is add_card5: return combo
    if hand.rows[i].add_card is add_card_f: return (5, combo[1]) if hand.rows[i].flush == card % 4 else combo
    if hand.rows[i].add_card is add_card_s:
        if not combo[0]:
            s = is_straight(combo[1])
            return (4, [s]) if s else combo
    if hand.rows[i].add_card is add_card_fs:
        if card % 4 == hand.rows[i].flush:
            s = is_straight(combo[1])
            if s: return (8, [s])
            else: return (5, combo[1])
        if not combo[0]:
            s = is_straight(combo[1])
            return (4, [s]) if s else combo
        return combo

def s4p(f, h: Hand) -> tuple:
    p = 0
    max_points = penalty
    pairs = list(combinations(f, 2))
    if h.rows[0].cells == 2:
        for pair in pairs:
            points = final_00(pair)
            if points > max_points:
                max_points = points
                p = ((pair[0], 0), (pair[1], 0))
        return p
    if h.rows[1].cells == 2:
        for pair in pairs:
            points = final_11(pair)
            if points > max_points:
                max_points = points
                p = ((pair[0], 1), (pair[1], 1))
        return p
    if h.rows[2].cells == 2:
        for pair in pairs:
            points = final_22(pair)
            if points > max_points:
                max_points = points
                p = ((pair[0], 2), (pair[1], 2))
        return p

    if h.rows[0].cells and h.rows[1].cells:
        for pair in pairs:
            combo0 = c2_3(h.rows[0].combo, pair[0] // 4)
            combo1 = final_12(pair[1], 1)
            if combo0 <= combo1 and combo1 <= h.rows[2].combo:
                points = get_points(combo0, 0) + get_points(combo1, 1)
                if points > max_points:
                    max_points = points
                    p = ((pair[0], 0), (pair[1], 1))
            combo0 = c2_3(h.rows[0].combo, pair[1])
            combo1 = final_12(pair[0], 1) // 4
            if combo0 <= combo1 and combo1 <= h.rows[2].combo:
                points = get_points(combo0, 0) + get_points(combo1, 1)
                if points > max_points:
                    max_points = points
                    p = ((pair[1], 0), (pair[0], 1))
        return p
    if h.rows[0].cells and h.rows[2].cells:
        for pair in pairs:
            combo0 = c2_3(h.rows[0].combo, pair[0] // 4)
            combo2 = final_12(pair[1], 2)
            if combo0 <= h.rows[1].combo and combo2 >= h.rows[1].combo:
                points = get_points(combo0, 0) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
                    p = ((pair[0], 0), (pair[1], 2))
            combo0 = c2_3(h.rows[0].combo, pair[1] // 4)
            combo2 = final_12(pair[0], 2)
            if combo0 <= h.rows[1].combo and combo2 >= h.rows[1].combo:
                points = get_points(combo0, 0) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
                    p = ((pair[1], 0), (pair[0], 2))
        return p
    if h.rows[1].cells and h.rows[2].cells:
        for pair in pairs:
            combo1 = final_12(pair[0], 1)
            combo2 = final_12(pair[1], 2)
            if combo1 >= h.rows[0].combo and combo2 >= combo1:
                points = get_points(combo1, 1) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
                    p = ((pair[0], 1), (pair[1], 2))
            combo1 = final_12(pair[1], 1)
            combo2 = final_12(pair[0], 2)
            if combo1 >= h.rows[0].combo and combo2 >= combo1:
                points = get_points(combo1, 1) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
                    p = ((pair[1], 1), (pair[0], 2))
        return p

def s4(f, h: Hand):
    max_points = penalty
    pairs = list(combinations(f, 2))
    if h.rows[0].cells == 2:
        for pair in pairs:
            points = final_00(pair)
            if points > max_points:
                max_points = points
        return max_points + h.rows[1].points + h.rows[2].points
    if h.rows[1].cells == 2:
        for pair in pairs:
            points = final_11(pair)
            if points > max_points:
                max_points = points
        return max_points + h.rows[0].points + h.rows[2].points
    if h.rows[2].cells == 2:
        for pair in pairs:
            points = final_22(pair)
            if points > max_points:
                max_points = points
        return max_points + h.rows[0].points + h.rows[1].points

    if h.rows[0].cells and h.rows[1].cells:
        for pair in pairs:
            combo0 = c2_3(h.rows[0].combo, pair[0])
            combo1 = final_12(pair[1], 1)
            if combo0 <= combo1 and combo1 <= h.rows[2].combo:
                points = get_points(combo0, 0) + get_points(combo1, 1)
                if points > max_points:
                    max_points = points
            combo0 = c2_3(h.rows[0].combo, pair[1])
            combo1 = final_12(pair[0], 1)
            if combo0 <= combo1 and combo1 <= h.rows[2].combo:
                points = get_points(combo0, 0) + get_points(combo1, 1)
                if points > max_points:
                    max_points = points
        return max_points + h.rows[2].points
    if h.rows[0].cells and h.rows[2].cells:
        for pair in pairs:
            combo0 = c2_3(h.rows[0].combo, pair[0])
            combo2 = final_12(pair[1], 2)
            if combo0 <= h.rows[1].combo and combo2 >= h.rows[1].combo:
                points = get_points(combo0, 0) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
            combo0 = c2_3(h.rows[0].combo, pair[1])
            combo2 = final_12(pair[0], 2)
            if combo0 <= h.rows[1].combo and combo2 >= h.rows[1].combo:
                points = get_points(combo0, 0) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
        return max_points + h.rows[1].points
    if h.rows[1].cells and h.rows[2].cells:
        for pair in pairs:
            combo1 = final_12(pair[0], 1)
            combo2 = final_12(pair[1], 2)
            if combo1 >= h.rows[0].combo and combo2 >= combo1:
                points = get_points(combo1, 1) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
            combo1 = final_12(pair[1], 1)
            combo2 = final_12(pair[0], 2)
            if combo1 >= h.rows[0].combo and combo2 >= combo1:
                points = get_points(combo1, 1) + get_points(combo2, 2)
                if points > max_points:
                    max_points = points
        return max_points + h.rows[0].points
def s00(h: Hand, d: list):
    rank = h.rows[0].combo[1][0]
    r = (d[0] // 4, d[1] // 4, d[2] // 4)
    pairs = ((r[0], r[1]), (r[0], r[2]), (r[1], r[2]))
    max_points = penalty
    for pair in pairs:
        if pair[0] == rank:
            if pair[1] == rank:
                combo = (3, (rank,))
                points = rank + 10 + penalty
            else:
                combo = (1, (rank, pair[1]))
                points = HIGH_ROW_PAIR[rank]
        elif pair[1] == rank:
            combo = (1, (rank, pair[0]))
            points = HIGH_ROW_PAIR[rank]
        elif pair[0] == pair[1]:
            combo = (1, (pair[0], rank))
            points = HIGH_ROW_PAIR[pair[0]]
        else:
            points = 0
            if rank > pair[0] and rank > pair[1]:
                combo = (0, (rank, pair[0], pair[1])) if pair[0] > pair[1] else (0, (rank, pair[1], pair[0]))
            elif pair[0] > rank and pair[0] > pair[1]:
                combo = (0, (pair[0], rank, pair[1])) if rank > pair[1] else (0, (pair[0], pair[1], rank))
            else: combo = (0, (pair[1], rank, pair[0])) if rank > pair[0] else (0, (pair[1], pair[0], rank))
        if combo <= h.rows[1].combo and points > max_points: max_points = points
    return h.rows[1].points + h.rows[2].points + max_points if max_points > penalty else penalty
def s22_(h: Hand, d: list):
    combo1, row2 = h.rows[1].combo, h.rows[2]
    r0, r1, r2 = d[0] // 4, d[1] // 4, d[2] // 4
    if row2.combo[0] == 0: c0, c1, c2 = row2.combo[1]
    elif row2.combo[0] == 1:
        p, k = row2.combo[1]
        c0, c1, c2 = p, p, k if p > k else k, p, p
    else: c0, c1, c2 = row2.combo[1][0], row2.combo[1][0], row2.combo[1][0]
    
    if row2.add_card is add_card_f:
        if (d[0] & 3 == row2.flush) + (d[1] & 3 == row2.flush) + (d[2] & 3 == row2.flush) >= 2:
            if combo1[0] < 5: return 4
            c10, c11, c12, c13, c14 = combo1[1]
            mask1 = (1 << c10) | (1 << c11) | (1 << c12) | (1 << c13) | (1 << c14)
            mask2 = (1 << c0) | (1 << c1) | (1 << c2)
            if d[0] & 3 == row2.flush:
                if d[1] & 3 == row2.flush:
                    mask2 = mask2 | (1 << r0) | (1 << r1)
                    return 4 if mask2 >= mask1 else penalty
                mask2 = mask2 | (1 << r0) | (1 << r2)
                return 4 if mask2 >= mask1 else penalty
            mask2 = mask2 | (1 << r1) | (1 << r2)
            return 4 if mask2 >= mask1 else penalty
        return 0 if LUT3_5[C_IND[(c0, c1, c2)]][C_IND[(r0, r1, r2)]] >= combo1 else penalty
    if row2.add_card is add_card_classic:
        combo2 = LUT3_5[C_IND[(c0, c1, c2)]][C_IND[(r0, r1, r2)]]
        if combo2 < combo1: return penalty
        if combo2[0] < 4: return 0
        if combo2[0] == 6: return 6
        if combo2[0] == 7: return 10

    if h.rows[2].add_card is add_card_s:
        s = row2.max_combo[1][0]
        mask = MASK[c0] | MASK[c1] | MASK[c2] | MASK[r0] | MASK[r1] | MASK[r2]
        if MASK & MASK5[s-3] == MASK5[s-3]: return 2 if (4, (s,)) >= combo1 else penalty
        if s > 3 and MASK & MASK5[s-4] == MASK5[s-4]: return 2 if (4, (s-1,)) >= combo1 else penalty
        if s > 4 and MASK & MASK5[s-5] == MASK5[s-5]: return 2 if (4, (s-2,)) >= combo1 else penalty
        return 0 if LUT3_5[C_IND[(c0, c1, c2)]][C_IND[(r0, r1, r2)]] >= combo1 else penalty 

    if h.rows[2].add_card is add_card_fs:
        f = (d[0] & 3 == row2.flush) + (d[1] & 3 == row2.flush) + (d[2] & 3 == row2.flush)
        s = row2.max_combo[1][0]
        if f < 2:
            mask = MASK[c0] | MASK[c1] | MASK[c2] | MASK[r0] | MASK[r1] | MASK[r2]
            if mask & MASK5[s-3] == MASK5[s-3]: return 2 if (4, (s,)) >= combo1 else penalty
            if s > 3 and mask & MASK5[s-4] == MASK5[s-4]: return 2 if (4, (s-1,)) >= combo1 else penalty
            if s > 4 and mask & MASK5[s-5] == MASK5[s-5]: return 2 if (4, (s-2,)) >= combo1 else penalty
            return 0 if LUT3_5[C_IND[(c0, c1, c2)]][C_IND[(r0, r1, r2)]] >= combo1 else penalty
        if f == 3:
            mask2 = MASK[c0] | MASK[c1] | MASK[c2] | MASK[r0] | MASK[r1]
            mask = mask2 | MASK[r2]
        else:
            if (d[0] & 3 == row2.flush) and (d[2] & 3 == row2.flush): r0, r1 = r0, r2
            elif (d[1] & 3 == row2.flush) and (d[2] & 3 == row2.flush): r0, r1 = r1, r2
            mask2 = MASK[c0] | MASK[c1] | MASK[c2] | MASK[r0] | MASK[r1]
            mask = mask2

        if mask & MASK5[s-3] == MASK5[s-3]:
            if s == 12: return 25
            return 15 if (8, (s,)) >= combo1 else penalty
        if s > 3 and mask & MASK5[s-4] == MASK5[s-4]: return 15 if (8, (s-1,)) >= combo1 else penalty
        if s > 4 and mask & MASK5[s-5] == MASK5[s-5]: return 15 if (8, (s-2,)) >= combo1 else penalty
        if combo1[0] < 5: return 4
        if combo1[0] > 5: return penalty
        c10, c11, c12, c13, c14 = combo1[1]
        mask1 = (1 << c10) | (1 << c11) | (1 << c12) | (1 << c13) | (1 << c14)
        return 4 if mask2 >= mask1 else penalty

def c3_5_(c: tuple, d: tuple) -> tuple:
    if c[0] == c[1] == c[2]:
        if d[0] == d[1] == d[2]:
            return (6, (c[0], d[0]))
        if d[0] == d[1]:
            return (6, (c[0], d[0])) if d[2] != c[0] else (7, (c[0],))
        if d[1] == d[2]:
            return (6, (c[0], d[1])) if d[0] != c[0] else (7, (c[0],))
        else: return (7, (c[0],)) if c[0] == d[0] or c[0] == d[1] or c[0] == d[2] else (3, (c[0],))
    if c[0] == c[1]:
        if d[0] == d[1] == d[2]:
            if c[2] == d[0]: return (6, (c[2], c[0]))
            return (2, (c[0], d[0], c[2])) if c[0] > d[0] else (2, (d[0], c[0], c[2])) 
        if d[0] == d[1]:
            if c[0] == d[0]: return (7, (c[0],))
            if c[2] == d[0]: return (6, (c[2], c[0]))
            if c[0] == d[2]: return (3, (c[0],))
            return (2, (c[0], d[0], c[2])) if c[0] > d[0] else (2, (d[0], c[0], c[2]))
        if d[1] == d[2]:
            if c[0] == d[1]: return (7, (c[0],))
            if c[2] == d[1]: return (6, (c[2], c[0]))
            if c[0] == d[0]: return (3, (c[0],))
            return (2, (c[0], d[1], c[2])) if c[0] > d[1] else (2, (d[1], c[0], c[2]))
        else:
            if (c[0] == d[0] or c[0] == d[1] or c[0] == d[2]) and (c[2] == d[0] or c[2] == d[1] or c[2] == d[2]): return (6, (c[0], c[2]))
            if (c[0] == d[0] or c[0] == d[1] or c[0] == d[2]): return (3, (c[0],))
            if (c[2] == d[0]): return (2, (c[0], c[2], d[1]))
            if (c[2] == d[1]): return (2, (c[0], c[2], d[0]))
            if (c[2] == d[2]): return (2, (c[0], c[2], d[0]))
    if c[1] == c[2]:
        if d[0] == d[1] == d[2]:
            if c[0] == d[0]: return (6, (c[0], c[1]))
            return (2, (c[1], d[0], c[0])) if c[1] > d[0] else (2, (d[0], c[1], c[0])) 
        if d[0] == d[1]:
            if c[1] == d[0]: return (7, (c[1],))
            if c[0] == d[0]: return (6, (c[0], c[1]))
            if c[1] == d[2]: return (3, (c[1],))
            return (2, (c[1], d[0], c[0])) if c[1] > d[0] else (2, (d[0], c[1], c[0]))
        if d[1] == d[2]:
            if c[1] == d[1]: return (7, (c[1],))
            if c[0] == d[1]: return (6, (c[0], c[1]))
            if c[1] == d[0]: return (3, (c[1],))
            return (2, (c[1], d[1], c[0])) if c[1] > d[1] else (2, (d[1], c[1], c[0]))
        else:
            if (c[1] == d[0] or c[1] == d[1] or c[1] == d[2]) and (c[0] == d[0] or c[0] == d[1] or c[0] == d[2]): return (6, (c[1], c[0]))
            if (c[1] == d[0] or c[1] == d[1] or c[1] == d[2]): return (3, (c[1],))
            if (c[0] == d[0]): return (2, (c[0], c[1], d[1]))
            if (c[0] == d[1]): return (2, (c[0], c[1], d[0]))
            if (c[0] == d[2]): return (2, (c[0], c[1], d[0]))
    else:
        if d[0] == d[1] == d[2]:
            if c[0] == d[0] or c[1] == d[0] or c[2] == d[0]: return (3, (d[0],))
            return (1, (d[0], c[0], c[1], c[2]))
        if d[0] == d[1]:
            if c[0] == d[0] or c[1] == d[0] or c[2] == d[0]: return (3, (d[0],))
            return (1, (d[0], c[0], c[1], c[2]))
        if d[1] == d[2]:
            if c[0] == d[1] or c[1] == d[1] or c[2] == d[1]: return (3, (d[1],))
            return (1, (d[1], c[0], c[1], c[2]))
        else:
            if (c[0] in d) and (c[1] in d): return (2, (c[0], c[1], c[2]))
            if (c[0] in d) and (c[2] in d): return (2, (c[0], c[2], c[1]))
            if (c[1] in d) and (c[2] in d): return (2, (c[1], c[2], c[0]))
            if c[0] in d:
                c_ = list(c)
                c_.remove(c[0])
                d_ = list(d)
                d_.remove(c[0])
                cd = [c[0]] + sorted([c_[0], c_[1], d_[0]], reverse=True)
                return (1, tuple(cd))
            if c[1] in d:
                c_ = list(c)
                c_.remove(c[1])
                d_ = list(d)
                d_.remove(c[1])
                cd = [c[1]] + sorted([c_[0], c_[1], d_[0]], reverse=True)
                return (1, tuple(cd))
            if c[2] in d:
                c_ = list(c)
                c_.remove(c[2])
                d_ = list(d)
                d_.remove(c[2])
                cd = [c[2]] + sorted([c_[0], c_[1], d_[0]], reverse=True)
                return (1, tuple(cd))
            cd = [c[0], c[1], c[2], d[0], d[1]]
            cd = sorted(cd, reverse=True)
            return (0, tuple(cd))
            
            


def s22(h: Hand, d: list):
    row2 = h.rows[2]
    combo1 = h.rows[1].combo
    kind1, cards1 = combo1
    kind2, cards2 = row2.combo
    add_card = row2.add_card
    flush = row2.flush
    d0, d1, d2 = d
    r0, r1, r2 = d0 // 4, d1 // 4, d2 // 4
    pairs = (
        (r0, r1, r0 if r0 == r1 else -1),
        (r0, r2, r0 if r0 == r2 else -1),
        (r1, r2, r1 if r1 == r2 else -1)
        )
    max_points = penalty
    if add_card is add_card_f:
        if (d[0] & 3 == row2.flush) + (d[1] & 3 == row2.flush) + (d[2] & 3 == row2.flush) >= 2:

            pass
        s0, s1, s2 = d0 % 4, d1 % 4, d2 % 4
        if flush == s0 == s1 or flush == s0 == s2 or flush == s1 == s2:
            print(f'cards2, r0, r1, r2 {cards2}, {r0}, {r1}, {r2}')
            if kind1 < 5: return 4
            else:
                if flush == s0 == s1: f0, f1 = r0, r1
                elif flush == s0 == s2: f0, f1 = r0, r2
                else: f0, f1 = r1, r2
                mask1 = (1 << cards1[0]) | (1 << cards1[1]) | (1 << cards1[2]) | (1 << cards1[3]) | (1 << cards1[4])
                mask2 = (1 << cards2[0]) | (1 << cards2[1]) | (1 << cards2[2]) | (1 << f0) | (1 << f1)
                return 4 if mask2 >= mask1 else penalty
        else:
            if (3, (cards2[0],)) < (kind1, cards1): return penalty
    if add_card is add_card_s:
        s = row2.max_combo[1][0]
        mask = MASK[cards2[0]] | MASK[cards2[1]] | MASK[cards2[2]] | MASK[r0] | MASK[r1] | MASK[r2]
        print(f'{mask:b}', cards2, r0, r1, r2)
        if (mask & MASK5[s - 3]) == MASK5[s - 3]: return 4
        if s > 3 and (mask & MASK5[s - 4]) == MASK5[s - 4] and (4, (s-1,)) >= combo1: return 4

        

                


    if add_card is add_card_fs:
        k0, k1, k2 = row2.combo[1]
        if row2.flush == d[0] % 4 == d[1] % 4:
            a, b = r0, r1
            if a > k0:
                if b > k0: cards5 = (a, b, k0, k1, k2)
                elif b > k1: cards5 = (a, k0, b, k1, k2)
                elif b > k2: cards5 = (a, k0, k1, b, k2)
                else: cards5 = (a, k0, k1, k2, b)
            elif a > k1:
                if b > k1: cards5 = (k0, a, b, k1, k2)
                elif b > k2: cards5 = (k0, a, k1, b, k2)
                else: cards5 = (k0, a, k1, k2, b)
            elif a > k2:
                if b > k2: cards5 = (k0, k1, a, b, k2)
                else: cards5 = (k0, k1, a, k2, b)
            else: cards5 = (k0, k1, k2, a, b)
            if row2.add_card is add_card_f:
                return 4 if (5, cards5) >= combo1 else penalty
            else:
                if cards5[0] - cards5[4] == 4:
                    if cards5[0] == 12: return 25
                    else:
                        return 15 if (8, (cards5[0],)) >= combo1 else penalty
                if cards5[0] == 12 and cards5[1] == 3:
                    if (8, (3,)) >= combo1: return 15
                if (5, cards5) >= combo1: max_points = 4
        if row2.flush == d[0] % 4 == d[2] % 4:
            a, b = r0, r2
            if a > k0:
                if b > k0: cards5 = (a, b, k0, k1, k2)
                elif b > k1: cards5 = (a, k0, b, k1, k2)
                elif b > k2: cards5 = (a, k0, k1, b, k2)
                else: cards5 = (a, k0, k1, k2, b)
            elif a > k1:
                if b > k1: cards5 = (k0, a, b, k1, k2)
                elif b > k2: cards5 = (k0, a, k1, b, k2)
                else: cards5 = (k0, a, k1, k2, b)
            elif a > k2:
                if b > k2: cards5 = (k0, k1, a, b, k2)
                else: cards5 = (k0, k1, a, k2, b)
            else: cards5 = (k0, k1, k2, a, b)
            if cards5[0] - cards5[4] == 4:
                if cards5[0] == 12: return 25
                else:
                    return 15 if (8, (cards5[0],)) >= combo1 else penalty
            if cards5[0] == 12 and cards5[1] == 3:
                if (8, (3,)) >= combo1: return 15
        if row2.flush == d[1] % 4 == d[2] % 4:
            a, b = r1, r2
            if a > k0:
                if b > k0: cards5 = (a, b, k0, k1, k2)
                elif b > k1: cards5 = (a, k0, b, k1, k2)
                elif b > k2: cards5 = (a, k0, k1, b, k2)
                else: cards5 = (a, k0, k1, k2, b)
            elif a > k1:
                if b > k1: cards5 = (k0, a, b, k1, k2)
                elif b > k2: cards5 = (k0, a, k1, b, k2)
                else: cards5 = (k0, a, k1, k2, b)
            elif a > k2:
                if b > k2: cards5 = (k0, k1, a, b, k2)
                else: cards5 = (k0, k1, a, k2, b)
            else: cards5 = (k0, k1, k2, a, b)
            if cards5[0] - cards5[4] == 4:
                if cards5[0] == 12: return 25
                else:
                    return 15 if (8, (cards5[0],)) >= combo1 else penalty
            if cards5[0] == 12 and cards5[1] == 3:
                if (8, (3,)) >= combo1: max_points = 15
        if max_points > -6: return max_points
    match kind2:
        case 0:
            k0, k1, k2 = row.combo[1]
            for a, b, r in pairs:
                if r != -1:
                    if k0 == r:
                        if 0 > max_points and (3, (r,)) >= combo1: max_points = 0
                    elif k1 == r:
                        if 0 > max_points and (3, (r,)) >= combo1: max_points = 0
                    elif k2 == r:
                        if 0 > max_points and (3, (r,)) >= combo1: max_points = 0
                    else:
                        if 0 > max_points and (1, (r, k0, k1, k2)) >= combo1: max_points = 0
                elif 0 > max_points and (a == k0 or a == k1 or a == k2 or b == k0 or b == k1 or b == k2):
                    if a == k0 and b == k1:
                        if (2, (a, b, k2)) >= combo1:
                            max_points = 0
                    elif a == k0 and b == k2:
                        if (2, (a, b, k1)) >= combo1:
                            max_points = 0
                    elif a == k1 and b == k2:
                        if (2, (a, b, k0)) >= combo1:
                            max_points = 0
                    elif a == k0:
                        if b > k1:
                            if (1, (a, b, k1, k2)) >= combo1: max_points = 0
                        elif b > k2:
                            if (1, (a, k1, b, k2)) >= combo1: max_points = 0
                        else:
                            if (1, (a, k1, k2, b)) >= combo1: max_points = 0
                    elif a == k1:
                        if b > k2:
                            if (1, (k0, a, b, k2)) >= combo1: max_points = 0
                        else:
                            if (1, (k0, a, k2, b)) >= combo1: max_points = 0
                    elif a == k2:
                        if (1, (k0, k1, a, b)) >= combo1: max_points = 0
                    elif b == k0:
                        if (1, (b, a, k1, k2)) >= combo1: max_points = 0
                    elif b== k1:
                        if a > k0:
                            if (1, (b, a, k0, k2)) >= combo1: max_points = 0
                        else:
                            if (1, (b, k0, a, k2)) >= combo1: max_points = 0
                    elif b == k2:
                        if a > k0:
                            if (1, (b, a, k0, k1)) >= combo1: max_points = 0
                        elif a > k1:
                            if (1, (b, k0, a, k1)) >= combo1: max_points = 0
                        else:
                            if (1, (b, k0, k1, a)) >= combo1: max_points = 0
                if a > k0:
                    if b > k0: cards5 = (a, b, k0, k1, k2)
                    elif b > k1: cards5 = (a, k0, b, k1, k2)
                    elif b > k2: cards5 = (a, k0, k1, b, k2)
                    else: cards5 = (a, k0, k1, k2, b)
                elif a > k1:
                    if b > k1: cards5 = (k0, a, b, k1, k2)
                    elif b > k2: cards5 = (k0, a, k1, b, k2)
                    else: cards5 = (k0, a, k1, k2, b)
                elif a > k2:
                    if b > k2: cards5 = (k0, k1, a, b, k2)
                    else: cards5 = (k0, k1, a, k2, b)
                else: cards5 = (k0, k1, k2, a, b)
                if cards5[0] - cards5[4] == 4:
                    return 2 if (4, (cards5[0],)) >= combo1 else penalty
                elif cards5[0] == 12 and cards5[1] == 3:
                    if (4, (3,)) >= combo1: max_points = 2
            return max_points            
        case 1:
            card0, card1 = row.combo[1]
            for a, b, r in pairs:
                if r != -1:
                    if card1 == r:
                        if 6 > max_points and (6, (r, card0)) >= combo1: max_points = 6
                    elif card0 == r:
                        if 10 > max_points and (7, (r,)) >= combo1: max_points = 10
                    elif 0 > max_points and (2, (card0, r, card1)) >= combo1: max_points = 0
                    elif 0 > max_points and (2, (r, card0, card1)) >= combo1: max_points = 0
                elif a == card0:
                    if b == card1:
                        if 6 > max_points and (6, (a, b)) >= combo1: max_points = 6
                    else:
                        if 0 > max_points and (3, (a,)) >= combo1: max_points = 0
                elif b == card0:
                    if a == card1:
                        if 6 > max_points and (6, (b, a)) >= combo1: max_points = 6
                    else:
                        if 0 > max_points and (3, (b,)) >= combo1: max_points = 0
                elif a == card1:
                    if 0 > max_points and (2, (card0, a, b)) >= combo1: max_points = 0
                    elif 0 > max_points and (2, (a, card0, b)) >= combo1: max_points = 0
                elif b == card1:
                    if 0 > max_points and (2, (card0, b, a)) >= combo1: max_points = 0
                    elif 0 > max_points and (2, (b, card0, a)) >= combo1: max_points = 0
                else:
                    if 0 > max_points:
                        k0, k1, k2 = card1, a, b
                        if k1 > k0:
                            k0, k1 = k1, k0
                        if k2 > k0:
                            k0, k2 = k2, k0
                        if k2 > k1:
                            k1, k2 = k2, k1
                        if (1, (card0, k0, k1, k2)) >= combo1: max_points = 0
            return max_points
        case 3:
            set_rank = cards[0]
            set_combo = (3, (set_rank,))
            for a, b, r in pairs:
                if r != -1:
                    if 6 > max_points and (6, (set_rank, r)) >= combo1: max_points = 6
                elif a == set_rank:
                    if 10 > max_points and (7, (a,)) >= combo1: max_points = 10
                elif b == set_rank:
                    if 10 > max_points and (7, (b,)) >= combo1: max_points = 10
                else:
                    if 0 > max_points and set_combo >= combo1: max_points = 0
    return max_points
       

def s3p(f, h_: Hand) -> tuple:
    start = dt.now()
    for card in f: 
        if card in h_.cards:
            h_.cards.remove(card)
    pairs = ((f[0], f[1]), (f[0], f[2]), (f[1], f[2]))
    deals = tuple(combinations(h_.cards, 3))
    max_points = penalty * len(deals)
    p = 0
    if h_.rows[0].cells >= 2:
        for pair in pairs:
            h = h_.clone()
            h.rows[0].add_card(h.rows[0], pair[0])
            h.rows[0].add_card(h.rows[0], pair[1])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[0], 0), (pair[1], 0))
    if h_.rows[1].cells >= 2:
        for pair in pairs:
            h = h_.clone()
            h.rows[1].add_card(h.rows[1], pair[0])
            h.rows[1].add_card(h.rows[1], pair[1])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[0], 1), (pair[1], 1))
    if h_.rows[2].cells >= 2:
        for pair in pairs:
            h = h_.clone()
            h.rows[2].add_card(h.rows[2], pair[0])
            h.rows[2].add_card(h.rows[2], pair[1])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[0], 2), (pair[1], 2))
    if h_.rows[0].cells and h_.rows[1].cells:
        for pair in pairs:
            h = h_.clone()
            h.rows[0].add_card(h.rows[0], pair[0])
            h.rows[1].add_card(h.rows[1], pair[1])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[0], 0), (pair[1], 1))
            h = h.clone()
            h.rows[0].add_card(h.rows[0], pair[1])
            h.rows[1].add_card(h.rows[1], pair[0])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[1], 0), (pair[0], 1))

    if h_.rows[0].cells and h_.rows[2].cells:
        for pair in pairs:
            h = h_.clone()
            h.rows[0].add_card(h.rows[0], pair[0])
            h.rows[2].add_card(h.rows[2], pair[1])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[0], 0), (pair[1], 2))
            h = h_.clone()
            h.rows[0].add_card(h.rows[0], pair[1])
            h.rows[2].add_card(h.rows[2], pair[0])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[1], 0), (pair[0], 2))
    if h_.rows[1].cells and h_.rows[2].cells:
        for pair in pairs:
            h = h_.clone()
            h.rows[1].add_card(h.rows[1], pair[0])
            h.rows[2].add_card(h.rows[2], pair[1])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[0], 1), (pair[1], 2))
            h = h_.clone()
            h.rows[1].add_card(h.rows[1], pair[1])
            h.rows[2].add_card(h.rows[2], pair[0])
            if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo:
                r = 0
                for deal in deals:
                    r += s4(deal, h)
                if r > max_points:
                    max_points = r
                    p = ((pair[1], 1), (pair[0], 2))
    print(f'elapsed time for 4 free cells {(dt.now() - start).total_seconds()}')
    return p

class Row:
    def __init__(self, row: int):
        self.row = row
        self.reset()
    def reset(self):
        self.cells = 3 if self.row == 0 else 5
        self.combo, self.max_combo = 0, 0
        self.flush = -1
        self.points = 0
        self.add_card = add_card_fs if self.row else add_card3
    def clone(self):
        obj = self.__class__.__new__(self.__class__)

        obj.row = self.row
        obj.cells = self.cells
        obj.combo = self.combo
        obj.max_combo = self.max_combo
        obj.flush = self.flush
        obj.points = self.points
        obj.add_card = self.add_card
        return obj
class Hand:
    def __init__(self):
        self.rows = [Row(0), Row(1), Row(2)]
        self.reset()
    def reset(self):
        for row in self.rows: row.reset()
        self.cards = list(range(52))
#        self.indexes3 = [
#                       ((0,0),(1,0)), ((0,0),(2,0)), ((1,0),(2,0)), ((0,1),(1,1)), ((0,1),(2,1)), ((1,1),(2,1)),
#                      ((0,2),(1,2)), ((0,2),(2,2)), ((1,2),(2,2)), 
#                        ((0,0),(1,1)), ((0,0),(2,1)), ((1,0),(2,1)), ((1,0),(0,1)), ((2,0),(0,1)), ((2,0),(1,1)), 
#                        ((0,0),(1,2)), ((0,0),(2,2)), ((1,0),(2,2)), ((1,0),(0,2)), ((2,0),(0,2)), ((2,0),(1,2)), 
#                        ((0,1),(1,2)), ((0,1),(2,2)), ((1,1),(2,2)), ((1,1),(0,2)), ((2,1),(0,2)), ((2,1),(1,2))
#                        ]
#        self.indexes2 = [(0,0), (1,0), (0,1), (1,1), (0,2), (1,2)]
#    def remove_index3_2(self, row):
#        for i in reversed(range(len(self.indexes3))):
#            if self.indexes3[i][0][1] == row and self.indexes3[i][1][1] == row: del self.indexes3[i]
#    def remove_index3_1(self, row):
#        for i in reversed(range(len(self.indexes3))):
#            if self.indexes3[i][0][1] == row or  self.indexes3[i][1][1] == row: del self.indexes3[i]
#    def remove_index2(self, row):
#        for i in reversed(range(len(self.indexes2))):
#            if self.indexes2[i][1] == row: del self.indexes2[i]
    def clone(self):
        obj = self.__class__.__new__(self.__class__)
        obj.rows = [row.clone() for row in self.rows]
        obj.cards = self.cards.copy()
        return obj

hand = Hand()
