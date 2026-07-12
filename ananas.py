import random, aux
from collections import Counter
from itertools import combinations

random.seed(10)

def suit_cards(hand: list):
    hand.sort(reverse=True, key=lambda item: item // 4)
    result = {}
    for i in range(4): result[i] = []
    for item in hand: result[item % 4].append(item // 4)
    return result

def rank_cards(hand: list):
    hand.sort(reverse=True, key=lambda item: item % 4)
    result = {}
    for i in range(13): result[i] = []
    for item in hand: result[item // 4].append(item % 4)
    k = list(result.keys())
    for item in k:
        if len(result[item]) == 0: del(result[item])
    return result

def fantasy_cards(hand: list):
    result = []
    for i in range(13):
        cards = [item for item in hand if item // 4 == i]
        if len(cards) >= 3:
            result.extend(list(combinations(cards, 3)))
        if len(cards) >= 2 and i >= 10: 
            result.extend(list(combinations(cards, 2)))
    return result

def high_combo(hand: list):
    ranks = [item // 4 for item in hand]
    counter = Counter(ranks)
    for key in counter:
        match counter[key]:
            case 3: combo = (3, (key, ))
            case 2: combo = (1, (key, ))
            case 1: combo = (0, (max(ranks), ))
    return combo

def high_points(hand: list):
    points = 0
    ranks = [item // 4 for item in hand]
    counter = Counter(ranks)
    for key in counter:
        match counter[key]:
            case 2: points = max(0, key - 3)
            case 3: points = 10 + key
    return points

def combo(hand: list):
#    suit = suit_cards(hand)
    rank = rank_cards(hand)
#    print('suit', suit)
    ranks = list(rank.keys())
    ranks.sort(reverse=True)
    result = {0: [], 1: [], 2: [], 3: [], 4:[], 5: [], 6: [], 7: [], 8: [], 9: []}
    l = len(ranks)
    straights = []
    if l >= 5:
        for i in range(0, l - 4):
            if ranks[i] - ranks[i + 4] == 4:
                straights.append(ranks[i:i+5])
        if {12,0,1,2,3} <= set(ranks): straights.append([3,2,1,0,12])
    for item in straights:
     for i1 in rank[item[0]]:
      for i2 in rank[item[1]]:
       for i3 in rank[item[2]]:
        for i4 in rank[item[3]]:
         for i5 in rank[item[4]]:
          result[4].append(((item[0], ), [item[0]*4 +i1, item[1]*4 +i2, item[2]*4+i3,item[3]*4 +i4, item[4]*4+i5]))

    hand.sort(reverse=True)
    for i in range(13):
        cards = [item for item in hand if item // 4 == i]
        match len(cards):
            case 4:
                cards4 = list(combinations(cards,4))
                for item in cards4: result[7].append([(i,), list(item)])
                cards3 = list(combinations(cards,3))
                for item in cards3: result[3].append([(i,), list(item)])
                cards2 = list(combinations(cards,2))
                for item in cards2: result[1].append([(i,), list(item)])
            case 3:
                cards3 = list(combinations(cards,3))
                for item in cards3: result[3].append([(i,), list(item)])
                cards2 = list(combinations(cards,2))
                for item in cards2: result[1].append([(i,), list(item)])
            case 2:
                cards2 = list(combinations(cards,2))
                for item in cards2: result[1].append([(i,), list(item)])

    suits = [[],[],[],[]]
    for item in hand : suits[item % 4].append(item)
    for i in range(4):
        if len(suits[i]) >= 5: 
            comb = list(combinations(suits[i], 5))
            for item in comb:
                l = list(item)
                k = tuple([x // 4 for x in l])
                if k[0] - k[4] == 4:
                    if k[0] == 12: 
                        result[9].append(((k[0], ), l))
                    else: result[8].append(((k[0], ), l))
                    continue
                if k == (12,3,2,1,0): 
                    result[8].append(((3, ), l))
                    continue
                result[5].append((k, list(item)))
    if len(result[3]) >=1:
        for item1 in result[3]: 
            for item2 in result[1]:
                if item1[0][0] != item2[0][0]:
                    result[6].append(((item1[0][0],item2[0][0]), item1[1] + item2[1]))
    
    if len(result[1]) >=2:
        for item1 in result[1]: 
            for item2 in result[1]:
                if item1[0][0] > item2[0][0]:
                    result[2].append(((item1[0][0],item2[0][0]), item1[1] + item2[1]))
    
    k = list(result.keys())
    for v in k:
        if len(result[v]) == 0: del result[v]
    return result           




def main(l):
    deck = list(range(52))
    deal = random.sample(deck,l)
    deal.sort()
#    deal.sort(reverse=True, key=lambda item: (item // 4, 3 - item % 4))
    print(aux.show_cards(deal))
    result = []
    comb2 = combo(deal)
    for k1 in comb2.keys():
        for item1 in comb2[k1]:
            hand = deal[:]
            for n in item1[1]: hand.remove(n)
            comb3 = combo(hand)
            for k2 in comb3.keys():
                for item2 in comb3[k2]:
                    if (k2,item2[0]) < (k1,item1[0]):
#                        result.append([(k1,k2), (item1[0], item2[0]), item1[1]+item2[1]])
                        f_cards = hand[:]
                        for n in item2[1]: f_cards.remove(n)
                        f_combo = high_combo(f_cards)
                        print('f combo', f_combo, (k2,item2[0]))
                        if f_combo <= (k2,item2[0]): result.append([(k1,k2,f_combo[0]), (item1[0], item2[0], f_combo[1] )]) #, item1[1]+item2[1]])
    result.sort(reverse=True, key=lambda item: (item[0], item[1]))
    print(result[0:])                
                

#    f_cards = fantasy_cards(deal)
#    print(f_cards)
#    for item in f_cards: print(aux.show_cards(item), high_combo(item), high_points(item))


r = main(13)
