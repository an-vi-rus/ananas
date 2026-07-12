from aux import show_cards, to_key, from_matrix, holdem, texas, omaha
import random
from datetime import datetime
from collections import Counter

random.seed()
deck = list(range(52))

def to_hysto(hysto: list, size: int) -> list[float]:
    l = len(hysto)
    q = l / size
    result = [0] * size
    for i in range(size):
        r1, r2 = int(i*q), int((i+1)*q)
        result[i] = round(sum(hysto[r1:r2])/(r2-r1),1)
    return result


def permute_hand(cards: list, cards_permutation: dict) -> tuple[list,dict]:
    sorted_cards = sorted(cards, reverse=True)
    permutation = cards_permutation.copy()
    ranks, suits = [13], [[]]

    for item in sorted_cards:
        if item // 4 == ranks[-1]:
            suits[-1].append(item % 4)
        else:
            if suits[-1]: 
                suits.append([])
            ranks.append(item // 4)
            suits[-1].append(item % 4) 
    for item in suits:
        if len(permutation) == 4: break
        cards_suits, permuted = set(item), set(permutation)
        cards_suits -= permuted
        if cards_suits:
            if len(cards_suits) > 1:
                suitcards = {}
                for i in cards_suits:
                    suitcards[i] = [x // 4 for x in sorted_cards if x % 4 == i]
                suitcards = sorted(suitcards.items(),reverse=True,key=lambda x: (x[1],3-x[0]))
                for i in suitcards: permutation[i[0]] = len(permutation)
            else: permutation[cards_suits.pop()] = len(permutation)

    permuted_cards = [item - item % 4 + permutation[item % 4] for item in sorted_cards]
    permuted_cards.sort(reverse=True, key=lambda x: (x // 4, 3 - x % 4))
    return (permuted_cards, permutation)

def permute_hands(cards1: list, cards2: list, cards_permutation: dict) -> tuple[list,list,dict]:
    result1 = permute_hand(cards1,cards_permutation)
    result2 = permute_hand(cards2, result1[1])
    return(result1[0],result2[0],result2[1])

def flops(hand: list) -> Counter:
    deck = list(range(52))
    for item in hand: deck.remove(item)
    h = permute_hand(hand, {})
    flops = []
    initial = h[1]
    l = len(deck)
    for i1 in range(l-2):
        for i2 in range(i1+1, l-1):
            for i3 in range(i2+1,l):
                flop = [deck[i1],deck[i2],deck[i3]]
                result = permute_hand(flop,initial)
                value = to_key(result[0])
                flops.append(value)
    return Counter(flops)

def flops_data() -> dict[str,Counter]:
    data = {}
    for i1 in range(13):
        for i2 in range(13):
            hand = from_matrix([i1,i2])
            key = to_key(hand)
            data[key] = flops(hand)
    return data
    
def preflop_stats(hand) -> list[list,list]:



    pass

def flop_full_stats(hand: list, flop: list) -> dict[str,list]:
    deck = list(range(52))
    for item in hand+flop: deck.remove(item)
    l = len(deck)
    num1, num2 = l*(l-1) // 2, (l-2)*(l-3) // 2
    my_combos, op_combos = [0] * 10, [0] * 10
    my_hyst, op_hyst = [], []
    result = {}
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            river = [deck[i1],deck[i2]] 
            table = flop + river
            d = deck[:]
            for item in river: d.remove(item)
            my_combo = holdem(hand+table)
            my_combos[my_combo[0]] += 100 / num1
            table_combo = holdem(table)
            my_wins, op_wins = 0, 0
            for i3 in range(l-3):
                for i4 in range(i3+1,l-2):
                    op_hand = [d[i3], d[i4]]
                    op_combo = holdem(op_hand+table)
                    op_combos[op_combo[0]] += 100 / (num1 * num2)
                    if op_combo <= my_combo and table_combo < my_combo:
                        my_wins += 100 / num2
                        my_combos[9] += 100 / (num1 * num2)
                    else:
                        op_wins += 100 / num2
                        op_combos[9] += 100 / (num1 * num2)
            my_hyst.append(my_wins)
            op_hyst.append(op_wins)
    print(num1,num2)
    


    for i in range(10): 
        my_combos[i] = round(my_combos[i], 1)
        op_combos[i] = round(op_combos[i], 1)
    result['my_combo'] = my_combos
    result['op_combo'] = op_combos
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    q = num1 / 100
    my_hysto, op_hysto = [], []
    for i in range(100):
        r1, r2 = int(i*q), int((i+1)*q)
        my_hysto.append(round(sum(my_hyst[r1:r2])/(r2-r1),1))
        op_hysto.append(round(sum(op_hyst[r1:r2])/(r2-r1),1))
    result['my_hysto'] = my_hysto
    result['op_hysto'] = op_hysto
    return result


def holdem_flop(hand: list, flop: list) -> dict[str,list]:
    start_time = datetime.now()
    deck = list(range(52))
    for item in hand+flop: deck.remove(item)
    l = len(deck)
    num = l*(l-1)/2
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * 100, [0] * 100
    result = {}
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            river = [deck[i1],deck[i2]]
            table = flop+river
            my_combo = holdem(hand+table)
            table_combo = holdem(table)
            my_comb[my_combo[0]] += 100 / num
            d = deck[:]
            for item in river: d.remove(item)
            for i3 in range(100): 
                op_hand = random.sample(d,2)
                op_combo = holdem(op_hand+table)
                op_comb[op_combo[0]] += 1 / num
                if op_combo <= my_combo and table_combo < my_combo: my_hyst[i3] += 1 / num
                if my_combo <= op_combo and table_combo < op_combo: op_hyst[i3] += 1 / num
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    result['my_hysto'] = my_hyst
    result['op_hysto'] = op_hyst
    print('elapsed time', (datetime.now()-start_time).total_seconds(), sum(my_hyst),sum(op_hyst))
    return result 

def texas_flop_(hand: list, flop: list) -> dict[str,list]:
    deck = list(range(16,52))
    for item in hand+flop: deck.remove(item)
    l = len(deck)
    num = l*(l-1)/2
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * 100, [0] * 100
    result = {}
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            river = [deck[i1],deck[i2]]
            table = flop+river
            my_combo = texas(hand+table)
            table_combo = texas(table)
            my_comb[my_combo[0]] += 100 / num
            d = deck[:]
            for item in river: d.remove(item)
            for i3 in range(100): 
                op_hand = random.sample(d,2)
                op_combo = texas(op_hand+table)
                op_comb[0] += 1 / num
                if op_combo <= my_combo and table_combo < my_combo: my_hyst[i3] += 1 / num
                if my_combo <= op_combo and table_combo < op_combo: op_hyst[i3] += 1 / num
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    result['my_hysto'] = my_hyst
    result['op_hysto'] = op_hyst
    print(sum(my_hyst)+sum(op_hyst))
    return result  

def texas_flop(hand: list, flop: list) -> dict[str,list]:
    deck = list(range(16,52))
    for item in hand+flop: deck.remove(item)
    l1 = len(deck)
    num1 = round(l1*(l1-1)/2)
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num1, [0] * num1
    result = {}
    ind = 0
    for i1 in range(l1-1):
        for i2 in range(i1+1,l1):
            river = [deck[i1],deck[i2]]
            table = flop+river
            my_combo = texas(hand+table)
            table_combo = texas(table)
            my_comb[0] += 100 / num1
            d = deck[:]
            for item in river: d.remove(item)
            l2 = len(d)
            num2 = num1 * l2 * (l2-1) / 2
            for i3 in range(l2-1):
                for i4 in range(i3+1,l2):
                    op_hand = [d[i3],d[i4]]
                    op_combo = texas(op_hand + table)
                    op_comb[op_combo[0]] += 100 / num2
                    if op_combo <= my_combo and table_combo < my_combo: my_hyst[ind] += 100 / num2
                    if my_combo <= op_combo and table_combo < op_combo: op_hyst[ind] += 100 / num2
            ind += 1

    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst, 100)
    result['op_hysto'] = to_hysto(op_hyst, 100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb

    return result

def omaha_flop(hand: list, flop: list) -> dict[str,list]:
    hand_size = len(hand)
    deck = list(range(52))
    for item in hand+flop: deck.remove(item)
    l = len(deck)
    num = l*(l-1)/2
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * 100, [0] * 100
    result = {}
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            river = [deck[i1],deck[i2]]
            table = flop+river
            my_combo = omaha(hand,table)
            my_comb[my_combo[0]] += 100 / num
            d = deck[:]
            for item in river: d.remove(item)
            for i3 in range(100): 
                op_hand = random.sample(d,hand_size)
                op_combo = omaha(op_hand,table)
                op_comb[op_combo[0]] += 1 / num
                if op_combo <= my_combo: my_hyst[i3] += 1 / num
                if my_combo <= op_combo: op_hyst[i3] += 1 / num
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    print(show_cards(hand),show_cards(flop),my_comb,op_comb)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    result['my_hysto'] = my_hyst
    result['op_hysto'] = op_hyst
    return result 

sample = random.sample(deck,10)
flop = sample[0:3]
hand = sample[3:]
omaha_flop(hand,flop)








