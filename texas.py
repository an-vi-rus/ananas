import random, json
from datetime import datetime, date, time
from PIL import Image, ImageTk
from collections import Counter
import numpy as np
from aux import show_cards, to_key, from_key, to_matrix, from_matrix, scale

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
    








#data_load()
#print(my_combo([50, 51]))
#print(my_hystogram([50, 51]))
#print(show_cards([16,18,30,44,45,46,48]))


