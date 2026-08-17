from itertools import product
from timeit import timeit
from datetime import datetime as dt

LUT3_5 = None
def c3_5(c: tuple, d: tuple) -> tuple:
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

def lut3_5():
    global C_IND, C_VAL, LUT3_5
    C_IND = {}
    C_VAL = []
    idx = 0
    for d0 in range(12, -1, -1):
        for d1 in range(d0, -1, -1):
            for d2 in range(d1, -1, -1):
                t = (d0, d1, d2)
                C_IND[t] = idx
                C_VAL.append(t)
                idx += 1

    LUT3_5 = []
    for c in C_VAL:
        row = []
        for d in C_VAL:
            row.append(c3_5(c, d))
        LUT3_5.append(row)

start = dt.now()
lut3_5() 
print(f'sorted time {(dt.now() - start).total_seconds()}')
def lut3_5_unsorted():
    global LUT3
    LUT3 = [[0] * 2197 for _ in range(2197)]

    triples = [
    tuple(sorted((r0, r1, r2), reverse=True))
    for r0, r1, r2 in product(range(13), repeat=3)
    ]
    start = dt.now()
    for idx0, c in enumerate(triples):
        for idx1, d in enumerate(triples):
            LUT3[idx0][idx1] = c3_5(c, d)
    print(f'time {(dt.now() - start).total_seconds()}')
lut3_5_unsorted()





