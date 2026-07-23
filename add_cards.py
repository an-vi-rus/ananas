def init(h):
    global hand
    hand = h
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
    row.cells -= 1
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
                    if rank > cards[1]: row.combo = (1,(cards[0], rank, cards[1], cards[2]))
                    elif rank > cards[2]: row.combo = (1,(cards[0], cards[1], rank, cards[2]))
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
                    row.max_combo = (3, (cards[0]))
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
            row.max_combo = (3, (cards[0]))
            return

def add_card_f(row: Row, card: int):
    rank = card // 4
    suit = card % 4
    cards = row.combo[1]
    match row.cells:
        case 1:
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
        case 2:
            if suit != row.flush: row.add_card = add_card5
            row.add_card(row, card)
            return
        case 3:
            if suit != row.flush: row.add_card = add_card5
            row.add_card(row, card)
    return

def add_card_s(row: Row, card: int):
    add_card5(row, card)
    if row.combo[0]:
        row.add_card = add_card5
        return
    cards = row.combo[1]
    if not row.cells:
        if cards[0] - cards[4] == 4:
            row.combo = (4, [cards[0]])
            row.max_combo = row.combo
            row.points = 2 if row.row == 2 else 4
            return
        if cards[0] == 12 and cards[1] == 3:
            row.combo = (4, [3])
            row.max_combo = row.combo
            row.points = 2 if row.row == 2 else 4
            return
    if not (cards[0] - cards[-1] <= 4 or cards[0] == 12 and cards[1] <= 3):
        row.add_card = add_card5
    return

def add_card_fs(row: Row, card):
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
                row.combo = (8, [s])
                row.max_combo = row.combo
                if s < 12: row.points = 15 if row.row ==2 else 30
                else: row.points = 25 if row.row == 2 else 50
                return
            row.combo = (5, cards)
            row.max_combo = row.combo
            row.points = 4 if row.row == 2 else 8
            return
        if s:
            row.combo = (4, [s])
            row.max_combo = row.combo
            row.points = 2 if row.row == 2 else 4
            return
    if not f:
        if not s:
            row.add_card = add_card5
            return
        row.add_card = add_card_s
        return
    if not s:
        row.add_card = add_card_f
    return