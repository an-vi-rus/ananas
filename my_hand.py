from itertools import combinations
from datetime import datetime as dt

penalty = -6
premium = 6
HIGH_ROW_PAIR = (0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7+premium, 8+premium, 9+premium)
MIDDLE_ROW_ROYALTY = (0, 0, 0, 2, 4, 8, 12, 20, 30, 50)
LOW_ROW_ROYALTY = (0, 0, 0, 0, 2, 4, 6, 10, 15, 25)

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
    row.cells -= 1
    kinds, cards = row.combo
    match row.cells:
        case 0:
            if kinds:
                if rank != cards[0]:
                    row.combo = (1, [cards[0], rank])
                    row.points = HIGH_ROW_PAIR[cards[0]]
                    return
                row.combo = (3, [rank])
                row.points = rank + 10 + premium
                return
        case 1:
            if rank == cards[0]:
                row.combo = (1, [rank])
                return
            row.combo = (0, [cards[0], rank]) if cards[0] > rank else (0, [rank, cards[0]])
            return
        case 2: row.combo = (0, [rank])

def add_card5(row: Row, card: int):
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
    rank = card // 4
    suit = card % 4
    cards = row.combo[1]
    match row.cells:
        case 0:
            if suit == row.flush:
                row.cells -= 1
                if rank > cards[0]: cards = (rank, cards[0], cards[1], cards[2], cards[3])
                elif rank > cards[1]: cards = (cards[0], rank, cards[1], cards[2], cards[3])
                elif rank > cards[2]: cards = (cards[0], cards[1], rank, cards[2], cards[3])
                elif rank > cards[3]: cards = (cards[0], cards[1], cards[2], rank, cards[3])
                else: cards = (cards[0], cards[1], cards[2], cards[3], rank)
                row.combo = (5, cards)
                row.max_combo = row.combo
                row.points = 4 if row.row == 2 else 8
                return
            add_card5(row, card)
            return
        case 1:
            if suit != row.flush:
                row.add_card = add_card5
                add_card5(row, card)
                return
            add_card5(row, card)
            row.max_combo = (5, (12, 12))
            return
        case 2:
            if suit != row.flush:
                row.add_card = add_card5
                add_card5(row, card)
                return
            add_card5(row, card)
            row.max_combo = (5, (12, 12))
            return
    return

def add_card_s(row: Row, card: int):
    add_card5(row, card)
    if row.combo[0]:
        row.add_card = add_card5
        return
    cards = row.combo[1]
    if not row.cells:
        if cards[0] - cards[4] == 4:
            row.combo = (4, (cards[0],))
            row.max_combo = row.combo
            row.points = 2 if row.row == 2 else 4
            return
        if cards[0] == 12 and cards[1] == 3:
            row.combo = (4, (3,))
            row.max_combo = row.combo
            row.points = 2 if row.row == 2 else 4
            return
    if not (cards[0] - cards[-1] <= 4 or cards[0] == 12 and cards[1] <= 3):
        row.add_card = add_card5
    return

def add_card_fs(row: Row, card):
    rank, suit = card // 4, card % 4
    if row.cells == 4:
        row.flush = suit
        row.combo = (0, (rank,))
        row.max_combo = (8, (12,))
        return
    if row.cells == 3:
        if rank == row.combo[1][0]:
            row.combo = (1, (rank,))
            row.max_combo = (7, (rank,))
            row.add_card = add_card5
            row.flush = -1
            return
        row.combo = (0, (rank, row.combo[1][0])) if rank > row.combo[1][0] else (0, (row.combo[1][0], rank))
        cards = row.combo[1]
        if cards[0] - cards[-1] <= 4: s = min(cards[-1] + 4, 12)
        elif cards[0] == 12 and cards[1] <= 3: s = 3
        else: s = 0
        f = suit == row.flush
        if not f:
            row.add_card = add_card_s if s else add_card5
            row.max_combo =(7, (row.combo[1][0],))
            return
        if not s:
            row.add_card = add_card_f
            row.max_combo =(7, (row.combo[1][0],))
        return

    f = card % 4 == row.flush
    add_card5(row, card)
    cards = row.combo[1]
    if row.combo[0]:
        row.add_card = add_card5
        return
    if cards[0] - cards[-1] <= 4: s = min(cards[-1] + 4, 12)
    elif cards[0] == 12 and cards[1] <= 3: s = 3
    else: s = 0
    if not row.cells:
        if f:
            if s:
                row.combo = (8, (s,))
                row.max_combo = row.combo
                if s < 12: row.points = 15 if row.row ==2 else 30
                else: row.points = 25 if row.row == 2 else 50
                return
            row.combo = (5, cards)
            row.max_combo = row.combo
            row.points = 4 if row.row == 2 else 8
            return
        if s:
            row.combo = (4, (s,))
            row.max_combo = row.combo
            row.points = 2 if row.row == 2 else 4
            return
    if not f:
        if not s:
            row.add_card = add_card5
            return
        row.add_card = add_card_s
        row.max_combo = (4, (s,))
        return
    if not s:
        row.add_card = add_card_f
        row.max_combo = (5, (12, 12))
        return
    row.max_combo = (8, (s,))

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
            if rank == combo[1][0]: return (1, combo[1])
            if rank == combo[1][1]: return (1, [rank, combo[1][0]])
            return (0, sorted(combo[1] + [rank], reverse=True))    
        case 1:
            if rank == combo[1][0]: return (3, combo[1]) 
            return (1, combo[1] + [rank])
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
def c4_5(combo: tuple, rank: int) -> tuple:
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
def final_22(pair: list):
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    combo = c4_5(c3_4(hand.rows[2].combo, rank0), rank1)
    if hand.rows[2].add_card is add_card5:
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
        obj.combo = (self.combo[0], self.combo[1].copy())
        obj.max_combo = (self.max_combo[0], self.max_combo[1].copy())
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
