from itertools import combinations, product
import random
from aux import show_cards, straights

def combo_cards(hand: list):
    rank_cards, suit_cards = [], []
    result = {}
    for i in range(13): rank_cards.append([])
    for i in range(4) : suit_cards.append(set())
    for i in range(1,10): result[i] = []

    for card in hand: 
        rank_cards[card // 4].append(card)
        suit_cards[card %  4].add(card)

    for straight in straights:
        card_list = []
        for rank in straight: card_list.append(rank_cards[rank])
        comb = list(product(*card_list))
        for item in comb:
            if item: result[4].append(((rank,),item))

    for item in suit_cards:
        if len(item) >=5:
            comb = list(combinations(item,5))
            for i in comb:
                ranks = set()
                for card in i: ranks.add(card // 4)
                if straights[0] <= ranks: result[9].append(((12,), i))
                else:
                    for ind in range(1,10):
                        if straights[ind] <= ranks: 
                            result[8].append(((12-ind,), i))
                            break
                    result[5].append((tuple(sorted(ranks,reverse=True)), i))
    
    for rank in range(13):
        match len(rank_cards[rank]):
            case 4:
                result[7].append(((rank,),tuple(rank_cards[rank])))
                comb = list(combinations(rank_cards[rank],3))
                for item in comb: 
                    result[3].append(((rank,),item))
                comb = list(combinations(rank_cards[rank],2))
                for item in comb: 
                    result[1].append(((rank,),item))
            case 3:
                result[3].append(((rank,),tuple(rank_cards[rank])))
                comb = list(combinations(rank_cards[rank],2))
                for item in comb: 
                    result[1].append(((rank,),item))
            case 2:
                result[1].append(((rank,),tuple(rank_cards[rank])))

    for item3 in result[3]:
        for item2 in result[1]:
            if item3[0] != item2[0]:
                result[6].append(((item3[0]+item2[0]), item3[1] + item2[1]))
    
    for item3 in result[1]:
        for item2 in result[1]:
            if item3[0] > item2[0]:
                result[2].append(((item3[0]+item2[0]), item3[1] + item2[1]))

    keys = list(result.keys())
    for key in keys:
        if len(result[key]) == 0: del result[key]
    result[0] = [((tuple(), set()))]
    return result             

def high_row(hand: list):
    ranks = []
    result = {1: [], 3: []}
    for i in range(13): ranks.append([])
    for card in hand: ranks[card // 4].append(card)
    for rank in range(13):
        cards = ranks[rank]
        match len(cards):
            case 3 | 4:
                comb = list(combinations(cards, 3))
                for item in comb: result[3].append(((rank,), item))
                comb = list(combinations(cards, 2))
                for item in comb: result[1].append(((rank,), item))
            case 2:
                result[1].append(((rank,), tuple(ranks[rank])))
    return result

def points(comb, row):
    match row:
        case 0: 
            match comb[0]:
                case 1: return max(comb[1][0]-3,0)
                case 3: return comb[1][0]+10
        case 1: 
            match comb[0]:
                case 3: return 2
                case 4: return 4
                case 5: return 8
                case 6: return 12
                case 7: return 20
                case 8: return 30
                case 9: return 50
        case 2: 
            match comb[0]:
                case 4: return 2
                case 5: return 4
                case 6: return 6
                case 7: return 10
                case 8: return 15
                case 9: return 25
    return 0

def create_hands(hand: list):
    combos = combo_cards(hand)
    hands = []
    rows = []
    hand_combos = []
    for i in combos.keys():
        for item in combos[i]:
            row = [i,item[0],set(item[1])]
            rows.append(row)
    rows.sort(reverse=True, key=lambda item: (item[0],item[1]))

    #for row in rows: print(row)

    for i1 in range(len(rows) - 2):
        for i2 in range(i1+1, len(rows) - 1):
            if rows[i2][2].isdisjoint(rows[i1][2]):
                for i3 in range(i2+1, len(rows)):
                    if rows[i3][2].isdisjoint(rows[i2][2] | rows[i1][2]):
                        hands.append([rows[i3],rows[i2],rows[i1]])



    hands.sort(reverse=True, key=lambda item: (item[0],item[1],item[2]))
    for item in hands:
        hand_combos.append(Hand(item[0],item[1],item[2]))
    return hand_combos

class Hand:
    def __init__(self,high,mid,low):
        self.high_combo = high[0]
        if high[1]: self.high_comb_rank = high[1][0]
        else: self.high_comb_rank = 0
        self.high_cards = list(high[2])
        self.high_points = points([self.high_combo,[self.high_comb_rank]],0)
        self.high_extra = 0
        self.mid_combo = mid[0]
        self.mid_cards = list(mid[2])
        self.mid_points = points([self.mid_combo],1)
        self.mid_extra = 0
        self.low_combo = low[0]
        self.low_cards = list(low[2])
        self.low_points = points([self.low_combo],2)
        self.low_extra = 0
        self.scoop_points = 0
        self.extra_points = self.high_extra+self.mid_extra+self.low_extra+self.scoop_points
        self.total_points = self.high_points+self.mid_points+self.low_points+self.extra_points
        self.fantasy = self.high_combo == 3 or self.mid_combo >=6 or self.low_combo >= 7
    def show_hand(self):
        print(show_cards(self.high_cards),show_cards(self.mid_cards),show_cards(self.low_cards),self.high_points,
            self.mid_points,self.low_points,'total',self.total_points)
        #print('combos',self.high_combo,self.mid_combo,self.low_combo)
        #print('points ',self.high_points,self.mid_points,self.low_points,self.total_points)

    

random.seed()
deck = list(range(52))

for hand_size in range(14,15):
    for i in range(3):
        hand = random.sample(deck, hand_size)
        hand.sort(reverse=True, key=lambda item: (item // 4, 3 - item % 4))
        hand = create_hands(hand)
        hand.sort(reverse=True, key=lambda item: (item.fantasy,item.total_points))
        fantasy = hand[0].fantasy
        hand_points = hand[0].total_points
        #print(fantasy, hand_points)
        #hand[0].show_hand()
