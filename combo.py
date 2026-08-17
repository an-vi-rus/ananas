from collections import Counter
from helpers import pack

def combo5(c: tuple) -> int:
    m = sorted(c, reverse=True)
    r = Counter(m).most_common()
    if r[0][0] == 0: return 0
    if r[0][1] == 4: return pack(7, r[0][0])
    if r[0][1] == 3: return pack(6, r[0][0], r[1][0]) if r[1][1] == 2 else pack(3, r[0][0])
    if r[0][1] == 2: return pack(2, r[0][0], r[1][0], r[2][0]) if r[1][1] == 2 else pack(1, r[0][0], r[1][0], r[2][0], r[3][0])
    if r[0][0] - r[4][0] == 4: return pack(4, r[0][0])
    if r[0][0] == 12 and r[1][0] == 3: return pack(4, 3)
    return pack(0, m[0], m[1], m[2], m[3], m[4])

def combo5f(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    if m[0] - m[4] == 4: return pack(8, m[0])
    if m[0] == 12 and m[1] == 3: return pack(8, 3)
    return pack(5, m[0], m[1], m[2], m[3], m[4])

def combo4(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    r = Counter(m).most_common()
    if r[0][1] == 4: return (pack(7, r[0][0]), pack(7, r[0][0]))
    if r[0][1] == 3: return (pack(3, r[0][0], r[1][0]), pack(7, r[0][0]))
    if r[0][1] == 2:
        if r[1][1] == 2: return (pack(2, r[0][0], r[1][0]), pack(6, r[0][0], r[1][0]))
        return (pack(1, r[0][0], r[1][0], r[2][0]), pack(3, r[0][0], 12, 12))
    if m[0] - m[3] <= 4:
        return (pack(0, m[0], m[1], m[2], m[3]), pack(4, min(12, m[3] + 4)))
    if m[0] == 12 and m[1] <= 3:
        return (pack(0, m[0], m[1], m[2], m[3]), pack(4, 3))
    return (pack(0, m[0], m[1], m[2], m[3]), pack(1, m[0], m[1], m[2], m[3]))

def combo4f(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    if m[0] - m[3] <= 4:
        return (pack(0, m[0], m[1], m[2], m[3]), pack(8, min(12, m[3] + 4)))
    if m[0] == 12 and m[1] <= 3:
        return (pack(0, m[0], m[1], m[2], m[3]), pack(8, 3))
    return (pack(0, m[0], m[1], m[2], m[3]), pack(5, 12, 12))

def combo3(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    r = Counter(m).most_common()
    if r[0][1] == 3: return (pack(3, r[0][0]), pack(7, r[0][0]))
    if r[0][1] == 2: return (pack(1, r[0][0], r[1][0]), pack(7, r[0][0]))
    if m[0] - m [2] <= 4:
        return (pack(0, m[0], m[1], m[2]), pack(4, min(12, m[2] + 4)))
    if m[0] == 12 and m[1] <= 3:
        return (pack(0, m[0], m[1], m[2]), pack(4, 3))
    return (pack(0, m[0], m[1], m[2]), pack(3, m[0], 12, 12))

def combo3f(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    if m[0] - m[2] <= 4:
        return (pack(0, m[0], m[1], m[2]), pack(8, min(12, m[2] + 4)))
    if m[0] == 12 and m[1] <= 3:
        return (pack(0, m[0], m[1], m[2]), pack(8, 3))
    return (pack(0, m[0], m[1], m[2]), pack(5, 12, 12))

def combo2(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    if m[0] == m[1]: return (pack(1, m[0]), pack(7, m[0]))
    return (pack(0, m[0], m[1]), pack(7, m[0]))

def combo2f(c: tuple) -> tuple:
    m = sorted(c, reverse=True)
    if m[0] - m[1] <=4:
        return (pack(0, m[0], m[1]), pack(8, min(12, m[1] + 4)))
    if m[0] == 12 and m[1] <= 3:
        return (pack(0, m[0], m[1]), pack(8, 3))
    return (pack(0, m[0], m[1]), pack(7, m[0]))

def next5(idx4, rank):
    kind = idx4 >> 16
    if kind == 7:
        return idx4 << 4
    rank0 = (idx4 >> 12) & 0xf
    rank1 = (idx4 >> 8) & 0xf
    if kind == 3:
        if rank == rank0:
            return pack(7, rank)
        if rank == rank1:
            return pack(6, rank0, rank1)
        return pack(3, rank0)
    if kind == 2:
        if rank == rank0:
            return pack(6, rank0, rank1)
        if rank == rank1:
            return pack(6, rank1, rank0)
        return pack(2, rank0, rank1, rank)
    rank2 = (idx4 >> 4) & 0xf
    if kind == 1:
        if rank == rank0:
            return pack(3, rank0)
        if rank == rank1:
            if rank0 > rank1:
                return pack(2, rank0, rank1, rank2)
            return pack(2, rank1, rank0, rank2)
        if rank == rank2:
            if rank0 > rank2:
                return pack(2, rank0, rank2, rank1)
            return pack(2, rank2, rank0, rank1)
        if rank > rank1:
            return pack(1, rank0, rank, rank1, rank2)
        if rank > rank2:
            return pack(1, rank0, rank1, rank, rank2)
        return pack(1, rank0, rank1, rank2, rank)
    rank3 = idx4 & 0xf
    l = [rank0, rank1, rank2, rank3]
    if rank in l:
        l.remove(rank)
        return pack(1, rank, *l)
    s = sorted((rank, rank0, rank1, rank2, rank3), reverse=True)
    if s[0] - s[4] == 4: return pack(4, s[0])
    if s[0] == 12 and s[1] == 3: return pack(4, 3)
    return pack(0, *s)

def next5f(idx4, rank):
    rank0 = (idx4 >> 12) & 0xF
    rank1 = (idx4 >> 8) & 0xF
    rank2 = (idx4 >> 4) & 0xf
    rank3 = idx4 & 0xf
    l = [rank0, rank1, rank2, rank3]
    if rank in l:
        l.remove(rank)
        return pack(1, rank, *l)
    s = sorted((rank, rank0, rank1, rank2, rank3), reverse=True)
    if s[0] - s[4] == 4: return pack(8, s[0])
    if s[0] == 12 and s[1] == 3: return pack(8, 3)
    return pack(5, *s)

def next4(idx3, rank):
    kind = idx3 >> 12
    rank0 = (idx3 >> 8) & 0xf
    if kind == 3:
        if rank == rank0:
            return pack(7, rank), pack(7, rank)
        return pack(3, rank0, rank), pack(7, rank0)
    rank1 = (idx3 >> 4) & 0xf
    if kind == 1:
        if rank == rank0:
            return pack(3, rank0, rank1), pack(7, rank0)
        if rank == rank1:
            if rank0 > rank1:
                return pack(2, rank0, rank1), pack(6, rank0, rank1)
            return pack(2, rank1, rank0), pack(6, rank1, rank0)
        if rank > rank1:
            return pack(1, rank0, rank, rank1), pack(3, rank0, 12, 12)
        return pack(1, rank0, rank1, rank), pack(3, rank0, 12, 12)
    rank2 = idx3 & 0xf
    l = [rank0, rank1, rank2]
    if rank in l:
        l.remove(rank)
        return pack(1, rank, *l), pack(3, rank, 12, 12)
    s = sorted((rank, rank0, rank1, rank2), reverse=True)
    if s[0] - s[3] <= 4: return pack(0, *s), pack(4, min(12, s[3] + 4))
    if s[0] == 12 and s[1] <= 3: return pack(0, *s), pack(4, 3)
    return pack(0, *s), pack(1, s[0], 12, 12, 12) 

def next4f(idx4, rank):
    rank0 = (idx4 >> 8) & 0xF
    rank1 = (idx4 >> 4) & 0xF
    rank2 = idx4 & 0xf
    l = [rank0, rank1, rank2]
    if rank in l:
        l.remove(rank)
        return pack(1, rank, *l), pack(3, rank, 12, 12)
    s = sorted((rank, rank0, rank1, rank2), reverse=True)
    if s[0] - s[3] <= 4: return pack(0, *s), pack(8, min(s[3] + 4, 12))
    if s[0] == 12 and s[1] <= 3: return pack(0, *s), pack(8, 3)
    return pack(0, *s), pack(5, 12, 12) 

def next3(idx2, rank):
    kind = idx2 >> 8
    rank0 = (idx2 >> 4) & 0xf
    if kind == 1:
        if rank == rank0:
            return pack(3, rank0), pack(7, rank0)
        return pack(1, rank0, rank), pack(7, rank0)
    rank1 = idx2 & 0xf
    if rank == rank0:
        return pack(1, rank, rank1), pack(7, rank)
    if rank == rank1:
        return pack(1, rank, rank0), pack(7, rank)
    l = sorted((rank, rank0, rank1), reverse=True)
    return pack(0, *l), pack(3, l[0], 12, 12)

def next3f(idx2, rank):
    rank0 = (idx2 >> 4) & 0xF
    rank1 = idx2 & 0xF
    l = [rank0, rank1]
    if rank in l:
        l.remove(rank)
        return pack(1, rank, *l), pack(7, rank)
    s = sorted((rank, rank0, rank1), reverse=True)
    if s[0] - s[2] <= 4: return pack(0, *s), pack(8, min(s[2] + 4, 12))
    if s[0] == 12 and s[1] <= 3: return pack(0, *s), pack(8, 3)
    return pack(0, *s), pack(5, 12, 12)     



 