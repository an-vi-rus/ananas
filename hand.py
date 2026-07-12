
premium = 6

class Row:
    def __init__(self, row: int):
        self.row = row
    def reset(self):
        self.cells = 3 if self.row == 3 else 5
        self.combo, self.max_combo = 0, 0
        self.flush = -1
        self.points = 0
        self.add_card = add_card_fs if self.row else add_card3
class Hand:
    def __init__(self):
        self.rows = [Row[0], Row[1], Row[2]]
        pass
    def reset(self):
        for row in self.rows: row.reset()
        self.cards = list(range(52))
        self.indexes3 = [
                        ((0,0),(1,0)), ((0,0),(2,0)), ((1,0),(2,0)), ((0,1),(1,1)), ((0,1),(2,1)), ((1,1),(2,1)),
                        ((0,2),(1,2)), ((0,2),(2,2)), ((1,2),(2,2)), 
                        ((0,0),(1,1)), ((0,0),(2,1)), ((1,0),(2,1)), ((1,0),(0,1)), ((2,0),(0,1)), ((2,0),(1,1)), 
                        ((0,0),(1,2)), ((0,0),(2,2)), ((1,0),(2,2)), ((1,0),(0,2)), ((2,0),(0,2)), ((2,0),(1,2)), 
                        ((0,1),(1,2)), ((0,1),(2,2)), ((1,1),(2,2)), ((1,1),(0,2)), ((2,1),(0,2)), ((2,1),(1,2))
                        ]
        self.indexes2 = [(0,0), (1,0), (0,1), (1,1), (0,2), (1,2)]
    def remove_index3_2(self, row):
        for i in reversed(range(len(self.indexes3))):
            if self.indexes3[i][0][1] == row and self.indexes3[i][1][1] == row: del self.indexes3[i]
    def remove_index3_1(self, row):
        for i in reversed(range(len(self.indexes3))):
            if self.indexes3[i][0][1] == row or  self.indexes3[i][1][1] == row: del self.indexes3[i]
    def remove_index2(self, row):
        for i in reversed(range(len(self.indexes2))):
            if self.indexes2[i][1] == row: del self.indexes2[i]

def is_straight(combo1):
    if combo1[0] - combo1[-1] <= 4: return min(combo1[-1] + 4, 12)
    if combo1[0] == 12 and combo1[1] <= 3: return 3
    return 0
def rank5(row: Row, card):
    rank = card // 4
    match row.cells:
        case 0:
            match row.combo[0]:
                case 1:
                    if row.combo[1][0] == rank: return (3, row.combo[1])
                    if row.combo[1][1] == rank: return (2, row.combo[1]) if row.combo[1][0] > rank else (2, [rank, row.combo[1][0], row.combo[1][2]])
                    if row.combo[1][2] == rank: return (2, [row.combo[1][0], rank, row.combo[1][1]]) if row.combo[1][0] > rank else (2, [rank, row.combo[1][0], row.combo[1][1]])
                case 2:
                    if row.combo[1][0] == rank: return (6, row.combo[1])
                    if row.combo[1][1] == rank: return (6, [row.combo[1][1], row.combo[1][0]])
                    return (2, row.combo[1] + [rank])
                case 0:
                    if rank in row.combo[1]:
                        r = row.combo[1][:]
                        r.remove(rank)
                        return (1, [rank] + r)
                case 3:
                    if row.combo[1][0] == rank: return (7, row.combo[1])
                    if row.combo[1][1] == rank: return (6, row.combo[1])
                    return row.combo
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
                case 3: return (7, row.combo[1]) if row.combo[1][0] == rank else (3, row.combo[1][0] + [rank])
        case 2:
            if row.combo[0]: return (3, [rank]) if rank == row.combo[1][0] else (1, row.combo[1] + [rank])
            if rank == row.combo[1][0]: return (1, row.combo[1])
            if rank == row.combo[1][1]: return (1, [rank, row.combo[1][0]])
            return (0, sorted(row.combo[1] + [rank], reverse=True))
        case 3:
            if rank == row.combo[1][0]: return (1, [rank])
            return (0, [row.combo[1][0], rank]) if row.combo[1][0] > rank else (0, [rank, row.combo[1][0]])
def rank3(row: Row, card):
    rank = card // 4
    match row.cells:
        case 0:
            if row.combo[0]: return (3, [rank]) if rank == row.combo[1][0] else (1, row.combo[1] + [rank])
            if rank == row.combo[1][0]: return (1, row.combo[1])
            if rank == row.combo[1][1]: return (1, [rank, row.combo[1][0]])
            return (0, sorted(row.combo[1] + [rank], reverse=True))
        case 1:
            if rank == row.combo[1][0]: return (1, [rank])
            return (0, [row.combo[1][0], rank]) if row.combo[1][0] > rank else (0, [rank, row.combo[1][0]])
        case 2: return (0, [rank])
def add_card_s(row: Row, card):
    row.combo = rank5(row, card)
    match row.cells:
        case 0:
            if row.combo[0] == 0:
                s = is_straight(row.combo[1])
                if s: 
                    row.combo = (4, [s])
                    row.max_combo = row.combo
                    row.points = 4 if row.row == 1 else 2
                    return
            row.max_combo = row.combo
            return
        case 1:
            if row.combo[0] == 0:
                if is_straight(row.combo) == 0:
                    row.add_card = add_card5
                    row.max_combo = (1, row.combo[1])
                return
            row.add_card = add_card5
            row.max_combo = (3, row.combo[1])
            return
        case 2:
            if row.combo[0] == 0:
                if is_straight(row.combo) == 0:
                    row.add_card = add_card5
                    row.max_combo = (3, row.combo[1])
                return
            row.add_card = add_card5
            row.max_combo = (7, row.combo[1])
            return
def add_card_f(row: Row, card):
    suit = card % 4
    row.combo = rank5(row, card)
    match row.cells:
        case 0:
            if row.flush == suit:
                row.combo = (5, row.combo[1])
                row.max_combo = row.combo
                row.points = 8 if row.row == 1 else 4
                return
            row.max_combo = row.combo
            return
        case 1:
            if row.combo[0] == 0:
                if row.flush != suit:
                    row.add_card = add_card5
                    row.max_combo = (1, row.combo[1])
                return
            row.add_card = add_card5
            row.max_combo = (3, row.combo[1])
            return
        case 2:
            if row.combo[0] == 0:
                if row.flush != suit:
                    row.add_card = add_card5
                    row.max_combo = (3, row.combo[1])
                return
            row.add_card = add_card5
            row.max_combo = (7, row.combo[1])
            return
def add_card_fs(row: Row, card):
    suit = card % 4
    row.combo = rank5(row, card)
    match row.cells:
        case 0:
            if row.combo[0] == 0:
                s = is_straight(row.combo[1])
                if s > 0 and row.flush == suit:
                    if s < 12:
                        row.combo = (8, [s])
                        row.max_combo = row.combo
                        row.points = 30 if row.row == 1 else 15
                        return
                    row.combo = (9, [s])
                    row.max_combo = row.combo
                    row.points = 50 if row.row == 1 else 25
                    return
                if row.flush == suit:
                    row.combo = (5, row.combo[1])
                    row.max_combo = row.combo
                    row.points = 8 if row.row == 1 else 4
                    return
                if s > 0:
                    row.combo = (4, [s])
                    row.max_combo = row.combo
                    row.points = 4 if row.row == 1 else 2
                    return
            row.max_combo = row.combo
            return
        case 1:
            if row.combo[0] == 0:
                s = is_straight(row.combo[1])
                if s > 0 and row.flush == suit:
                    row.max_combo = (8, [s]) if s < 12 else (9, [12])
                    return
                if row.flush == suit:
                    row.max_combo = (5, [12] + row.combo[1])
                    row.add_card = add_card_f
                    return
                if s > 0:
                    row.max_combo = (4, [s])
                    row.add_card = add_card_s
                    return
                row.max_combo = (1, row.combo[1])
                row.add_card = add_card5
                return
            row.max_combo = (3, row.combo[1])
            row.add_card = add_card5
            return
        case 2:
            if row.combo[0] == 0:
                s = is_straight(row.combo[1])
                if s > 0 and row.flush == suit:
                    row.max_combo = (8, [s]) if s < 12 else (9, [12])
                    return
                if row.flush == suit:
                    row.max_combo = (5, [12] + row.combo[1])
                    row.add_card = add_card_f
                    return
                if s > 0:
                    row.max_combo = (4, [s])
                    row.add_card = add_card_s
                    return
                row.max_combo = (3, row.combo[1])
                row.add_card = add_card5
                return
            row.max_combo = (7, row.combo[1])
            row.add_card = add_card5
            return
        case 3:
            if row.combo[0] == 0:
                s = is_straight(row.combo[1])
                if s > 0 and row.flush == suit:
                    row.max_combo = (8, [s]) if s < 12 else (9, [12])
                    return
                if row.flush == suit:
                    row.max_combo = (5, [12] + row.combo[1])
                    row.add_card = add_card_f
                    return
                if s > 0:
                    row.max_combo = (4, [s])
                    row.add_card = add_card_s
                    return
                row.max_combo = (7, row.combo[1])
                row.add_card = add_card5
                return
            row.max_combo = (7, row.combo[1])
            row.add_card = add_card5
            return
        case 4:
            row.flush = suit
            rank = card // 4
            row.combo = (0, [rank])
            row.max_combo = (8, [rank + 4]) if rank < 8 else (9, [12])
            return
def add_card5(row: Row, card):
    row.combo = rank5(row, card)
    match row.cells:
        case 0:
            row.max_combo = row.combo
            match row.combo[0]:
                case 3: row.points = 2 if row.row == 1 else 0
                case 6: row.points = 12 if row.row == 1 else 6
                case 7: row.points = 20 if row.row == 1 else 10
            return
        case 1:
            match row.combo[0]:
                case 2: 
                    row.max_combo = (6, row.combo[1])
                    return
                case 1: 
                    row.max_combo = (3, row.combo[1])
                    return
                case 0: 
                    row.max_combo = (1, row.combo[1])
                    return
                case 3:
                    row.max_combo = (7, row.combo[1])
                    return
                case 7: row.max_combo = row.combo
            return
        case 2:
            if row.combo > 0:
                row.max_combo = (7, row.combo[1])
                return
            row.max_combo = (3, row.combo[1])
            return
def add_card3(row: Row, card):
    row.combo = rank3(row, card)
    if row.cells == 0:
        match row.combo[0]:
            case 0: return
            case 1: 
                if row.combo[1][0] < 4: return
                row.points = row.combo[1][0] - 3 + premium
                return
            case 3:
                row.points = row.combo[1][0] + 10 + premium
    return 


