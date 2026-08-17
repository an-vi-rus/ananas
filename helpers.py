
def r_size(kind, cells):
    if kind == 7: return 1
    if kind == 6: return 2
    if kind == 3: return 1 if cells == 0 else 4 - cells
    if kind == 2: return 3 - cells
    if kind == 1: return 4 - cells
    if kind in (4, 5, 8): return 5
    return 5 - cells

def pack(*combo):
    shift = 20
    v = 0
    for x in combo:
        v |= x << shift
        shift -= 4
    return v

def unpack(idx, cells):
    r = (idx >> 20) & 0xF
    combo = [r]
    for i in range(r_size(r, cells)):
        combo.append((idx >> (16 - 4 * i)) & 0xF)
    return combo

