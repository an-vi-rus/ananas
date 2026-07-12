import random, json
from datetime import datetime, date, time
from PIL import Image, ImageTk
from collections import Counter
import numpy as np
from itertools import combinations

straights = ({12,11,10,9,8}, {11,10,9,8,7}, {10,9,8,7,6}, {9,8,7,6,5}, {8,7,6,5,4},{7,6,5,4,3},{6,5,4,3,2},{5,4,3,2,1},{4,3,2,1,0},{3,2,1,0,12})
rank_sym = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
suit_sym = ('♥♠♦♣')

def show_cards(cards: list):
    card_ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
    card_suits = ('♥♠♦♣')
    r = ''
    for item in cards: 
        r += card_ranks[item // 4]
        r += card_suits[item % 4] + ','
    return r

def show_card(card: int):
    card_ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
    card_suits = ('♥♠♦♣')
    return card_ranks[card // 4] + card_suits[card % 4]

def to_matrix(hand: list):
    h = [12 - hand[0] // 4, 12 - hand[1] // 4]
    h.sort()
    if hand[0] % 4 != hand[1] % 4: h.sort(reverse=True)
    return h
def from_matrix(hand: list):return [(12 - hand[0])*4, (12 - hand[1])*4] if hand[0] < hand[1] else [(12 - hand[1])*4, (12 - hand[0])*4+1] 
def to_key(hand: list):
    h = [str(item) for item in hand]
    return '-'.join(h)
def from_key(key: str):
    result = key.split('-')
    for i in range(len(result)): result[i] = int(result[i])
    return result
def scale(hand: list):
    if hand[0] < hand[1]: return 2
    if hand[0] == hand[1]: return 3
    return 6
def round_list(lst: list, digits: int):
    result = []
    for i in range(len(lst)): result.append(round(lst[i],digits))
    return result
def to_hysto(hysto: list, size: int) -> list[float]:
    l = len(hysto)
    q = l / size
    result = [0] * size
    for i in range(size):
        r1, r2 = round(i*q), round((i+1)*q)
        result[i] = round(sum(hysto[r1:r2])/(r2-r1),1)
    return result

def data_load():
    filename = 'Texas/preflop.json'
    global data
    texas = {}
    with open(filename) as f: data = json.load(f)
    equity = np.full((9, 9), 0.0).tolist()
    combo = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    combos = np.full((9, 9, 10), 0.0).tolist()
    hystogram = []

    for key1 in data:
        hand = to_matrix(from_key(key1))
        data1 = data[key1]
        for value2 in data1.values():
            hystogram.extend([value2[9]] * scale(hand))
            for i in range(10):
                combos[hand[0]][hand[1]][i] += value2[i] / 5984
    hystogram.sort(reverse=True)
    n = len(hystogram) // 100
    result = []
    for i1 in range(100):
        r = 0
        for i2 in range(n):
            r += hystogram[n * i1 + i2] / n
        result.append(round(r,1))
    texas['hystogram'] = result

    for i1 in range(9):
        for i2 in range(9):
            equity[i1][i2] = round(combos[i1][i2][9], 1)
            for i3 in range(9): 
                combo[i3] += combos[i1][i2][i3] * scale([i1, i2])
    for i in range(9): combo[i] = round(combo[i] / 315, 1)
    texas['equity'] = equity
    texas['combos'] = combo
    return texas
def my_combo(hand: list):
    combo = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    key = to_key(from_matrix(to_matrix(hand)))
    for value in data[key].values():
        for i in range(9): combo[i] += value[i] / 5984
    for i in range(9): combo[i] = round(combo[i], 1)
    return combo
def my_hystogram(hand: list):
    hystogram = []
    key = to_key(from_matrix(to_matrix(hand)))
    for value in data[key].values():
        hystogram.append(value[9])
    hystogram.sort(reverse=True)
    n = len(hystogram) // 100
    result = []
    for i1 in range(100):
        r = 0
        for i2 in range(n):
            r += hystogram[n * i1 + i2] / n
        result.append(round(r, 1))
    return result

def holdem(cards: list):
    ranks = Counter([x // 4 for x in cards]).most_common()
    ranks.sort(key=lambda item: (item[1], item[0]), reverse=True)
    suits = Counter([x % 4 for x in cards]).most_common()
    straights = ({12,11,10,9,8}, {11,10,9,8,7}, {10,9,8,7,6}, {9,8,7,6,5}, {8,7,6,5,4},{7,6,5,4,3},{6,5,4,3,2},{5,4,3,2,1},{4,3,2,1,0},{3,2,1,0,12})
    
    if suits[0][1] >= 5:
        suit = suits[0][0]
        suit_cards = {x // 4 for x in cards if x % 4 == suit}
        for i in range(len(straights)):
            if straights[i] <= suit_cards: return (8, (12 - i,))
        result = list(suit_cards)
        result.sort(reverse=True)
        return (5, (*result[0:5],))
    
    result = [item[0] for item in ranks]

    if len(result) >= 5:
        s = set(result)
        for i in range(len(straights)):
            if straights[i] <= s: return (4, (12 - i,))

    if ranks[0][1] == 4: return (7, (result[0], max(result[1:])))

    if ranks[0][1] == 3:
        if ranks[1][1] > 1: return (6, (*result[0:2],))
        return (3, (*result[0:3],))
    
    if ranks[0][1] == 1: return (0, (*result[0:5],))

    if ranks[1][1] == 1: return (1, (*result[0:4],))
    
    return (2, (*result[0:2], max(result[2:])))
def holdem_data():
    num1, num2 = 1000, 1000
    hystogram = np.full((13,13),0).tolist()
    combos = np.full((13,13), 0.0).tolist()
    for i1 in range(13):
        for i2 in range(13):
            my_hand = from_matrix([i1,i2])
            deck = list(range(0,52))
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
                    my_combo = holdem(my_hand+river)
                    combo[my_combo[0]] += 100 / (num1 * num2)
                    op_combo = holdem(op_hand+river)
                    table_combo = holdem(river)
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
    with open('holdem_data.json', 'w') as f: json.dump([combos, hystogram], f)

def texas(cards: list):
    ranks = Counter([x // 4 for x in cards]).most_common()
    ranks.sort(key=lambda item: (item[1], item[0]), reverse=True)
    suits = Counter([x % 4 for x in cards]).most_common()
    straights = ({12,11,10,9,8}, {11,10,9,8,7}, {10,9,8,7,6}, {9,8,7,6,5}, {8,7,6,5,4},{7,6,5,4,12})
    
    if suits[0][1] >=5:
        suit = suits[0][0]
        suit_cards = {x // 4 for x in cards if x % 4 == suit}
        for i in range(len(straights)):
            if straights[i] <= suit_cards: return (8, (12 - i,))
        result = list(suit_cards)
        result.sort(reverse=True)
        return (6, (*result[0:5],))
    
    result = [item[0] for item in ranks]
    
    if len(result) >= 5:
        s = set(result)
        for i in range(len(straights)):
            if straights[i] <= s: return (4, (12 - i,))

    if ranks[0][1] == 4: return (7, (result[0], max(result[1:])))
    
    if ranks[0][1] == 3:
        if ranks[1][1] > 1: return (5, (*result[0:2],))
        return (3, (*result[0:3],))
    
    if ranks[0][1] == 1: return (0, (*result[0:5],))
    
    if ranks[1][1] == 1: return (1, (*result[0:4],))
    
    return (2, (*result[0:2], max(result[2:])))
def texas_data():
    num1, num2 = 1000, 1000
    hystogram = np.full((9,9),0).tolist()
    combos = np.full((9,9), 0.0).tolist()
    for i1 in range(9):
        for i2 in range(9):
            my_hand = from_matrix([i1,i2])
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

   
def omaha(hand: list, table: list):
    def is_straight(hand: set, table: set):
        straights = ({12,11,10,9,8}, {11,10,9,8,7}, {10,9,8,7,6}, {9,8,7,6,5}, {8,7,6,5,4},{7,6,5,4,3},{6,5,4,3,2},{5,4,3,2,1},{4,3,2,1,0},{3,2,1,0,12})
    
        l = len(table)
        t = sorted(table, reverse=True)
        table_set = []
        for i in range(l - 2):
            for j in range(i + 1, l - 1):
                for k in range(j + 1, l):
                    if t[i] - t[k] < 5 or t[i] == 12 and t[j] < 4:
                        table_set.append({t[i], t[j], t[k]})
        for i in range(len(straights)):
            for item in table_set:
                if item <= straights[i]:
                    if straights[i] - item <= hand:
                        return 12 - i
        return 0 

    hand_rank_counter = Counter([item // 4 for item in hand])
    hand_suit_counter = Counter([item % 4 for item in hand])
    table_rank_counter = Counter([item // 4 for item in table])
    table_suit_counter = Counter([item % 4 for item in table])
    for key in hand_rank_counter: hand_rank_counter[key] = min(hand_rank_counter[key],2)
    for key in hand_suit_counter: hand_suit_counter[key] = min(hand_suit_counter[key],2)
    for key in table_rank_counter: table_rank_counter[key] = min(table_rank_counter[key],3)
    for key in table_suit_counter: table_suit_counter[key] = min(table_suit_counter[key],3)
    full_rank_counter = (hand_rank_counter + table_rank_counter)
    full_suit_counter = (hand_suit_counter + table_suit_counter)
    table_rank_list = sorted(list({item // 4 for item in table}),reverse=True)
    hand_rank_list = sorted(list({item // 4 for item in hand}),reverse=True)
    #table_rank_set = {item // 4 for item in table}
    hand_rank_set = {item // 4 for item in hand}
    ranks = sorted(full_rank_counter.items(),key=lambda item: (item[1],item[0]),reverse=True)
    
    s = full_suit_counter.most_common(1)
    if s[0][1] == 5:
        suit = s[0][0]
        h = {item // 4 for item in hand  if item % 4 == suit}
        t = {item // 4 for item in table if item % 4 == suit}
        result = is_straight(h,t)
        if result: return (8, (result,))

    if ranks[0][1] == 4: return (7, (ranks[0][0],))
    
    i = 0
    l = len(ranks)
    while i < l and ranks[i][1] > 2:
        j = 0
        while j < l and ranks[j][1] > 1:
            if i == j:
                j += 1
                continue
            if hand_rank_counter[ranks[i][0]] + hand_rank_counter[ranks[j][0]] > 1 and table_rank_counter[ranks[i][0]] + table_rank_counter[ranks[j][0]] > 2:    
                return (6, (ranks[i][0],ranks[j][0]))
            j += 1
        i += 1

    if s[0][1] == 5:
        return (5, (max(item // 4 for item in hand if item % 4 == suit),))   
    
    result = is_straight(hand_rank_set,table_rank_list)
    if result: return (4,(result,))

    if ranks[0][1] == 3:
        if table_rank_counter[ranks[0][0]] == 3: return (3,(ranks[0][0],*hand_rank_list[0:2]))
        if table_rank_counter[ranks[0][0]] == 2:
            hand_rank_list.remove(ranks[0][0])
            return (3, (ranks[0][0],hand_rank_list[0]))
        return (3,(ranks[0][0],))
    
    i = 0
    l = len(ranks)
    while i < l and ranks[i][1] > 1:
        j = 0
        while j < l and ranks[j][1] > 1:
            if i == j:
                j += 1
                continue
            h_r_c = hand_rank_counter[ranks[i][0]] + hand_rank_counter[ranks[j][0]]
            if h_r_c > 1 and h_r_c < 3: return(2, (ranks[i][0],ranks[j][0]))
            if h_r_c == 1: 
                return (2, (ranks[i][0],ranks[j][0], max(hand_rank_set - {ranks[i][0],ranks[j][0]}))) 
            j += 1
        i += 1

    if ranks[0][1] > 1:
        if hand_rank_counter[ranks[0][0]] == 2: return (1, (ranks[0][0],))
        if hand_rank_counter[ranks[0][0]] == 1: 
            hand_rank_list.remove(ranks[0][0])
            return (1, (ranks[0][0],hand_rank_list[0]))
        return (1, (ranks[0][0],*hand_rank_list[0:2]))
    
    return (0,(*hand_rank_list[0:2],))

def get_samples(deal_size = [20, 27], sample_size = [50, 100, 200, 400]):
    samples = {}
    for d in deal_size:
        samples[d] = []
        deals = list(combinations(range(d), 3))
        for s in sample_size:
            sample = random.sample(deals, s)
            samples[d].append(sample)
    return samples









