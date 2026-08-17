from helpers import *
from tables import *

PENALTY, PREMIUM = -6, 6

HIGH_ROW_PAIR = (0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7 + PREMIUM, 8 + PREMIUM, 9 + PREMIUM)
HIGH_ROW_TRIPLE = tuple(i + 10 + PREMIUM for i in range(13))
MIDDLE_ROW_ROYALTY = (0, 0, 0, 2, 4, 8, 12, 20, 30, 50)
MIDDLE_ROYALTY = (
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x00-0x0f
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,  # 0x10-0x1f
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x20-0x2f
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 0x30-0x3f
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  # 0x40-0x4f
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,  # 0x50-0x5f
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,  # 0x60-0x6f
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,  # 0x70-0x7f
    30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 50, 50, 50, 50,  # 0x80-0x8f
)
LOW_ROW_ROYALTY = (0, 0, 0, 0, 2, 4, 6, 10, 15, 25)
LOW_ROYALTY = (
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x00-0x0f
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x10-0x1f
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x20-0x2f
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x30-0x3f
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 0x40-0x4f
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  # 0x50-0x5f
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,  # 0x60-0x6f
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,  # 0x70-0x7f
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 25, 25, 25, 25,  # 0x80-0x8f
)
def high_row_points():
    idx3 = [combo3(c)[0] >> 8 for c in product(range(13), repeat=3)]
    t = [0] * 0x3c01
    for idx in idx3:
        kind = idx >> 12
        if kind == 3: t[idx] = 10 + PREMIUM + ((idx >> 8) & 0xf)
        elif kind == 1: t[idx] = HIGH_ROW_PAIR[(idx >> 8) & 0xf]
    return t
HIGH_ROYALTY = high_row_points()

class Row:
    def __init__(self, row: int):
        self.row = row
        self.cells = 3 if self.row == 0 else 5
        self.idx, self.max_idx = 0, 0
        self.flush = -1
        self.points = 0

    def reset(self):
        self.cells = 3 if self.row == 0 else 5
        self.idx, self.max_idx = 0, 0
        self.flush = -1
        self.points = 0

    def clone(self):
        obj = self.__class__.__new__(self.__class__)

        obj.row = self.row
        obj.cells = self.cells
        obj.idx = self.idx
        obj.max_idx = self.max_idx
        obj.flush = self.flush
        obj.points = self.points

        return obj

class Hand:
    def __init__(self):
        self.rows = [Row(0), Row(1), Row(2)]
        self.cards = list(range(52))

    def reset(self):
        for row in self.rows: row.reset()
        self.cards = list(range(52))

    def clone(self):
        obj = self.__class__.__new__(self.__class__)
        obj.rows = [row.clone() for row in self.rows]
        obj.cards = self.cards.copy()
        return obj

def add_card5(row: Row, card):
    rank = card >> 2
    if row.cells == 0:
        if row.flush == -1:
            row.idx = T4_1[row.idx >> 4][rank]
            row.max_idx = row.idx
            row.points = LOW_ROYALTY[row.idx >> 16] if row.row == 2 else MIDDLE_ROYALTY[row.idx >> 16]
            return
        elif row.flush == (card & 3):
            row.idx = T4_1F[row.idx >> 4][rank]
            row.max_idx = row.idx 
            row.points = LOW_ROYALTY[row.idx >> 16] if row.row == 2 else MIDDLE_ROYALTY[row.idx >> 16]
            return
        else:
            row.idx = T4_1[row.idx >> 4][rank]
            row.max_idx = row.idx
            row.points = LOW_ROYALTY[row.idx >> 16] if row.row == 2 else MIDDLE_ROYALTY[row.idx >> 16]
            return        
    elif row.cells == 1:
        if row.flush == -1:
            row.idx, row.max_idx = T3_1[row.idx >> 8][rank]
            return
        elif row.flush == (card & 3):
            row.idx, row.max_idx = T3_1F[row.idx >> 8][rank]
            return
        else:
            row.flush = -1
            row.idx, row.max_idx = T3_1[row.idx >> 8][rank]
            return

    elif row.cells == 2:
        if row.flush == -1:
            row.idx, row.max_idx = T2_1[row.idx >> 12][rank]
            return
        elif row.flush == (card & 3):
            row.idx, row.max_idx = T2_1F[row.idx >> 12][rank]
            return 
        else:
            row.flush = -1
            row.idx, row.max_idx = T2_1[row.idx >> 12][rank]
            return

    elif row.cells == 3:
        if row.flush == (card & 3):
            row.idx, row.max_idx = T1_1F[row.idx >> 16][rank]
            return
        else:
            row.flush = -1
            row.idx, row.max_idx = T1_1[row.idx >> 16][rank]
            return

    else:
        row.idx = pack(0, rank)
        row.max_idx = pack(8, min(12, rank + 4))
        row.flush = card & 3
def add_card3(row: Row, card):
    rank = card >> 2
    if row.cells == 0:
        kind = row.idx >> 20
        rank0 = (row.idx >> 16) & 0xF
        if kind == 1:
            if rank == rank0:
                row.idx = pack(3, rank)
                row.points = HIGH_ROYALTY[row.idx >> 8]
                return
            row.idx = pack(1, rank0, rank)
            row.points = HIGH_ROYALTY[row.idx >> 8]
            return
        rank1 = (row.idx >> 12) & 0xF
        if rank == rank0:
            row.idx = pack(1, rank, rank1)
            row.points = HIGH_ROYALTY[row.idx >> 8]
            return
        if rank == rank1:
            row.idx = pack(1, rank, rank0)
            row.points = HIGH_ROYALTY[row.idx >> 8]
            return
        if rank > rank0:
            row.idx = pack(0, rank, rank0, rank1)
            return
        if rank > rank1:
            row.idx = pack(0, rank0, rank, rank1)
            return
        row.idx = pack(0, rank0, rank1, rank)
        return
    elif row.cells == 1:
        rank0 = (row.idx >> 16) & 0xF
        if rank == rank0:
            row.idx = pack(1, rank)
            return
        row.idx = pack(0, rank, rank0) if rank > rank0 else pack(0, rank0, rank)
        return
    else:
        row.idx = pack(0, rank)

def s00(h: Hand, c: list):
    idx = T1_3[(h.rows[0].idx >> 16) & 0xf][c[0] >> 2][c[1] >> 2][c[2] >> 2]
    if idx[0] <= h.rows[1].idx:
        return HIGH_ROYALTY[idx[0] >> 8] + h.rows[1].points + h.rows[2].points
    if idx[1] <= h.rows[1].idx:
        return HIGH_ROYALTY[idx[1] >> 8] + h.rows[1].points + h.rows[2].points
    if idx[2] <= h.rows[1].idx:
        return HIGH_ROYALTY[idx[2] >> 8] + h.rows[1].points + h.rows[2].points
    return PENALTY
def s00_(h: Hand, c: list):
    idx = T1_2[(h.rows[0].idx >> 16) & 0xf][c[0] >> 2][c[1] >> 2]
    if idx <= h.rows[1].idx:
        return HIGH_ROYALTY[idx >> 8] + h.rows[1].points + h.rows[2].points
    return PENALTY
def s00p(h: Hand, c: list):
    max_points = PENALTY
    p = 0
    idx0 = T1_2[(h.rows[0].idx >> 16) & 0xf][c[1] >> 2][c[2] >> 2]
    idx1 = T1_2[(h.rows[0].idx >> 16) & 0xf][c[0] >> 2][c[2] >> 2]
    idx2 = T1_2[(h.rows[0].idx >> 16) & 0xf][c[0] >> 2][c[1] >> 2]
    if idx0 <= h.rows[1].idx:
        points = HIGH_ROYALTY[idx0 >> 8]
        if points > max_points:
            max_points = points
            p = ((c[1], 0), (c[2], 0))
    if idx1 <= h.rows[1].idx:
        points = HIGH_ROYALTY[idx1 >> 8]
        if points > max_points:
            max_points = points
            p = ((c[0], 0), (c[2], 0))
    if idx2 <= h.rows[1].idx:
        points = HIGH_ROYALTY[idx2 >> 8]
        if points > max_points:
            max_points = points
            p = ((c[0], 0), (c[1], 0))
    return p

def s22(h: Hand, c: list):
    if h.rows[2].flush > -1:
        flush = h.rows[2].flush
        f0, f1, f2 = (c[0] & 3) == flush, (c[1] & 3) == flush, (c[2] & 3) == flush
        f = f0 + f1 + f2
        if f == 3:
            idx = T3_3F[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2][c[2] >> 2][0]
            if idx >= h.rows[1].idx:
                return LOW_ROYALTY[idx >> 16] + h.rows[0].points + h.rows[1].points
            else: return PENALTY
        if f == 2:
            if f0 == 0:
                idx = T3_2F[h.rows[2].idx >> 8][c[1] >> 2][c[2] >> 2]
            elif f1 == 0:
                idx = T3_2F[h.rows[2].idx >> 8][c[0] >> 2][c[2] >> 2]
            else:
                idx = T3_2F[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2]
            if idx >= h.rows[1].idx:
                return LOW_ROYALTY[idx >> 16] + h.rows[0].points + h.rows[1].points
            else: return PENALTY
    idx = T3_3[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2][c[2] >> 2][0]
    if idx >= h.rows[1].idx: return LOW_ROYALTY[idx >> 16] + h.rows[0].points + h.rows[1].points
    return PENALTY
def s22_(h: Hand, c: list):
    idx = T3_2[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2]
    if h.rows[2].flush != -1:
        if (c[0] & 3) == (c[1] & 3) == h.rows[2].flush:
            idx = T3_2F[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2]
    if idx >= h.rows[1].idx:
        return LOW_ROYALTY[idx >> 16] + h.rows[0].points + h.rows[1].points
    return PENALTY
def s22p(h: Hand, c: list):
    max_points = PENALTY
    p = 0
    flush = h.rows[2].flush
    idx = h.rows[2].idx >> 8
    idx0 = T3_2[idx][c[1] >> 2][c[2] >> 2]
    idx1 = T3_2[idx][c[0] >> 2][c[2] >> 2]
    idx2 = T3_2[idx][c[0] >> 2][c[1] >> 2]
    if flush != -1:
        if (c[1] & 3) == (c[2] & 3) == flush: idx0 = T3_2F[idx][c[1] >> 2][c[2] >> 2]
        if (c[0] & 3) == (c[2] & 3) == flush: idx1 = T3_2F[idx][c[0] >> 2][c[2] >> 2]
        if (c[0] & 3) == (c[1] & 3) == flush: idx2 = T3_2F[idx][c[0] >> 2][c[1] >> 2]
    if idx0 >= h.rows[1].idx:
        points = LOW_ROYALTY[idx0 >> 16]
        if points > max_points:
            max_points = points
            p = ((c[1], 2), (c[2], 2))
    if idx1 >= h.rows[1].idx:
        points = LOW_ROYALTY[idx1 >> 16]
        if points > max_points:
            max_points = points
            p = ((c[0], 2), (c[2], 2))
    if idx2 >= h.rows[1].idx:
        points = LOW_ROYALTY[idx2 >> 16]
        if points > max_points:
            max_points = points
            p = ((c[0], 2), (c[1], 2))
    return p

def s11(h: Hand, c: list):
    if h.rows[1].flush > -1:
        flush = h.rows[1].flush
        f0, f1, f2 = (c[0] & 3) == flush, (c[1] & 3) == flush, (c[2] & 3) == flush
        f = f0 + f1 + f2
        if f == 3:
            idx = T3_3F[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2][c[2] >> 2]
            if h.rows[2].idx >= idx[0]:
                return MIDDLE_ROYALTY[idx[0] >> 16] + h.rows[0].points + h.rows[2].points
            elif h.rows[2].idx >= idx[1]:
                return MIDDLE_ROYALTY[idx[1] >> 16] + h.rows[0].points + h.rows[2].points
            elif h.rows[2].idx >= idx[2]:
                return MIDDLE_ROYALTY[idx[2] >> 16] + h.rows[0].points + h.rows[2].points
            return PENALTY
        if f == 2:
            if f0 == 0:
                idx0 = T3_2F[h.rows[1].idx >> 8][c[1] >> 2][c[2] >> 2]
                idx1 = T3_2[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2]
                idx2 = T3_2[h.rows[1].idx >> 8][c[0] >> 2][c[2] >> 2]
                if h.rows[2].idx >= idx0:
                    return MIDDLE_ROYALTY[idx0 >> 16] + h.rows[0].points + h.rows[2].points
                if idx2 > idx1: idx1, idx2 = idx2, idx1
                if idx1 < h.rows[0].idx: return PENALTY
                if idx1 <= h.rows[2].idx: return MIDDLE_ROYALTY[idx1 >> 16] + h.rows[0].points + h.rows[2].points
                if idx2 < h.rows[0].idx: return PENALTY
                if idx2 <= h.rows[2].idx: return MIDDLE_ROYALTY[idx2 >> 16] + h.rows[0].points + h.rows[2].points
                return PENALTY
            elif f1 == 0:
                idx0 = T3_2F[h.rows[1].idx >> 8][c[0] >> 2][c[2] >> 2]
                idx1 = T3_2[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2]
                idx2 = T3_2[h.rows[1].idx >> 8][c[1] >> 2][c[2] >> 2]
                if h.rows[2].idx >= idx0:
                    return MIDDLE_ROYALTY[idx0 >> 16] + h.rows[0].points + h.rows[2].points
                if idx2 > idx1: idx1, idx2 = idx2, idx1
                if idx1 < h.rows[0].idx: return PENALTY
                if idx1 <= h.rows[2].idx: return MIDDLE_ROYALTY[idx1 >> 16] + h.rows[0].points + h.rows[2].points
                if idx2 < h.rows[0].idx: return PENALTY
                if idx2 <= h.rows[2].idx: return MIDDLE_ROYALTY[idx2 >> 16] + h.rows[0].points + h.rows[2].points
                return PENALTY
              
            else:
                idx0 = T3_2F[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2]
                idx1 = T3_2[h.rows[1].idx >> 8][c[0] >> 2][c[2] >> 2]
                idx2 = T3_2[h.rows[1].idx >> 8][c[1] >> 2][c[2] >> 2]
                if h.rows[2].idx >= idx0:
                    return MIDDLE_ROYALTY[idx0 >> 16] + h.rows[0].points + h.rows[2].points
                if idx2 > idx1: idx1, idx2 = idx2, idx1
                if idx1 < h.rows[0].idx: return PENALTY
                if idx1 <= h.rows[2].idx: return MIDDLE_ROYALTY[idx1 >> 16] + h.rows[0].points + h.rows[2].points
                if idx2 < h.rows[0].idx: return PENALTY
                if idx2 <= h.rows[2].idx: return MIDDLE_ROYALTY[idx2 >> 16] + h.rows[0].points + h.rows[2].points
                return PENALTY
    idx = T3_3[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2][c[2] >> 2]
    if idx[0] < h.rows[0].idx: return PENALTY
    if idx[0] <= h.rows[2].idx: return MIDDLE_ROYALTY[idx[0] >> 16] + h.rows[0].points + h.rows[2].points
    if idx[1] < h.rows[0].idx: return PENALTY
    if idx[1] <= h.rows[2].idx: return MIDDLE_ROYALTY[idx[1] >> 16] + h.rows[0].points + h.rows[2].points
    if h.rows[2].idx >= idx[2] >= h.rows[0].idx: return MIDDLE_ROYALTY[idx[2] >> 16] + h.rows[0].points + h.rows[2].points
    return PENALTY
def s11_(h: Hand, c: list):
    idx = T3_2[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2]
    if h.rows[1].flush != -1:
        if (c[0] & 3) == (c[1] & 3) == h.rows[1].flush:
            idx = T3_2F[h.rows[1].idx >> 8][c[0] >> 2][c[1] >> 2]
    if h.rows[0].idx <= idx <= h.rows[2].idx:
        return MIDDLE_ROYALTY[idx >> 16] + h.rows[0].points + h.rows[2].points
    return PENALTY
def s11p(h: Hand, c: list):
    max_points = PENALTY
    p = 0
    flush = h.rows[1].flush
    idx = h.rows[1].idx >> 8
    idx0 = T3_2[idx][c[1] >> 2][c[2] >> 2]
    idx1 = T3_2[idx][c[0] >> 2][c[2] >> 2]
    idx2 = T3_2[idx][c[0] >> 2][c[1] >> 2]
    if flush != -1:
        if (c[1] & 3) == (c[2] & 3) == flush: idx0 = T3_2F[idx][c[1] >> 2][c[2] >> 2]
        if (c[0] & 3) == (c[2] & 3) == flush: idx1 = T3_2F[idx][c[0] >> 2][c[2] >> 2]
        if (c[0] & 3) == (c[1] & 3) == flush: idx2 = T3_2F[idx][c[0] >> 2][c[1] >> 2]
    if h.rows[0].idx <= idx0 <= h.rows[2].idx:
        points = MIDDLE_ROYALTY[idx0 >> 16]
        if points > max_points:
            max_points = points
            p = ((c[1], 1), (c[2], 1))
    if h.rows[0].idx <= idx1 <= h.rows[2].idx:
        points = MIDDLE_ROYALTY[idx1 >> 16]
        if points > max_points:
            max_points = points
            p = ((c[0], 1), (c[2], 1))
    if h.rows[0].idx <= idx2 <= h.rows[2].idx:
        points = MIDDLE_ROYALTY[idx2 >> 16]
        if points > max_points:
            max_points = points
            p = ((c[0], 1), (c[1], 1))

    return p

def s01(h: Hand, c: list):
    max_points = PENALTY
    c0, c1, c2 = c[0] >> 2, c[1] >> 2, c[2] >> 2
    idx0 = h.rows[0].idx >> 12
    idx1 = h.rows[1].idx >> 4
    idx2 = h.rows[2].idx
    idx_00 = T2_1[idx0][c0][0]
    idx_01 = T2_1[idx0][c1][0]
    idx_02 = T2_1[idx0][c2][0]
    points00 = HIGH_ROYALTY[idx_00 >> 8]
    points01 = HIGH_ROYALTY[idx_01 >> 8]
    points02 = HIGH_ROYALTY[idx_02 >> 8]
    if h.rows[1].flush == -1:    
        idx_10 = T4_1[idx1][c0]
        idx_11 = T4_1[idx1][c1]
        idx_12 = T4_1[idx1][c2]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
        if idx_00 <= idx_11 <= idx2:
            points = points00 + points11
            if points > max_points: max_points = points
        if idx_00 <= idx_12 <= idx2:
            points = points00 + points12
            if points > max_points: max_points = points
        if idx_01 <= idx_10 <= idx2:
            points = points01 + points10
            if points > max_points: max_points = points
        if idx_01 <= idx_12 <= idx2:
            points = points01 + points12
            if points > max_points: max_points = points
        if idx_02 <= idx_10 <= idx2:
            points = points02 + points10
            if points > max_points: max_points = points
        if idx_02 <= idx_11 <= idx2:
            points = points02 + points11
            if points > max_points: max_points = points
        return max_points + h.rows[2].points if max_points > PENALTY else PENALTY
    flush = h.rows[1].flush 
    if (c[0] & 3) == flush:
        idx_10 = T4_1F[idx1][c0]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
    else:
        idx_10 = T4_1[idx1][c0]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
    if (c[1] & 3) == flush:
        idx_11 = T4_1F[idx1][c1]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
    else:
        idx_11 = T4_1[idx1][c1]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
    if (c[2] & 3) == flush:
        idx_12 = T4_1F[idx1][c2]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    else:
        idx_12 = T4_1[idx1][c2]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    if idx_00 <= idx_11 <= idx2:
        points = points00 + points11
        if points > max_points: max_points = points
    if idx_00 <= idx_12 <= idx2:
        points = points00 + points12
        if points > max_points: max_points = points
    if idx_01 <= idx_10 <= idx2:
        points = points01 + points10
        if points > max_points: max_points = points
    if idx_01 <= idx_12 <= idx2:
        points = points01 + points12
        if points > max_points: max_points = points
    if idx_02 <= idx_10 <= idx2:
        points = points02 + points10
        if points > max_points: max_points = points
    if idx_02 <= idx_11 <= idx2:
        points = points02 + points11
        if points > max_points: max_points = points
    return max_points + h.rows[2].points if max_points > PENALTY else PENALTY
def s01_(h: Hand, c: list):
    c0, c1 = c[0] >> 2, c[1] >> 2
    idx0 = h.rows[0].idx >> 12
    idx1 = h.rows[1].idx >> 4
    flush1 = h.rows[1].flush
    idx2 = h.rows[2].idx
    points2 = h.rows[2].points

    idx00 = T2_1[idx0][c0][0]
    idx01 = T2_1[idx0][c1][0]

    idx10 = T4_1[idx1][c0]
    idx11 = T4_1[idx1][c1]
    if flush1 != -1:
        if (c[0] & 3) == flush1: idx10 = T4_1F[idx1][c0]
        if (c[1] & 3) == flush1: idx11 = T4_1F[idx1][c1]

    if idx01 <= idx10 <= idx2:
        points0 = HIGH_ROYALTY[idx01 >> 8] + MIDDLE_ROYALTY[idx10 >> 16] + points2
    else: points0 = PENALTY
    if idx00 <= idx11 <= idx2:
            points1 = HIGH_ROYALTY[idx00 >> 8] + MIDDLE_ROYALTY[idx11 >> 16] + points2
    else: points1 = PENALTY

    return points1 if points1 > points0 else points0
def s01p(h: Hand, c: list):
    max_points = PENALTY
    p = 0
    c0, c1, c2 = c[0] >> 2, c[1] >> 2, c[2] >> 2
    idx0 = h.rows[0].idx >> 12
    idx1 = h.rows[1].idx >> 4
    idx2 = h.rows[2].idx
    idx_00 = T2_1[idx0][c0][0]
    idx_01 = T2_1[idx0][c1][0]
    idx_02 = T2_1[idx0][c2][0]
    points00 = HIGH_ROYALTY[idx_00 >> 8]
    points01 = HIGH_ROYALTY[idx_01 >> 8]
    points02 = HIGH_ROYALTY[idx_02 >> 8]
    if h.rows[1].flush == -1:    
        idx_10 = T4_1[idx1][c0]
        idx_11 = T4_1[idx1][c1]
        idx_12 = T4_1[idx1][c2]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
        if idx_00 <= idx_11 <= idx2:
            points = points00 + points11
            if points > max_points:
                max_points = points
                p = ((c[0], 0), (c[1], 1))
        if idx_00 <= idx_12 <= idx2:
            points = points00 + points12
            if points > max_points:
                max_points = points
                p = ((c[0], 0), (c[2], 1))
        if idx_01 <= idx_10 <= idx2:
            points = points01 + points10
            if points > max_points:
                max_points = points
                p = ((c[1], 0), (c[0], 1))
        if idx_01 <= idx_12 <= idx2:
            points = points01 + points12
            if points > max_points:
                max_points = points
                p = ((c[1], 0), (c[2], 1))
        if idx_02 <= idx_10 <= idx2:
            points = points02 + points10
            if points > max_points:
                max_points = points
                p = ((c[2], 0), (c[0], 1))
        if idx_02 <= idx_11 <= idx2:
            points = points02 + points11
            if points > max_points:
                max_points = points
                p = ((c[2], 0), (c[1], 1))
        return p
    flush = h.rows[1].flush 
    if (c[0] & 3) == flush:
        idx_10 = T4_1F[idx1][c0]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
    else:
        idx_10 = T4_1[idx1][c0]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
    if (c[1] & 3) == flush:
        idx_11 = T4_1F[idx1][c1]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
    else:
        idx_11 = T4_1[idx1][c1]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
    if (c[2] & 3) == flush:
        idx_12 = T4_1F[idx1][c2]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    else:
        idx_12 = T4_1[idx1][c2]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    if idx_00 <= idx_11 <= idx2:
        points = points00 + points11
        if points > max_points:
            max_points = points
            p = ((c[0], 0), (c[1], 1))
    if idx_00 <= idx_12 <= idx2:
        points = points00 + points12
        if points > max_points:
            max_points = points
            p = ((c[0], 0), (c[2], 1))
    if idx_01 <= idx_10 <= idx2:
        points = points01 + points10
        if points > max_points:
            max_points = points
            p = ((c[1], 0), (c[0], 1))
    if idx_01 <= idx_12 <= idx2:
        points = points01 + points12
        if points > max_points:
            max_points = points
            p = ((c[1], 0), (c[2], 1))
    if idx_02 <= idx_10 <= idx2:
        points = points02 + points10
        if points > max_points:
            max_points = points
            p = ((c[2], 0), (c[0], 1))
    if idx_02 <= idx_11 <= idx2:
        points = points02 + points11
        if points > max_points:
            max_points = points
            p = ((c[2], 0), (c[1], 1))
    return p
    
def s02(h: Hand, c: list):
    max_points = PENALTY
    c0, c1, c2 = c[0] >> 2, c[1] >> 2, c[2] >> 2
    idx0 = h.rows[0].idx >> 12
    idx1 = h.rows[1].idx
    idx2 = h.rows[2].idx >> 4
    idx_00 = T2_1[idx0][c0][0]
    idx_01 = T2_1[idx0][c1][0]
    idx_02 = T2_1[idx0][c2][0]
    points00 = HIGH_ROYALTY[idx_00 >> 8]
    points01 = HIGH_ROYALTY[idx_01 >> 8]
    points02 = HIGH_ROYALTY[idx_02 >> 8]
    if h.rows[2].flush == -1:    
        idx_20 = T4_1[idx2][c0]
        idx_21 = T4_1[idx2][c1]
        idx_22 = T4_1[idx2][c2]
        points20 = LOW_ROYALTY[idx_20 >> 16]
        points21 = LOW_ROYALTY[idx_21 >> 16]
        points22 = LOW_ROYALTY[idx_22 >> 16]
        if idx_00 <= idx1 <= idx_21:
            points = points00 + points21
            if points > max_points: max_points = points
        if idx_00 <= idx1 <= idx_22:
            points = points00 + points22
            if points > max_points: max_points = points
        if idx_01 <= idx1 <= idx_20:
            points = points01 + points20
            if points > max_points: max_points = points
        if idx_01 <= idx1 <= idx_22:
            points = points01 + points22
            if points > max_points: max_points = points
        if idx_02 <= idx1 <= idx_20:
            points = points02 + points20
            if points > max_points: max_points = points
        if idx_02 <= idx1 <= idx_21:
            points = points02 + points21
            if points > max_points: max_points = points
        return max_points + h.rows[1].points if max_points > PENALTY else PENALTY
    flush = h.rows[2].flush 
    if (c[0] & 3) == flush:
        idx_20 = T4_1F[idx2][c0]
        points20 = LOW_ROYALTY[idx_20 >> 16]
    else:
        idx_20 = T4_1[idx2][c0]
        points20 = LOW_ROYALTY[idx_20 >> 16]
    if (c[1] & 3) == flush:
        idx_21 = T4_1F[idx2][c1]
        points21 = LOW_ROYALTY[idx_21 >> 16]
    else:
        idx_21 = T4_1[idx2][c1]
        points21 = LOW_ROYALTY[idx_21 >> 16]
    if (c[2] & 3) == flush:
        idx_22 = T4_1F[idx2][c2]
        points22 = LOW_ROYALTY[idx_22 >> 16]
    else:
        idx_22 = T4_1[idx2][c2]
        points22 = LOW_ROYALTY[idx_22 >> 16]
    if idx_00 <= idx1 <= idx_21:
        points = points00 + points21
        if points > max_points: max_points = points
    if idx_00 <= idx1 <= idx_22:
        points = points00 + points22
        if points > max_points: max_points = points
    if idx_01 <= idx1 <= idx_20:
        points = points01 + points20
        if points > max_points: max_points = points
    if idx_01 <= idx1 <= idx_22:
        points = points01 + points22
        if points > max_points: max_points = points
    if idx_02 <= idx1 <= idx_20:
        points = points02 + points20
        if points > max_points: max_points = points
    if idx_02 <= idx1 <= idx_21:
        points = points02 + points21
        if points > max_points: max_points = points
    return max_points + h.rows[1].points if max_points > PENALTY else PENALTY  
def s02_(h: Hand, c: list):
    c0, c1 = c[0] >> 2, c[1] >> 2
    idx0 = h.rows[0].idx >> 12
    idx1 = h.rows[1].idx
    idx2 = h.rows[2].idx >> 4
    flush2 = h.rows[2].flush
    points1 = h.rows[1].points

    idx00 = T2_1[idx0][c0][0]
    idx01 = T2_1[idx0][c1][0]

    idx20 = T4_1[idx2][c0]
    idx21 = T4_1[idx2][c1]
    if flush2 != -1:
        if (c[0] & 3) == flush2: idx20 = T4_1F[idx2][c0]
        if (c[1] & 3) == flush2: idx21 = T4_1F[idx2][c1]
    
    if idx01 <= idx1 <= idx20:
        points0 = HIGH_ROYALTY[idx01 >> 8] + points1 + LOW_ROYALTY[idx20 >> 16]
    else: points0 = PENALTY
    if idx00 <= idx1 <= idx21:
        points2 = HIGH_ROYALTY[idx00 >> 8] + points1 + LOW_ROYALTY[idx21 >> 16]
    else: points2 = PENALTY

    return points2 if points2 > points0 else points0
def s02p(h: Hand, c: list):
    max_points = PENALTY
    p = 0
    c0, c1, c2 = c[0] >> 2, c[1] >> 2, c[2] >> 2
    idx0 = h.rows[0].idx >> 12
    idx1 = h.rows[1].idx
    idx2 = h.rows[2].idx >> 4
    idx_00 = T2_1[idx0][c0][0]
    idx_01 = T2_1[idx0][c1][0]
    idx_02 = T2_1[idx0][c2][0]
    points00 = HIGH_ROYALTY[idx_00 >> 8]
    points01 = HIGH_ROYALTY[idx_01 >> 8]
    points02 = HIGH_ROYALTY[idx_02 >> 8]
    if h.rows[2].flush == -1:    
        idx_20 = T4_1[idx2][c0]
        idx_21 = T4_1[idx2][c1]
        idx_22 = T4_1[idx2][c2]
        points20 = LOW_ROYALTY[idx_20 >> 16]
        points21 = LOW_ROYALTY[idx_21 >> 16]
        points22 = LOW_ROYALTY[idx_22 >> 16]
        if idx_00 <= idx1 <= idx_21:
            points = points00 + points21
            if points > max_points:
                max_points = points
                p = ((c[0], 0), (c[1], 2))
        if idx_00 <= idx1 <= idx_22:
            points = points00 + points22
            if points > max_points:
                max_points = points
                p = ((c[0], 0), (c[2], 2))
        if idx_01 <= idx1 <= idx_20:
            points = points01 + points20
            if points > max_points:
                max_points = points
                p = ((c[1], 0), (c[0], 2))
        if idx_01 <= idx1 <= idx_22:
            points = points01 + points22
            if points > max_points:
                max_points = points
                p = ((c[1], 0), (c[2], 2))
        if idx_02 <= idx1 <= idx_20:
            points = points02 + points20
            if points > max_points:
                max_points = points
                p = ((c[2], 0), (c[0], 2))
        if idx_02 <= idx1 <= idx_21:
            points = points02 + points21
            if points > max_points:
                max_points = points
                p = ((c[2], 0), (c[1], 2))
        return p
    flush = h.rows[2].flush 
    if (c[0] & 3) == flush:
        idx_20 = T4_1F[idx2][c0]
        points20 = LOW_ROYALTY[idx_20 >> 16]
    else:
        idx_20 = T4_1[idx2][c0]
        points20 = LOW_ROYALTY[idx_20 >> 16]
    if (c[1] & 3) == flush:
        idx_21 = T4_1F[idx2][c1]
        points21 = LOW_ROYALTY[idx_21 >> 16]
    else:
        idx_21 = T4_1[idx2][c1]
        points21 = LOW_ROYALTY[idx_21 >> 16]
    if (c[2] & 3) == flush:
        idx_22 = T4_1F[idx2][c2]
        points22 = LOW_ROYALTY[idx_22 >> 16]
    else:
        idx_22 = T4_1[idx2][c2]
        points22 = LOW_ROYALTY[idx_22 >> 16]
    if idx_00 <= idx1 <= idx_21:
        points = points00 + points21
        if points > max_points:
            max_points = points
            p = ((c[0], 0), (c[1], 2))
    if idx_00 <= idx1 <= idx_22:
        points = points00 + points22
        if points > max_points:
            max_points = points
            p = ((c[0], 0), (c[2], 2))
    if idx_01 <= idx1 <= idx_20:
        points = points01 + points20
        if points > max_points:
            max_points = points
            p = ((c[1], 0), (c[0], 2))
    if idx_01 <= idx1 <= idx_22:
        points = points01 + points22
        if points > max_points:
            max_points = points
            p = ((c[1], 0), (c[2], 2))
    if idx_02 <= idx1 <= idx_20:
        points = points02 + points20
        if points > max_points:
            max_points = points
            p = ((c[2], 0), (c[0], 2))
    if idx_02 <= idx1 <= idx_21:
        points = points02 + points21
        if points > max_points:
            max_points = points
            p = ((c[2], 0), (c[1], 2))
    return p

def s12(h: Hand, c: list):
    max_points = PENALTY
    c0, c1, c2 = c[0] >> 2, c[1] >> 2, c[2] >> 2
    idx0 = h.rows[0].idx
    idx1 = h.rows[1].idx >> 4
    idx2 = h.rows[2].idx >> 4

    if h.rows[1].flush == -1:    
        idx_10 = T4_1[idx1][c0]
        idx_11 = T4_1[idx1][c1]
        idx_12 = T4_1[idx1][c2]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    else:
        flush = h.rows[1].flush 
        if (c[0] & 3) == flush:
            idx_10 = T4_1F[idx1][c0]
            points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        else:
            idx_10 = T4_1[idx1][c0]
            points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        if (c[1] & 3) == flush:
            idx_11 = T4_1F[idx1][c1]
            points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        else:
            idx_11 = T4_1[idx1][c1]
            points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        if (c[2] & 3) == flush:
            idx_12 = T4_1F[idx1][c2]
            points12 = MIDDLE_ROYALTY[idx_12 >> 16]
        else:
            idx_12 = T4_1[idx1][c2]
            points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    if h.rows[2].flush == -1:    
        idx_20 = T4_1[idx2][c0]
        idx_21 = T4_1[idx2][c1]
        idx_22 = T4_1[idx2][c2]
        points20 = LOW_ROYALTY[idx_20 >> 16]
        points21 = LOW_ROYALTY[idx_21 >> 16]
        points22 = LOW_ROYALTY[idx_22 >> 16]
    else:
        flush = h.rows[2].flush 
        if (c[0] & 3) == flush:
            idx_20 = T4_1F[idx2][c0]
            points20 = LOW_ROYALTY[idx_20 >> 16]
        else:
            idx_20 = T4_1[idx2][c0]
            points20 = LOW_ROYALTY[idx_20 >> 16]
        if (c[1] & 3) == flush:
            idx_21 = T4_1F[idx2][c1]
            points21 = LOW_ROYALTY[idx_21 >> 16]
        else:
            idx_21 = T4_1[idx2][c1]
            points21 = LOW_ROYALTY[idx_21 >> 16]
        if (c[2] & 3) == flush:
            idx_22 = T4_1F[idx2][c2]
            points22 = LOW_ROYALTY[idx_22 >> 16]
        else:
            idx_22 = T4_1[idx2][c2]
            points22 = LOW_ROYALTY[idx_22 >> 16]

    if idx0 <= idx_10 <= idx_21:
        points = points10 + points21
        if points > max_points: max_points = points
    if idx0 <= idx_10 <= idx_22:
        points = points10 + points22
        if points > max_points: max_points = points
    if idx0 <= idx_11 <= idx_20:
        points = points11 + points20
        if points > max_points: max_points = points
    if idx0 <= idx_11 <= idx_22:
        points = points11 + points22
        if points > max_points: max_points = points
    if idx0 <= idx_12 <= idx_20:
        points = points12 + points20
        if points > max_points: max_points = points
    if idx0 <= idx_12 <= idx_21:
        points = points12 + points21
        if points > max_points: max_points = points
    return max_points + h.rows[0].points if max_points > PENALTY else PENALTY  
def s12_(h: Hand, c: list):
    c0, c1 = c[0] >> 2, c[1] >> 2
    idx0 = h.rows[0].idx
    idx1 = h.rows[1].idx >> 4
    idx2 = h.rows[2].idx >> 4
    points0 = h.rows[0].points
    flush1 = h.rows[1].flush
    flush2 = h.rows[2].flush

    idx10 = T4_1[idx1][c0]
    idx11 = T4_1[idx1][c1]
    idx20 = T4_1[idx2][c0]
    idx21 = T4_1[idx2][c1]

    if flush1 != -1:
        if (c[0] & 3) == flush1: idx10 = T4_1F[idx1][c0]
        if (c[1] & 3) == flush1: idx11 = T4_1F[idx1][c1]
    if flush2 != -1:
        if (c[0] & 3) == flush2: idx20 = T4_1F[idx2][c0]
        if (c[1] & 3) == flush2: idx21 = T4_1F[idx2][c1]

    if idx0 <= idx11 <= idx20:
        points1 = points0 + MIDDLE_ROYALTY[idx11 >> 16] + LOW_ROYALTY[idx20 >> 16]
    else: points1 = PENALTY
    if idx0 <= idx10 <= idx21:
        points2 = points0 + MIDDLE_ROYALTY[idx10 >> 16] + LOW_ROYALTY[idx21 >> 16]
    else: points2 = PENALTY

    return points2 if points2 > points1 else points1
def s12p(h: Hand, c: list):
    max_points = PENALTY
    p = 0
    c0, c1, c2 = c[0] >> 2, c[1] >> 2, c[2] >> 2
    idx0 = h.rows[0].idx
    idx1 = h.rows[1].idx >> 4
    idx2 = h.rows[2].idx >> 4

    if h.rows[1].flush == -1:    
        idx_10 = T4_1[idx1][c0]
        idx_11 = T4_1[idx1][c1]
        idx_12 = T4_1[idx1][c2]
        points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    else:
        flush = h.rows[1].flush 
        if (c[0] & 3) == flush:
            idx_10 = T4_1F[idx1][c0]
            points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        else:
            idx_10 = T4_1[idx1][c0]
            points10 = MIDDLE_ROYALTY[idx_10 >> 16]
        if (c[1] & 3) == flush:
            idx_11 = T4_1F[idx1][c1]
            points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        else:
            idx_11 = T4_1[idx1][c1]
            points11 = MIDDLE_ROYALTY[idx_11 >> 16]
        if (c[2] & 3) == flush:
            idx_12 = T4_1F[idx1][c2]
            points12 = MIDDLE_ROYALTY[idx_12 >> 16]
        else:
            idx_12 = T4_1[idx1][c2]
            points12 = MIDDLE_ROYALTY[idx_12 >> 16]
    if h.rows[2].flush == -1:    
        idx_20 = T4_1[idx2][c0]
        idx_21 = T4_1[idx2][c1]
        idx_22 = T4_1[idx2][c2]
        points20 = LOW_ROYALTY[idx_20 >> 16]
        points21 = LOW_ROYALTY[idx_21 >> 16]
        points22 = LOW_ROYALTY[idx_22 >> 16]
    else:
        flush = h.rows[2].flush 
        if (c[0] & 3) == flush:
            idx_20 = T4_1F[idx2][c0]
            points20 = LOW_ROYALTY[idx_20 >> 16]
        else:
            idx_20 = T4_1[idx2][c0]
            points20 = LOW_ROYALTY[idx_20 >> 16]
        if (c[1] & 3) == flush:
            idx_21 = T4_1F[idx2][c1]
            points21 = LOW_ROYALTY[idx_21 >> 16]
        else:
            idx_21 = T4_1[idx2][c1]
            points21 = LOW_ROYALTY[idx_21 >> 16]
        if (c[2] & 3) == flush:
            idx_22 = T4_1F[idx2][c2]
            points22 = LOW_ROYALTY[idx_22 >> 16]
        else:
            idx_22 = T4_1[idx2][c2]
            points22 = LOW_ROYALTY[idx_22 >> 16]

    if idx0 <= idx_10 <= idx_21:
        points = points10 + points21
        if points > max_points:
            max_points = points
            p = ((c[0], 1), (c[1], 2))
    if idx0 <= idx_10 <= idx_22:
        points = points10 + points22
        if points > max_points:
            max_points = points
            p = ((c[0], 1), (c[2], 2))
    if idx0 <= idx_11 <= idx_20:
        points = points11 + points20
        if points > max_points:
            max_points = points
            p = ((c[1], 1), (c[0], 2))
    if idx0 <= idx_11 <= idx_22:
        points = points11 + points22
        if points > max_points:
            max_points = points
            p = ((c[1], 1), (c[2], 2))
    if idx0 <= idx_12 <= idx_20:
        points = points12 + points20
        if points > max_points:
            max_points = points
            p = ((c[2], 1), (c[0], 2))
    if idx0 <= idx_12 <= idx_21:
        points = points12 + points21
        if points > max_points:
            max_points = points
            p = ((c[2], 1), (c[1], 2))
    return p  

def s4p(h: Hand, c: list):
    if h.rows[0].cells == 2: return s00p(h, c)
    if h.rows[1].cells == 2: return s11p(h, c)
    if h.rows[2].cells == 2: return s22p(h, c)
    if h.rows[0].cells and h.rows[1].cells: return s01p(h, c)
    if h.rows[0].cells and h.rows[2].cells: return s02p(h, c)
    return s12p(h, c)     
