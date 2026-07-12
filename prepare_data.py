import random, json, numpy as np
from datetime import datetime
from aux import from_matrix, texas, omaha, show_cards
from collections import Counter, defaultdict

random.seed()
deck = list(range(52))
 
def texas_data():
    num1, num2 = 1000, 1000
    hystogram = np.full((9,9),0).tolist()
    combos = np.full((9,9), 0.0).tolist()
    start_time = datetime.now()
    for i1 in range(9):
        for i2 in range(9):
            my_hand = aux.from_matrix([i1,i2])
            print(my_hand, round((datetime.now() - start_time).total_seconds(),2))
            deck = list(range(16,52))
            for item in my_hand: deck.remove(item)
            hyst = []
            combo = np.full(10,0.0).tolist()
            for _ in range(num1):
                flop = random.sample(deck,3)
                d = deck[:]
                for item in flop: d.remove(item)
                e = 0
                for _ in range(num2):
                    sample = random.sample(d,4)
                    river = flop+sample[0:2]
                    op_hand = sample[2:4]
                    my_combo = texas(my_hand+river)
                    combo[my_combo[0]] += 100 / (num1 * num2)
                    op_combo = texas(op_hand+river)
                    table_combo = texas(river)
                    if op_combo <= my_combo and table_combo < my_combo: 
                        e += 100 / num2
                        combo[9] += 100 / (num1 * num2)
                hyst.append(e)
            for i in range(10): combo[i] = round(combo[i],1)
            combos[i1][i2] = combo
            hyst.sort(reverse=True)
            num = num1 // 100
            h = np.full(100,0.0).tolist()
            for j1 in range(100):
                r = 0
                for j2 in range(num): r+= hyst[j1*num+j2] / num
                h[j1] = round(r,1)
            hystogram[i1][i2] = h
    with open('texas_data.json', 'w') as f: json.dump([combos, hystogram], f)
    #print(hystogram[0][0])
    print(combos)

def is_straight(cards: list):
        cards.sort(reverse=True)
        l = len(cards)-4
        match l:
            case 1:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[0]-cards[1] == 9: return 3
            case 2:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[1]-cards[5] == 4: return cards[1]
                if cards[0]-cards[2] == 9: return 3
            case 3:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[1]-cards[5] == 4: return cards[1]
                if cards[2]-cards[6] == 4: return cards[2]
                if cards[0]-cards[3] == 9: return 3
            case _: return 0

def holdem(cards: list):
    def is_straight(cards: list):
        cards.sort(reverse=True)
        l = len(cards)-4
        match l:
            case 1:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[0]-cards[1] == 9: return 3
            case 2:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[1]-cards[5] == 4: return cards[1]
                if cards[0]-cards[2] == 9: return 3
            case 3:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[1]-cards[5] == 4: return cards[1]
                if cards[2]-cards[6] == 4: return cards[2]
                if cards[0]-cards[3] == 9: return 3
            case _: return 0
    
    ranks = sorted(Counter([x // 4 for x in cards]).items(),reverse=True,key=lambda item: (item[1],item[0]))
    rank_list = [item[0] for item in ranks]
    suits = Counter([x % 4 for x in cards]).most_common()
    
    if suits[0][1] >= 5:
        suit_list = [item // 4 for item in cards if item % 4 == suits[0][0]]
        result = is_straight(suit_list)
        if result: return (8,[result])
        else: return (5,suit_list[0:5])
    
    if len(rank_list) >= 5:
        result = is_straight(rank_list[:])
        if result: return (4,[result])

    if ranks[0][1] == 4: return (7, [rank_list[0], max(rank_list[1:])])

    if ranks[0][1] == 3:
        if ranks[1][1] > 1: return (6, rank_list[0:2])
        return (3, rank_list[0:3])
    
    if ranks[0][1] == 1: return (0, rank_list[0:5])

    if ranks[1][1] == 1: return (1, rank_list[0:4])
    
    return (2, rank_list[0:2] + [max(rank_list[2:])])

def holdem_noflush(cards: list):
    ranks = sorted(Counter([x // 4 for x in cards]).items(),reverse=True,key=lambda item: (item[1],item[0]))
    rank_list = [item[0] for item in ranks]

    if len(rank_list) >= 5:
        result = is_straight(rank_list)
        if result: return (4, [result])

    if ranks[0][1] == 4: return (7, [rank_list[0], max(rank_list[1:])])

    if ranks[0][1] == 3:
        if ranks[1][1] > 1: return (6, rank_list[0:2])
        return (3, rank_list[0:3])
    
    if ranks[0][1] == 1: return (0, rank_list[0:5])

    if ranks[1][1] == 1: return (1, rank_list[0:4])
    
    return (2, rank_list[0:2] + [max(rank_list[2:])])

def holdem_data():
    num1, num2 = 1000, 1000
    hystogram = np.full((13,13),0).tolist()
    combos = np.full((13,13), 0.0).tolist()
    start_time = datetime.now()
    for i1 in range(13):
        for i2 in range(13):
            my_hand = aux.from_matrix([i1,i2])
            print(my_hand, round((datetime.now() - start_time).total_seconds(),2))
            deck = list(range(0,52))
            for item in my_hand: deck.remove(item)
            hyst = []
            combo = np.full(10,0.0).tolist()
            for i3 in range(num1):
                flop = random.sample(deck,3)
                d = deck[:]
                for item in flop: d.remove(item)
                e = 0
                for i4 in range(num2):
                    sample = random.sample(d,4)
                    river = flop+sample[0:2]
                    op_hand = sample[2:4]
                    my_combo = holdem(my_hand+river)
                    combo[my_combo[0]] += 100 / num2
                    op_combo = holdem(op_hand+river)
                    table_combo = holdem(river)
                    if op_combo <= my_combo and table_combo < my_combo: 
                        e += 100 / num2
                        combo[9] += 100 / num2
                hyst.append(e)
            combos[i1][i2] = combo
            hyst.sort(reverse=True)
            num = num1 // 100
            h = np.full(100,0.0).tolist()
            for j1 in range(100):
                r = 0
                for j2 in range(num): r+= hyst[j1*num+j2] / num
                h[j1] = round(r,1)
            hystogram[i1][i2] = h
    with open('holdem_data.json', 'w') as f: json.dump([combos, hystogram], f)
    print(hystogram[0][0])

def omaha_data():
    result = {}
    for h in range(4,8):
        num1, num2 = 10000, 1000
        start_time = datetime.now()
        hyst = np.full(num1, 0.0).tolist()
        combos = [0,0,0,0,0,0,0,0,0]
        for i1 in range(num1):
            deck = list(range(52))
            my_hand = random.sample(deck, h)
            for item in my_hand: deck.remove(item)
            wins = 0
            for i2 in range(num2):
                t = random.sample(deck,5+h)
                table = t[0:5]
                op_hand = t[5:5+h]
                my_combo = omaha(my_hand,table)
                op_combo = omaha(op_hand,table)
                combos[my_combo[0]] += 100 / (num1 * num2)
                if op_combo <= my_combo: wins += 100 / num2
            hyst[i1] = round(wins,1)
    
        for i in range(9): combos[i] = round(combos[i],1)
        hyst.sort(reverse=True)
        num = num1 // 100
        hystogram = np.full(100,0.0).tolist()
        for i1 in range(100):
            r = 0
            for i2 in range(num): r+= hyst[i1*num+i2] / num
            hystogram[i1] = round(r,1)    
        result['omaha' + str(h)] = [combos,hystogram]

def omaha_preflop(hand: list):
    deck = list(range(52))
    l = len(hand)
    for item in hand: deck.remove(item)
    start_time = datetime.now()
    num1, num2 = 500, 50
    my_combos, op_combos = [0]*9, [0]*9
    my_hystos, op_hystos = [], []
    equity = 0
    for _ in range(num1):
        flop = random.sample(deck,3)
        d = deck[:]
        for item in flop: d.remove(item)
        my_wins, op_wins = 0, 0
        for _ in range(num2):
            sample = random.sample(d,2+l)
            table = flop + sample[0:2]
            op_hand = sample[2:]
            my_combo = omaha(hand,table)
            op_combo = omaha(op_hand,table)
            my_combos[my_combo[0]] += 100 / (num1*num2)
            op_combos[op_combo[0]] += 100 / (num1*num2)
            if op_combo <= my_combo: my_wins += 100 / num2
            else: op_wins += 100 / num2
        my_hystos.append(my_wins)
        op_hystos.append(op_wins)
        equity += my_wins / num1
    my_hystos.sort(reverse=True)
    op_hystos.sort(reverse=True)
    q = num1 // 100
    my_hysto = [sum(my_hystos[i*q:(i+1)*q])/q for i in range(100)]
    op_hysto = [sum(op_hystos[i*q:(i+1)*q])/q for i in range(100)]
    result = {'my_combo': my_combos, 'op_combo': op_combos, 'my_hysto': my_hysto, 'op_hysto': op_hysto, 'equity': equity}
    print('time elapsed',(datetime.now()-start_time).total_seconds())
    return result

def holdem_flop(hand: list, flop: list):
    deck = list(range(52))
    for item in hand+flop: deck.remove(item)
    my_combos, op_combos = [0]*9, [0]*9
    my_hysto, op_hysto = [0]*990, [0]*990
    start_time = datetime.now()
    for i1 in range(46):
        for i2 in range(i1+1,47):
            d = deck[:]
            d.remove(deck[i1])
            d.remove(deck[i2])
            table = flop + [deck[i1],deck[i2]]
            my_combo = holdem(hand+table)
            table_combo = holdem(table)
            my_combos[my_combo[0]] += 100 / 1081
            i = 0
            for i3 in range(44):
                for i4 in range(i3+1,45):
                    op_hand = [d[i3],d[i4]]
                    op_combo = holdem(op_hand+table)
                    op_combos[op_combo[0]] += 100 / (990 * 1081)
                    if op_combo <= my_combo and table_combo < my_combo: my_hysto[i] += 100 / 1081
                    else: op_hysto[i] += 100 / 1081
                    i += 1 
    my_hysto.sort(reverse=True)
    op_hysto.sort(reverse=True)
    q = 9.9
    my_hystos = [sum(my_hysto[int(i*q):int((i+1)*q)]) / (int((i+1)*q) - int(i*q)) for i in range(100)]
    op_hystos = [sum(op_hysto[int(i*q):int((i+1)*q)]) / (int((i+1)*q) - int(i*q)) for i in range(100)]
    result = {'my_combos': my_combos, 'op_combos': op_combos, 'my_hystos': my_hystos, 'op_hystos': op_hystos, 'equity': sum(my_hystos)/100}
    print('time elapsed',(datetime.now()-start_time).total_seconds())
    return result



card_list = []

def sample_test():
    start_time = datetime.now()
    deck = list(range(52))
    for _ in range(1000000):
        card_list.append(random.sample(deck,7))
    print('sample elapsed time',round((datetime.now()-start_time).total_seconds(),2))
#sample_test()
def holdem_test():
    def is_straight(cards: list):
        cards.sort(reverse=True)
        l = len(cards)-4
        match l:
            case 1:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[0]-cards[1] == 9: return 3
            case 2:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[1]-cards[5] == 4: return cards[1]
                if cards[0]-cards[2] == 9: return 3
            case 3:
                if cards[0]-cards[4] == 4: return cards[0]
                if cards[1]-cards[5] == 4: return cards[1]
                if cards[2]-cards[6] == 4: return cards[2]
                if cards[0]-cards[3] == 9: return 3
            case _: return 0
    
    deck = list(range(52))
    start_time = datetime.now()

    for i in range(1000000):
        #cards = random.sample(deck,7)
        cards = card_list[i]
        ranks = sorted(Counter([x // 4 for x in cards]).items(),reverse=True,key=lambda item: (item[1],item[0]))
        rank_list = [item[0] for item in ranks]
        suits = Counter([x % 4 for x in cards]).most_common()
    
        if suits[0][1] >= 5:
            suit_list = [item // 4 for item in cards if item % 4 == suits[0][0]]
            result = is_straight(suit_list)
            if result: 
                ret = (8,[result])
                continue
            else: 
                ret = (5,suit_list[0:5])
                continue
    
        if len(rank_list) >= 5:
            result = is_straight(rank_list[:])
            if result: 
                ret = (4,[result])
                continue

        if ranks[0][1] == 4: 
            ret = (7, [rank_list[0], max(rank_list[1:])])
            continue

        if ranks[0][1] == 3:
            if ranks[1][1] > 1: 
                ret = (6, rank_list[0:2])
                continue
            ret = (3, rank_list[0:3])
            continue
    
        if ranks[0][1] == 1: 
            ret = (0, rank_list[0:5])
            continue

        if ranks[1][1] == 1: 
            ret = (1, rank_list[0:4])
            continue
    
        ret = (2, rank_list[0:2] + [max(rank_list[2:])])
    print('holdem elapsedtime', round((datetime.now()-start_time).total_seconds(),2))
#holdem_test()
def is_straight_test():
    start_time = datetime.now()
    for i in range(1000000):
        ranks = sorted(Counter([x // 4 for x in card_list[i]]).items(),reverse=True,key=lambda item: (item[1],item[0]))
        rank_list = [item[0] for item in ranks]
        result = is_straight(rank_list)
    print('is_straight elapsed time',round((datetime.now()-start_time).total_seconds(),2))
#is_straight_test()
def holdem_noflush_test():
    start_time = datetime.now()
    for i in range(1000000):
        result = holdem_noflush(card_list[i]) 
    print('holdem_noflush elapsed time',round((datetime.now()-start_time).total_seconds(),2))
#holdem_noflush_test()
    
def omaha_straight(hand: list, table: list):
    h = {item // 4: 6 for item in hand}
    t = {item // 4: 1 for item in table}
    cards = defaultdict(int)
    for item in h: cards[item] += h[item]
    for item in t: cards[item] += t[item]
    result = sorted(cards.items(),reverse=True,key=lambda item: item[0])
    l = len(result) - 4
    if l > 0:
        for i1 in range(0,l):
            if result[i1][0] - result[i1+4][0] == 4:    
                s = 0
                for i2 in range(5): s += result[i1+i2][1]
                if s // 6 >= 2 and s % 6 >= 3: return result[i1][0]
        if result[0][0] - result[-4][0] == 9:
            s = result[0][1]
            for i in range(-4,0): s += result[i][1]
            if (s // 6 >= 2) and (s % 6 >= 3): 
                return 3
            
            return 5
    return 0



     
       

 

    




    