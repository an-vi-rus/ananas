from itertools import product, combinations

from combo import *

def empty_table(m, n):
    return [[0] * n for _ in range(m)]

def t4():
    idx4 = [combo4(c)[0] >> 4 for c in product(range(13), repeat=4)]
    t = empty_table(0x8C001, 13)
    for idx in idx4:
        for rank in range(13):
            t[idx][rank] = next5(idx, rank)
    return t
T4_1 = t4()
def t4f():
    idx4f = [combo4f(c)[0] >> 4 for c in combinations(range(13), 4)]
    t = empty_table(0x8C001, 13)
    for idx in idx4f:
        for rank in range(13):
            t[idx][rank] = next5f(idx, rank)
    return t
T4_1F = t4f()
def t4_2():
    pass
def t4_2f():
    pass
def t3():
    idx3 = [combo3(c)[0] >> 8 for c in product(range(13), repeat=3)]
    t = empty_table(0x3CC1, 13)
    for idx in idx3:
        for rank in range(13):
            t[idx][rank] = next4(idx, rank)
    return t
T3_1 = t3()
def t3f():
    idx3f = [combo3f(c)[0] >> 8 for c in combinations(range(13), 3)]
    t = [[None] * 13 for _ in range(0xCBB)]
    for idx in idx3f:
        for rank in range(13):
            t[idx][rank] = next4f(idx, rank)
    return t
T3_1F = t3f()
def t3_2():
    idx3 = [combo3(c)[0] >> 8 for c in product(range(13), repeat=3)]
    t = [[[None] * 13 for _ in range(13)] for _ in range(0x3C01)]
    for idx in idx3:
        for c0 in range(13):
            idx4, _ = T3_1[idx][c0]
            for c1 in range(13):
                t[idx][c0][c1] = T4_1[idx4 >> 4][c1]
    return t
T3_2 = t3_2()
def t3_2f():
    idx3f = [combo3f(c)[0] >> 8 for c in combinations(range(13), 3)]
    t = [[[None] * 13 for _ in range(13)] for _ in range(0xCBB)]
    for idx in idx3f:
        for c0 in range(13):
            idx4, _ = T3_1F[idx][c0]
            for c1 in range(13):
                t[idx][c0][c1] = T4_1F[idx4 >> 4][c1]
    return t
T3_2F = t3_2f()
def t3_3():
    idx3 = [combo3(c)[0] >> 8 for c in product(range(13), repeat=3)]
    t = [[[[None] * 13 for _ in range(13)] for _ in range(13)] for _ in range(0x3C01)]
    for idx in idx3:
        for c in product(range(13), repeat=3):
            c0 = T3_2[idx][c[1]][c[2]]
            c1 = T3_2[idx][c[0]][c[2]]
            c2 = T3_2[idx][c[0]][c[1]]
            t[idx][c[0]][c[1]][c[2]] = sorted((c0, c1, c2), reverse=True)
    return t
T3_3 = t3_3()
def t3_3f():
    idx3f = [combo3f(c)[0] >> 8 for c in combinations(range(13), 3)]
    t = [[[[None] * 13 for _ in range(13)] for _ in range(13)] for _ in range(0xCBB)]
    for idx in idx3f:
        for c in combinations(range(13), 3):
            c0 = T3_2F[idx][c[1]][c[2]]
            c1 = T3_2F[idx][c[0]][c[2]]
            c2 = T3_2F[idx][c[0]][c[1]]
            if c0 and c1 and c2:
                t[idx][c[0]][c[1]][c[2]] = sorted((c0, c1, c2), reverse=True)
    return t
T3_3F = t3_3f()
def t2():
    idx2 = [combo2(c)[0] >> 12 for c in product(range(13), repeat=2)]
    t = empty_table(0x1CD, 13)
    for idx in idx2:
        for rank in range(13):
            t[idx][rank] = next3(idx, rank)
    return t
T2_1 = t2()
def t2f():
    idx2f = [combo2f(c)[0] >> 12 for c in combinations(range(13), 2)]
    t = empty_table(0x1CD, 13)
    for idx in idx2f:
        for rank in range(13):
            t[idx][rank] = next3f(idx, rank)
    return t
T2_1F = t2f()
def t1_2():
    t = [[[None] * 13 for _ in range(13)] for _ in range(13)]
    for c in product(range(13), repeat=3):
        t[c[0]][c[1]][c[2]], _ = combo3(c)
    return t
T1_2 = t1_2()
def t1_3():
    t = [[[[None] * 13 for _ in range(13)] for _ in range(13)] for _ in range(13)]
    for c in product(range(13), repeat=4):
        c1 = T1_2[c[0]][c[2]][c[3]]
        c2 = T1_2[c[0]][c[1]][c[3]]
        c3 = T1_2[c[0]][c[1]][c[2]]
        t[c[0]][c[1]][c[2]][c[3]] = sorted((c1, c2, c3), reverse=True)
    return t
T1_3 = t1_3() 


T1_1 = [[combo2((r, c)) for c in range(13)] for r in range(13)]
T1_1F = [[combo2f((r, c)) for c in range(13)] for r in range(13)]


