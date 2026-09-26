import random

def test_deck(n, seed):
    deck = list(range(52))
    if seed >= 0: random.seed(seed)
    else: random.seed()
    random.shuffle(deck)
    tmp = deck [n - 52:]
    random.seed()
    random.shuffle(tmp)
    deck[n-52:] = tmp
    return deck

p = ((51, 2), (50, 2), (48, 2), (49, 2), (20, 1))

def s0deck():
    deck = list(range(52))
    result = []
    for pair in p:
        deck.remove(pair[0])
        result.append(pair[0])
    random.shuffle(deck)
    result.extend(deck)
    return result

def decki_j(i, j):
    random.seed(j)
    deck = list(range(52))
    random.shuffle(deck)
    sample = deck[:i]
    for item in sample: deck.remove(item)
    sample.extend(deck)
    return sample[:]
