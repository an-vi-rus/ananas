from collections import Counter
import aux
import random, json, numpy as np
from datetime import datetime

random.seed()
   
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

u



deck = list(range(52))

decks, num = 1000, 10000

def chances(hand: list):
    hand_size = len(hand)
    deck = list(range(52))
    my_combos = np.full(9, 0)
    wins = 0
    for item in hand: deck.remove(item)
    start_time = datetime.now()
    for i in range(10000):
        sample = random.sample(deck, 5 + hand_size)
        table = sample[0:5]
        op_hand = sample[5:5+hand_size]
        my_combo = omaha(hand, table)
        op_combo = omaha(op_hand, table)
        my_combos[my_combo[0]] += 1
        if op_combo <= my_combo: wins += 1
    end_time = datetime.now()
    delta = end_time - start_time
    print('time elapsed', delta.total_seconds())
    result = []
    for i in range(9): result.append(int(my_combos[i] / 10) / 10)
    print(result)
    return 100 * wins / 10000

def my_preflop(hand: list, num=1000000):
    hand_size = len(hand)
    deck = list(range(52))
    my_combos, op_combos = np.full(10, 0.0), np.full(10, 0.0)
    my_wins, op_wins = np.full(9, 0.0), np.full(9, 0.0)
    for item in hand: deck.remove(item)
    start_time = datetime.now()
    for i in range(num):
        sample = random.sample(deck, 5 + hand_size)
        table = sample[0:5]
        op_hand = sample[5:5+hand_size]
        my_combo = omaha(hand, table)
        op_combo = omaha(op_hand, table)
        my_combos[my_combo[0]] += 1
        op_combos[op_combo[0]] += 1
        if op_combo <= my_combo: 
            my_combos[9] += 1
            my_wins[my_combo[0]] += 1
        if op_combo >= my_combo:
            op_combos[9] += 1
            op_wins[op_combo[0]] += 1
    end_time = datetime.now()
    delta = end_time - start_time
    print('elapsed time', delta.total_seconds())
    my_combos = my_combos * 100 / num
    op_combos = op_combos * 100 / num
    my_wins = my_wins * 100 / num
    op_wins = op_wins * 100 / num
    print(aux.show_cards(hand))
    print(sum(my_combos[0:9]),sum(op_combos[0:9]),my_combos[9]+op_combos[9])
    
    print(f'пусто {my_combos[0]}, пара {my_combos[1]}, 2 пары {my_combos[2]}, сет {my_combos[3]}, стрит {my_combos[4]}, флеш {my_combos[5]}, фулхаус {my_combos[6]}, каре {my_combos[7]}, флешстрит {my_combos[8]}, шансы {my_combos[9]}')
    print(f'пусто {op_combos[0]}, пара {op_combos[1]}, 2 пары {op_combos[2]}, сет {op_combos[3]}, стрит {op_combos[4]}, флеш {op_combos[5]}, фулхаус {op_combos[6]}, каре {op_combos[7]}, флешстрит {op_combos[8]}, шансы {op_combos[9]}')
    print(f'пусто {my_wins[0]}, пара {my_wins[1]}, 2 пары {my_wins[2]}, сет {my_wins[3]}, стрит {my_wins[4]}, флеш {my_wins[5]}, фулхаус {my_wins[6]}, каре {my_wins[7]}, флешстрит {my_wins[8]}')
    print(f'пусто {op_wins[0]}, пара {op_wins[1]}, 2 пары {op_wins[2]}, сет {op_wins[3]}, стрит {op_wins[4]}, флеш {op_wins[5]}, фулхаус {op_wins[6]}, каре {op_wins[7]}, флешстрит {op_wins[8]}')



def to_matrix(hand: list):
    h = []
    for item in hand: h.append((item // 4, item % 4))
    h.sort(key=lambda item: item[0])
    suits = [item[1] for item in h]
    suit_dict = {}
    i = 0
    for item in suits:
        if item not in suit_dict: 
            suit_dict[item] = i
            i += 1
    result = []
    for i in range(len(hand)):
        result.append((h[i][0], suit_dict[h[i][1]]))
    result.sort(key=lambda item: (item[0], item[1]))
    return tuple(result)
    

def omaha7counter():
    hands = []
    start_time = datetime.now()
    for i1 in range(0, 46):
      print('i1', i1)
      for i2 in range(i1+1, 47):
        for i3 in range(i2+1, 48):
          for i4 in range(i3+1, 49):
            for i5 in range(i4+1, 50):
              for i6 in range(i5+1, 51):
                for i7 in range(i6+1, 52):
                  hand = to_matrix([i1,i2,i3,i4,i5,i6,i7])
                  hands.append(hand)
    end_time = datetime.now()
    delta = end_time - start_time
    print ('elapsed time', delta.total_seconds())
    hands = tuple(hands)
    hands_counter = Counter(hands)
    end_time = datetime.now()
    delta = end_time - start_time
    print ('elapsed time', delta.total_seconds())
    with open('omaha7counter.json', 'w') as f:
        json.dump(hands_counter, f)
    end_time = datetime.now()
    delta = end_time - start_time
    print ('elapsed time', delta.total_seconds())

omaha7counter()

def hands(l=4):
    hands = []
    start_time = datetime.now()
    for i1 in range(3,52):
      for i2 in range(2,i1):
        for i3 in range(1,i2):
          for i4 in range(0,i3):       
            hands.append(to_matrix((i1, i2, i3, i4)))
    hands.sort(reverse=True, key=lambda item: (item[0], item[1], item[2], item[3]))
    hands = tuple(hands)
    inv = Counter(hands)
    hands_ = []
    for item in hands:
        r = ((item[0][0],item[1][0],item[2][0],item[3][0]), (item[0][1],item[1][1],item[2][1],item[3][1]))
        hands_.append(r)
    hand_suits = []
    for item in hands_:
        hand_suits.append(item[1])
    suits_counter = Counter(hand_suits)
    hand_ranks = []
    for item in hands_:
        hand_ranks.append(item[0])
    ranks_counter = Counter(hand_ranks)       
    end_time = datetime.now()
    delta = end_time - start_time
    #print('elapsed time', delta.total_seconds(), len(hands), len(inv), len(suits_counter), len(ranks_counter))
    values = list({*inv.values()})
    counters = []
    for i in range(len(values)):
        counters.append([])
        for key, value in inv.items():
            if value == values[i]: counters[i].append(key)
    #print(len(counters[0]),len(counters[1]),len(counters[2]),len(counters[3]),len(counters[4]),len(counters[5]))
    #print(len(counters[0])+len(counters[1])+len(counters[2])+len(counters[3])+len(counters[4])+len(counters[5]))


#hands()

max_hand_size = 7
for h in range(14, max_hand_size + 1):
    start_time = datetime.now()
    stats = np.full(decks, 0.0)
    for i in range(decks):
        deck = list(range(52))
        my_hand = random.sample(deck, h)
        for item in my_hand: deck.remove(item)
        wins = 0
        for j in range(num):
            sample = random.sample(deck, 5 + h)    
            table = sample[0:5]
            op_hand = sample[5:5+h]
            my_combo = omaha(my_hand, table)
            op_combo = omaha(op_hand, table)
            if op_combo <= my_combo: wins += 1
        
        stats[i] = round(100 * wins / num, 1)
        #print('chance of hand', aux.show_cards(my_hand), stats[i])
    
    end_time = datetime.now()
    delta = end_time - start_time
#    print('omaha', str(h), sum(stats) / decks, 'elapsed time', delta.total_seconds(), '\n')
#    with open('omaha'+str(h)+'h.json', 'w') as f:
#        json.dump(stats.tolist(), f)

#print('\n')