from tables import *

def s22_(h: Hand, c: list):
    idx = T3_2[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2]
    if h.rows[2].flush != -1:
        if (c[0] & 3) == (c[1] & 3) == h.rows[2].flush:
            idx = T3_2F[h.rows[2].idx >> 8][c[0] >> 2][c[1] >> 2]
    if idx >= h.rows[1].idx:
        if idx == 0x8c0000: return 25 + h.rows[0].points + h.rows[1].points
        return LOW_ROW_ROYALTY[idx >> 20] + h.rows[0].points + h.rows[1].points
    return PENALTY

