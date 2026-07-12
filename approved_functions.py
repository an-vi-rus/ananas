from aux import holdem, texas, omaha, to_hysto, round_list, show_cards
import random
from datetime import datetime

random.seed()

def holdem_flop(hand: list, flop: list) -> dict[str,list]:
    deck = list(range(52))
    for item in hand+flop: deck.remove(item)
    l = len(deck)
    num = round(l*(l-1)/2)
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    ind = 0
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            river = [deck[i1],deck[i2]]
            table = flop+river
            my_combo = holdem(hand+table)
            my_comb[my_combo[0]] += 100 / num
            d = deck[:]
            for item in river: d.remove(item)
            for _ in range(100): 
                op_hand = random.sample(d,2)
                op_combo = holdem(op_hand+table)
                op_comb[op_combo[0]] += 1 / num
                if op_combo <= my_combo: my_hyst[ind] += 1
                if my_combo <= op_combo: op_hyst[ind] += 1
            ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result

def holdem_turn(hand: list, turn: list) -> dict[str,list]:
    deck = list(range(52))
    for item in hand+turn: deck.remove(item)
    l = len(deck)
    num = round((l-1)*(l-2)/2)
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    for i1 in range(l):
        table = turn + [deck[i1]]
        my_combo = holdem(hand+table)
        my_comb[my_combo[0]] += 100 / l
        d = deck[:]
        d.pop(i1)
        ind = 0
        for i2 in range(l-2):
            for i3 in range(i2+1,l-1):
                op_hand = [d[i2],d[i3]]
                op_combo = holdem(op_hand+table)
                op_comb[op_combo[0]] += 100 / (l*num)
                if op_combo <= my_combo: my_hyst[ind] += 100 / l
                if my_combo <= op_combo: op_hyst[ind] += 100 / l
                ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result 

def holdem_river(hand: list, table: list) -> dict[str]:
    deck = list(range(52))
    for item in hand+table: deck.remove(item)
    l = len(deck)
    num = round(l*(l-1)/2)
    my_comb, op_comb = [0] * 9, [0] * 9 
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    my_combo = holdem(hand+table)
    my_comb[my_combo[0]] += 100
    ind = 0
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            op_hand = [deck[i1],deck[i2]]
            op_combo = holdem(op_hand+table)
            op_comb[op_combo[0]] += 100 / num
            if op_combo <= my_combo: my_hyst[ind] += 100
            if my_combo <= op_combo: op_hyst[ind] += 100
            ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
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
            my_comb[my_combo[0]] += 100 / num1
            d = deck[:]
            for item in river: d.remove(item)
            l2 = len(d)
            num2 = round(l2 * (l2-1) / 2)
            for i3 in range(l2-1):
                for i4 in range(i3+1,l2):
                    op_hand = [d[i3],d[i4]]
                    op_combo = texas(op_hand + table)
                    op_comb[op_combo[0]] += 100 / (num1*num2)
                    if op_combo <= my_combo: my_hyst[ind] += 100 / num2
                    if my_combo <= op_combo: op_hyst[ind] += 100 / num2
            ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst, 100)
    result['op_hysto'] = to_hysto(op_hyst, 100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result

def texas_turn(hand: list, turn: list) -> dict[str,list]:
    deck = list(range(16,52))
    for item in hand+turn: deck.remove(item)
    l = len(deck)
    num = round((l-1)*(l-2)/2)
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    for i1 in range(l):
        table = turn + [deck[i1]]
        my_combo = texas(hand+table)
        my_comb[my_combo[0]] += 100 / l
        d = deck[:]
        d.pop(i1)
        ind = 0
        for i2 in range(l-2):
            for i3 in range(i2+1,l-1):
                op_hand = [d[i2],d[i3]]
                op_combo = texas(op_hand+table)
                op_comb[op_combo[0]] += 100 / (l*num)
                if op_combo <= my_combo: my_hyst[ind] += 100 / l
                if my_combo <= op_combo: op_hyst[ind] += 100 / l
                ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result

def texas_river(hand: list, table: list) -> dict[str]:
    deck = list(range(16,52))
    for item in hand+table: deck.remove(item)
    l = len(deck)
    num = round(l*(l-1)/2)
    my_comb, op_comb = [0] * 9, [0] * 9 
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    my_combo = texas(hand+table)
    my_comb[my_combo[0]] += 100
    ind = 0
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            op_hand = [deck[i1],deck[i2]]
            op_combo = texas(op_hand+table)
            op_comb[op_combo[0]] += 100 / num
            if op_combo <= my_combo: my_hyst[ind] += 100
            if my_combo <= op_combo: op_hyst[ind] += 100
            ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result

def omaha_preflop(hand: list) -> dict[str,list]:
    hand_size = len(hand)
    deck = list(range(52))
    for item in hand: deck.remove(item)
    l = len(deck)
    num = 200
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    for i in range(num):
        flop = random.sample(deck,3)
        d = deck[:]
        for item in flop: d.remove(item)
        for _ in range(num):
            sample = random.sample(d,hand_size+2)
            table = flop+sample[0:2]
            op_hand = sample[2:]
            my_combo = omaha(hand,table)
            my_comb[my_combo[0]] += 100 / (num*num)
            op_combo = omaha(op_hand,table)
            op_comb[op_combo[0]] += 100 / (num*num)
            if op_combo <= my_combo: my_hyst[i] += 100 / num
            if my_combo <= op_combo: op_hyst[i] += 100 / num
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result        

def omaha_flop(hand: list, flop: list) -> dict[str,list]:
    hand_size = len(hand)
    deck = list(range(52))
    for item in hand+flop: deck.remove(item)
    l = len(deck)
    num = round(l*(l-1)/2)
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    ind = 0
    for i1 in range(l-1):
        for i2 in range(i1+1,l):
            river = [deck[i1],deck[i2]]
            table = flop+river
            my_combo = omaha(hand,table)
            my_comb[my_combo[0]] += 100 / num
            d = deck[:]
            for item in river: d.remove(item)
            for _ in range(100): 
                op_hand = random.sample(d,hand_size)
                op_combo = omaha(op_hand,table)
                op_comb[op_combo[0]] += 1 / num
                if op_combo <= my_combo: my_hyst[ind] += 1
                if my_combo <= op_combo: op_hyst[ind] += 1
            ind += 1
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result 

def omaha_turn(hand: list, turn: list) -> dict[str,list]:
    hand_size = len(hand)
    deck = list(range(52))
    for item in hand+turn: deck.remove(item)
    l = len(deck)
    num = 1000
    my_comb, op_comb = [0] * 9, [0] * 9
    my_hyst, op_hyst = [0] * num, [0] * num
    result = {}
    for i1 in range(l):
        table = turn + [deck[i1]]
        my_combo = omaha(hand,table)
        my_comb[my_combo[0]] += 100 / (l*num)
        d = deck[:]
        d.pop(i1)
        for i2 in range(num):
            op_hand = random.sample(d,hand_size)
            op_combo = omaha(op_hand,table)
            op_comb[op_combo[0]] += 1 / num
            if op_combo <= my_combo: my_hyst[i2] += 100 / l
            if my_combo <= op_combo: op_hyst[i2] += 100 / l
    my_hyst.sort(reverse=True)
    op_hyst.sort(reverse=True)
    result['my_hysto'] = to_hysto(my_hyst,100)
    result['op_hysto'] = to_hysto(op_hyst,100)
    result['my_combo'] = my_comb
    result['op_combo'] = op_comb
    return result 

def omaha_river(hand: list, table: list) -> dict[str]:
    hand_size = len(hand)
    deck = list(range(52))
    for item in hand+table: deck.remove(item)
    num = 10000
    op_comb = [0] * 9
    my_wins, op_wins = 0, 0
    result = {'my_combo': omaha(hand,table)}
    for i in range(num):
        op_hand = random.sample(deck,hand_size)
        op_combo = omaha(op_hand,table)
        op_comb[op_combo[0]] += 100 / num
        if op_combo <= my_combo: my_wins += 100 / num
        if my_combo <= op_combo: op_wins += 100 / num
    
    result['my_wins'] = my_wins
    result['op_wins'] = op_wins
    result['op_combo'] = op_comb
    return result   



