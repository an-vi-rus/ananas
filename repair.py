import random, json, os
from aux import show_cards
import poker

#print("File location using os.getcwd():", os.getcwd())
random.seed()
deck = list(range(52))
def load_data():
    preflop = {}
    with open('holdem.json') as f:
        data = json.load(f)
    preflop['holdem'] = data
    with open('texas.json') as f:
        data = json.load(f)
    preflop['texas'] = data
    omaha = {}
    with open('omaha.json') as f: data = json.load(f)
    for i in range(4,8):
        d = data['omaha'+str(i)]
        omaha['omaha'+str(i)] = {'combo': d[0], 'combos': d[1]}
    preflop['omaha'] = omaha
    with open('preflop.json', 'w') as f: json.dump(preflop,f)

def normalize_hand(hand: list):
    h = [[item // 4, item % 4] for item in hand]
    h.sort(reverse=True, key=lambda x: x[0])
    suits = [item[1] for item in h]
    new_suits = suits[:]
    i = 0
    s={}
    new_suits = suits[:]
    for i1 in range(len(hand)):
        if suits[i1] in s: 
            new_suits[i1] = s[suits[i1]]
        else:
            s[suits[i1]] = i        
            new_suits[i1] = i
            i+= 1
    new_hand = []
    for i in range(len(hand)): new_hand.append(h[i][0]*4+new_suits[i]) 
    return new_hand

with open('preflop.json') as f: data = json.load(f)

for i in range(4,8):
    h = data['omaha']['omaha'+str(i)]['combos']
    data['omaha']['omaha'+str(i)]['hysto'] = h
    del data['omaha']['omaha'+str(i)]['combos']
    print(data['omaha']['omaha'+str(i)])
with open('preflop_data.json','w') as f: json.dump(data,f)


def update():
    with open('preflop.json') as f: data = json.load(f)
    holdem_hyst = data['holdem']['hysto']
    texas_hyst = data['texas']['hysto']
    for tab in poker.tabs:
        if tab.startswith('Holdem'): 
            cnv = poker.tabs[tab]['cnv']
            for i in range(100):
                cnv.create_line((600,600-i,600+holdem_hyst[i],600-i),fill='red')
        if tab.startswith('Texas'): 
            cnv = poker.tabs[tab]['cnv']
            for i in range(100):
                cnv.create_line((600,600-i,600+texas_hyst[i],600-i),fill='red')


#update()

#load_data()