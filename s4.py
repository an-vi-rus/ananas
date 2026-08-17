from lut import LUT3_5, C_IND

penalty = -6
premium = 6
def s22_c(c: tuple, deal):
    d = 
    if c[0] == 0: return LUT3_5[C_IND[c[1]]][C_IND[]

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