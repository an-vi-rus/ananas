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

