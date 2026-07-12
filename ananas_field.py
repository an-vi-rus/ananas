import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from collections import Counter
from aux import show_cards, straights, get_samples
import random
from itertools import combinations, product
from copy import deepcopy
from datetime import datetime as dt
import combos
import no_fs

root = tk.Tk()
root.title("Ananas")
root.attributes("-fullscreen", True)
root.update_idletasks()

card_h = int(root.winfo_height() / 12)
card_w = int(card_h / 1.4)
frame = ttk.Frame(root)
frame.pack(fill='both', expand=True)
canvas = tk.Canvas(frame, bg='lightgreen', bd=0)
canvas.pack(fill='both', expand=True)

rb_value = IntVar()
rb_value.set(0)
penalty = -6
premium = +6

samplesize = [30, 50 , 100, 200, 500]
samples = get_samples(range(16, 28), samplesize)

def is_straight(cards: list):
    if cards[0] - cards[4] == 4: return cards[0]
    if cards[0] == 12 and cards[1] == 3: return 3
    for i in range(len(straights)):
        if straights[i] <= cards: return 12 - i
    return 0

def high_final(hand: list):
    ranks = [item // 4 for item in hand]
    counter = Counter(ranks).most_common()
    match len(counter):
        case 3: return (0, sorted(ranks, reverse=True))
        case 2: return (1, [counter[0][0], counter[1][0]])
        case 1: return (3, [ranks[0]])
def combo_final(hand: list):
    ranks = [item // 4 for item in hand]
    ranks.sort(reverse=True)
    counter = Counter(ranks).most_common()
    if counter[0][1] > 1:
        rnks = [item[0] for item in counter]
        match len(counter):
            case 4: return (1, rnks)
            case 3: 
                if counter[1][1] == 2: return (2, rnks)
                return (3, rnks)
            case 2: 
                if counter[1][1] == 2: return (6, rnks)
                return (7, rnks)
    suits = [item % 4 for item in hand]
    if suits[1:5].count(suits[0]) == 4:
        if ranks[4] == 8: return (9, [12])
        if ranks[0] - ranks[4] == 4: return (8, [ranks[0]])
        if ranks[0] - ranks[1] == 9: return (8, [3])
        return (5, ranks)
    if ranks[0] - ranks[4] == 4: return (4, [ranks[0]])
    if ranks[0] - ranks[1] == 9: return (4, [3])
    return (0, ranks)

def combo_to_str(combos):
    r = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    match combos[0]:
        case 1: return 'Pair of '+ r[combos[1][0]]
        case 2: return 'Two pairs '+ r[combos[1][0]] + ' and '+ r[combos[1][1]]
        case 3: return 'Set of ' + r[combos[1][0]]
        case 4: return 'Straight highest ' + r[combos[1][0]]
        case 5: return 'Flush highest ' + r[combos[1][0]]
        case 6: return 'Full hause ' + r[combos[1][0]] + ' and ' + r[combos[1][1]]
        case 7: return 'Four of a kind ' + r[combos[1][0]]
        case 8: return 'Straight flush highest ' + r[combos[1][0]]
        case 9: return 'Royal flush'
        case 0: return ''
def points(combo, row):
    match row:
        case 0: 
            match combo[0]:
                case 1: return max(combo[1][0]-3, 0)
                case 3: return combo[1][0]+10
        case 1: 
            match combo[0]:
                case 3: return 2
                case 4: return 4
                case 5: return 8
                case 6: return 12
                case 7: return 20
                case 8: return 30
                case 9: return 50
        case 2: 
            match combo[0]:
                case 4: return 2
                case 5: return 4
                case 6: return 6
                case 7: return 10
                case 8: return 15
                case 9: return 25
    return 0
def highrow_points(combo):
    match combo[0]:
            case 1: 
                if combo[1][0] < 4: return 0
                if combo[1][0] < 7: return combo[1][0] -3
                return combo[1][0] + 3
            case 3: return combo[1][0] + 16
            case 0: return 0

def add_card3(row, card):
    row.cells -= 1
    rank = card // 4
    match row.cells:
        case 0:
            row.combo = combos.c3_2(row.combo, rank)
            row.points = points0(row.combo)
            return
        case 1:
            if row.combo[1][0] == rank: 
                row.combo = (1, [rank])
                return
            else:
                row.combo = (0, [row.combo[1][0], rank]) if row.combo[1][0] > rank else (0, [rank, row.combo[1][0]])
                return
        case 2:
            row.combo = (0, [rank])
            return
def add_pair3(row, pair: list):
    row.cells -= 2
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    if row.cells == 0:
        row.combo = combos.c3_1(row.combo, [rank0, rank1])
        row.points = points0(row.combo)
        return row
    else:
        if rank0 == rank1:
            row.combo = (1, [rank0])
            return row
        row.combo = (0, [rank0, rank1]) if rank0 > rank1 else (0, [rank1, rank0])
        return row
def add_card5(row, card: int) -> tuple:
    row.cells -= 1
    rank, suit = card // 4, card % 4
    match row.cells:
        case 0: 
            row.combo = combos.c5_4(row.combo, rank)
            if row.combo[0]:
                row.max_combo = row.combo
                row.points = row.get_points()
                return
            if row.combo[1][0] - row.combo[1][-1] <= 4: row.straight = row.combo[1][0]
            elif row.combo[1][0] == 12 and row.combo[1][1] == 3: row.straight = 3
            else: row.straight = 0
            if row.flush == suit: 
                if row.straight:
                    row.combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    row.max_combo = row.combo
                    row.points = row.get_points()
                    return
                row.combo = (5, row.combo[1])
                row.max_combo = row.combo
                row.points = row.get_points()
                return
            if row.straight:
                row.combo = (4, [row.straight])
                row.max_combo = row.combo
                row.points = row.get_points()
                return
            row.max_combo = row.combo
            row.points = row.get_points()
            return
        case 1: 
            row.combo = combos.c4_3(row.combo, rank)
            if row.combo[0]:
                row.max_combo = combos.max_combo(row.combo)
                return
            if row.combo[1][0] - row.combo[1][-1] <= 4: row.straight = min(row.combo[1][-1] + 4, 12)
            elif row.combo[1][0] == 12 and row.combo[1][1] <= 3: row.straight = 3
            else: row.straight = 0
            if row.flush == suit: 
                if row.straight:
                    row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    return
                row.max_combo = (5, [12])
                return
            row.flush = -1
            if row.straight:
                row.max_combo = (4, [row.straight])
                return
            row.max_combo = combos.max_combo(row.combo)
            return
        case 2: 
            row.combo = combos.c3_2(row.combo, rank)
            if row.combo[0]:
                row.max_combo = combos.max_combo(row.combo)
                return
            if row.combo[1][0] - row.combo[1][-1] <= 4: row.straight = min(row.combo[1][-1] + 4, 12)
            elif row.combo[1][0] == 12 and row.combo[1][1] <= 3: row.straight = 3
            else: row.straight = 0
            if row.flush == suit: 
                if row.straight:
                    row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    return
                row.max_combo = (5, [12])
                return
            row.flush = -1
            if row.straight:
                row.max_combo = (4, [row.straight])
                return
            row.max_combo = combos.max_combo(row.combo)
            return
        case 3:
            if row.combo == rank:
                row.combo = (1, [rank])
                row.max_combo = (7, [rank])
                row.straight = 0
                row.flush = -1
                return
            row.combo = (0, [row.combo[1][0], rank]) if row.combo[1][0] > rank else (0, [rank, row.combo[1][0]])
            if row.combo[1][0] - row.combo[1][1] <= 4: row.straight = min(row.combo[1][1] + 4, 12)
            elif row.combo[1][0] == 12 and row.combo[1][1] <= 3: row.straight = 3
            else: row.straight = 0
            if row.flush == suit:
                if row.straight:
                    row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    return
            row.flush = -1
            row.max_combo == (7, [row.combo[1][0]])
            return
        case 4:
            row.straight = min(rank + 4, 12)
            row.flush = suit
            row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
            return
def add_pair5(row, pair: list):
    row.cells -= 2
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    suit0, suit1 = pair[0] % 4, pair[1] % 4
    match row.cells:
        case 0: 
            row.combo = combos.c5_3(row.combo, [rank0, rank1])
            if row.combo[0]:
                row.max_combo = row.combo
                row.points = row.get_points()
                return
            if row.combo[1][0] - row.combo[1][-1] <= 4: row.straight = row.combo[1][0]
            elif row.combo[1][0] == 12 and row.combo[1][1] == 3: row.straight = 3
            else: row.straight = 0
            if suit0 == suit1 and row.flush == suit0: 
                if row.straight:
                    row.combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    row.max_combo = row.combo
                    row.points = row.get_points()
                    return
                row.combo = (5, row.combo[1])
                row.max_combo = row.combo
                row.points = row.get_points()
                return
            if row.straight:
                row.combo = (4, [row.straight])
                row.max_combo = row.combo
                row.points = row.get_points()
                return
            row.max_combo = row.combo
            row.points = row.get_points()
            return
        case 1: 
            row.combo = combos.c4_2(row.combo, [rank0, rank1])
            if row.combo[0]:
                row.max_combo = combos.max_combo(row.combo)
                return
            if row.combo[1][0] - row.combo[1][-1] <= 4: row.straight = min(row.combo[1][-1] + 4, 12)
            elif row.combo[1][0] == 12 and row.combo[1][1] <= 3: row.straight = 3
            else: row.straight = 0
            if suit0 == suit1 and row.flush == suit0: 
                if row.straight:
                    row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    return
                row.max_combo = (5, [12])
                return
            row.flush = -1
            if row.straight:
                row.max_combo = (4, [row.straight])
                return
            row.max_combo = combos.max_combo(row.combo)
            return
        case 2: 
            row.combo = combos.c3_1(row.combo, [rank0, rank1])
            if row.combo[0]:
                row.max_combo = combos.max_combo(row.combo)
                return
            if row.combo[1][0] - row.combo[1][-1] <= 4: row.straight = min(row.combo[1][-1] + 4, 12)
            elif row.combo[1][0] == 12 and row.combo[1][1] <= 3: row.straight = 3
            else: row.straight = 0
            if suit0 == suit1 and row.flush == suit0: 
                if row.straight:
                    row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                    return
                row.max_combo = (5, [12])
                return
            row.flush = -1
            if row.straight:
                row.max_combo = (4, [row.straight])
                return
            row.max_combo = combos.max_combo(row.combo)
            return
        case 3:
            if rank0 == rank1:
                row.straight = 0
                row.flush = -1
                row.combo = (1, [rank0])
                row.max_combo = (7, [rank0])
                return
            else: 
                row.combo = (0, [rank0, rank1]) if rank0 > rank1 else (0, [rank1, rank0])
                if row.combo[1][0] - row.combo[1][1] <= 4: row.straight = min(row.combo[1][1] + 4, 12)
                elif row.combo[1][0] == 12 and row.combo[1][1] <= 3: row.straight = 3
                else: row.straight = 0
                if suit0 == suit1: 
                    row.flush = suit0
                    if row.straight:
                        row.max_combo = (9, [12]) if row.straight == 12 else (8, [row.straight])
                        return
                row.flush = -1
                row.max_combo == (7, [row.combo[1][0]])
                return
def final_card(row, card) -> tuple:
    rank = card // 4
    combo = combos.c5_4(row.combo, rank)
    if combo[0] == 0:
        suit = card % 4
        straight = row.straight
        if straight:
            if combo[1][0] - combo[1][4] <= 4: straight = combo[1][0]
            elif combo[1][0] == 12 and combo[1][1] == 3: straight = 3
            else: straight = 0
        if row.flush == suit:
            if straight == 0:
                return (5, combo[1])
            else:
                return (9, [12]) if straight == 12 else (8, [straight])
        elif straight: 
            return (4, [straight])
    return combo
def final_pair(row, pair) -> tuple:
    rank0, rank1 = pair[0] // 4, pair[1] // 4
    combo = combos.c5_3(row.combo, [rank0, rank1])
    if combo[0] == 0:
        suit0, suit1 = pair[0] % 4, pair[1] % 4
        straight = row.straight
        if straight:
            if combo[1][0] - combo[1][4] <= 4: straight = combo[1][0]
            elif combo[1][0] == 12 and combo[1][1] == 3: straight = 3
            else: straight = 0
        if row.flush == suit0 and suit0 == suit1:
            if straight == 0:
                return (5, combo[1])
            else:
                return (9, [12]) if straight == 12 else (8, [straight])
        elif straight: 
            return (4, [straight])
    return combo

def points2(combo: tuple):
    match combo[0]:
        case 5: return 4
        case 6: return 6
        case 4: return 2
        case 0 | 1 | 2 | 3: return 0
        case 8: return 15
        case 7: return 10
        case 9: return 25
def points1(combo: tuple):
    match combo[0]:
        case 0 | 1 | 2: return 0
        case 3: return 2
        case 4: return 4
        case 5: return 8
        case 6: return 12
        case 8: return 30
        case 7: return 20
        case 9: return 50
def points0(combo: tuple):
    if combo[0] == 0: return 0
    if combo[0] == 1:
        if combo[1][0] < 4: return 0
        if combo[1][0] < 10: return combo[1][0] - 3
        return combo[1][0] - 3 + premium
    return combo[1][0] + 10 + premium

def total(combos):
    if combos[0] <= combos[1] and combos[1] <= combos[2]:
        return points(combos[0], 0) + points(combos[1], 1) + points(combos[2], 2)
    return -6
def set_card_imgs():
    global card_imgs
    card_imgs = []
    card_ranks=('2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace')
    card_suits = ('hearts', 'spades', 'diamonds', 'clubs')
    for i in range(13):
        for j in range(4):
            filename = 'images/' + card_ranks[i] + '_of_' + card_suits[j]
            filename = filename + '2.png' if i > 8 and i < 12 else filename + '.png'
            with Image.open(filename) as f:
                img = ImageTk.PhotoImage(f.resize((card_w - 2, card_h - 2), 2))
                card_imgs.append(img)
def char_to_card(card_char: str):
    card_chars = ['234567890jqka', '@#$%^&*()JQKA', '™£¢∞§¶•ªº∆œ˚å', '€‹›ﬁﬂ‡°·‚ÔŒÅ']
    if card_char:
        for i in range(4):
            ind = card_chars[i].find(card_char)
            if ind >= 0: return ind * 4 + i
    return -1 
def key_pressed(event):
    global deal, deal_
    card = char_to_card(event.char)
    if card >= 0: 
        cards[card].select(event)
    match event.keysym:
        case 'Right' | 'x': rb_value.set((rb_value.get()+3)%9)
        case 'Left' | 'z': rb_value.set((rb_value.get()-3)%9)
        case 'Up' | 's': rb_value.set((rb_value.get()-1)%9)
        case 'Down' | 'S': rb_value.set((rb_value.get()+1)%9)
        case 'f': rb_value.set(9)
        case 'Escape': 
            for card in cards:
                card.state = 'free'
                canvas.coords(card.id,card.x,card.y)
            for player in players: player.reset() 
            fantasy.reset()
            hand_.reset()
            test_deal(seed)
        case 'p': 
            print(f'free cards {len(hand_.cards)} combo {hand_.rows[0].combo}, {hand_.rows[1].combo}, {hand_.rows[2].combo}')
        case 'c':
            match hand_.rows[0].cells + hand_.rows[1].cells + hand_.rows[2].cells:
                case 2: hand_.s4p(fantasy.hand)
                case 3: hand_.s3p_(fantasy.hand)
                case 4: hand_.s3p(fantasy.hand)
                case 5: hand_.s2p_(fantasy.hand, 32)
                case 6: hand_.s2p(fantasy.hand, 16)
                case 7: hand_.s1p_(fantasy.hand, 16)
                case 8: hand_.s1p_(fantasy.hand, 8)
        case 'C':
            match hand_.rows[0].cells + hand_.rows[1].cells + hand_.rows[2].cells:
                case 2:
                    placement = no_fs.s4p(hand_, fantasy.hand)
                    hand_.place_cards(placement)
                case 4:
                    placement = no_fs.s3p(hand_, fantasy.hand)
                    hand_.place_cards(placement)
        case 'n': fantasy.next()
        case 'F': fantasy.fantasy()
        case 'r': 
            if len(fantasy.hand) >= 13: fantasy.sort_fantasy()
        case 'm':
            for row in hand.rows: row.max_comb()
        case 'd': deal_ = deal[:]
        case 'D': deal = deal_
root.bind('<Key>', key_pressed)
class Card:
    def __init__(self, n: int):
        self.n = n
        self.x = root.winfo_width()/2 - (6-self.n // 4) * card_w + 10
        self.y = self.n % 4 * card_h + card_h // 2 + 10
        self.state = 'free'
        self.place = 0
        self.id = canvas.create_image(self.x, self.y, image = card_imgs[n], anchor='center')
        canvas.tag_bind(self.id, "<Button-1>", self.select)
    def select(self, event):
        if self.state == 'free':
            if rb_value.get() < 9:
                p = rb_value.get()//3
                row = rb_value.get()%3
                if players[p].free_cells[row]: 
                    players[p].insert_card(self, row)
                    self.place = (p, row)
                    self.state = 'placed'
                    hand_.cards.remove(self.n)
                    #hand.remove_card(self.n)
                    #if p == 2: hand.add_card(self.n, row)
                    if p == 2:
                        if row:
                            hand_.rows[row].add_card5(self.n)
                        else:
                            hand_.rows[row].add_card3(self.n)
            else: 
                fantasy.insert_card(self)
                hand_.cards.remove(self.n)
                self.state = 'selected'
            return
        if self.state == 'placed':
            p = players[self.place[0]]
            if p.n < 2:
                p.remove_card(self, self.place[1])
                self.state = 'free'
                hand.insert_card(self.n)
            else:
                if rb_value.get() == 9:
                    p.remove_card(self, self.place[1])
                    self.state = 'selected'
                    fantasy.insert_card(self)
                else:
                    p.remove_card(self, self.place[1])
                    self.state = 'free'
                    hand.insert_card(self.n)
            return
        if self.state == 'selected':
            if rb_value.get() == 9:
                fantasy.remove_card(self)
                self.state = 'free'
            else:
                p = rb_value.get()//3
                row = rb_value.get()%3
                if p == 2 and players[2].free_cells[row]:
                    if row:
                        hand_.rows[row].add_card5(self.n)
                    else:
                        hand_.rows[row].add_card3(self.n)
                    #hand.add_card(self.n, row)
                    #hand.remove_card(self.n)
                    players[2].insert_card(self, row)
                    self.state = 'placed'
                    self.place = (2, row)
                    fantasy.remove_card(self)
class Player:
    def __init__(self, n: int):
        self.n = n
        self.x = 50 + 800 * (n % 2) + 420 * (n // 2)
        self.y = 300 + 300 * (n // 2)
        self.x1, self.y1 = [self.x + 1.5*card_w, self.x + 0.5*card_w, self.x + 0.5*card_w], [self.y + 0.5*card_h, self.y + 1.5*card_h, self.y + 2.5*card_h]
        self.rows = [[], [], []]
        self.combos = [(0, []), (0, []), (0, [])]
        self.free_cells = [3, 5, 5]
        self.points = [0, 0, 0]
        
        self.combo_id, self.point_id, rb_labels = [], [], ['High', 'Mid', 'Low']
        for c in range(1,4): canvas.create_rectangle(self.x + card_w*c,self.y,         self.x+card_w*(c+1),self.y + card_h)
        for c in range(0,5): canvas.create_rectangle(self.x + card_w*c,self.y+card_h,  self.x+card_w*(c+1),self.y + card_h*2)
        for c in range(0,5): canvas.create_rectangle(self.x + card_w*c,self.y+card_h*2,self.x+card_w*(c+1),self.y + card_h*3)
        for i in range(3): 
            rb = Radiobutton(text=rb_labels[i], variable=rb_value, value=3*self.n+i, indicatoron=False)
            canvas.create_window(self.x-card_w, self.y+card_h*i, window=rb, width=card_w-5, height=card_h, anchor='nw')
            self.combo_id.append(canvas.create_text((self.x+5*card_w+10,self.y+i*card_h), text='', anchor='nw'))
            self.point_id.append(canvas.create_text((self.x+5*card_w+10,self.y+i*card_h+20), text='', anchor='nw'))
        self.total_id = canvas.create_text((self.x+2*card_w,self.y), text='', anchor='sw')
    def reset(self):
        self.rows = [[], [], []]
        self.combos = [(0, []), (0, []), (0, [])]
        self.free_cells = [3, 5, 5]
        self.points = [0, 0, 0]
        for item in self.combo_id: canvas.itemconfig(item, text='')
        for item in self.point_id: canvas.itemconfig(item, text='')
        canvas.itemconfig(self.total_id, text='')
    def insert_card(self, card, row):
        shift = 0.5 if row == 0 else -0.5
        self.rows[row].append(card.n)
        canvas.coords(card.id, (self.x+card_w*(len(self.rows[row])+shift),self.y+card_h*(row+0.5)))
        self.free_cells[row] -= 1
        if self.free_cells[row] == 0:
            self.combos[row] = combo_final(self.rows[row]) if row else high_final(self.rows[row])
            c_to_s = combo_to_str(self.combos[row])
            self.points[row] = points(self.combos[row], row)
            if self.points[row] > 0: canvas.itemconfig(self.point_id[row], text=f'+{self.points[row]}')
            canvas.itemconfig(self.combo_id[row], text=c_to_s)
        if total(self.combos) > 0: canvas.itemconfig(self.total_id, text=f'+{str(total(self.combos))}')
    def remove_card(self, card, row):
        self.rows[row].remove(card.n)
        self.free_cells[row] += 1
        self.sort_cards(row)
    def sort_cards(self, row):
        shift = 1.5 if row == 0 else 0.5
        for i in range(len(self.rows[row])):
            n = self.rows[row][i]
            canvas.coords(cards[self.rows[row][i]].id, (self.x+card_w*(i+shift)),self.y+card_h*(row+0.5))
class Fantasy:
    def __init__(self):
        self.point = (240, 510)
        self.hand = []
        self.dropped = []
        self.step = 0
        self.sort = 'suit'


        self.radiobutton = Radiobutton(text = 'Fantasy',  variable=rb_value, value=9, bg='lightgreen')
        self.sort_button = Button(text = 'Sort', bg='lightgreen', command=self.sort_fantasy)
        self.next_button = Button(text = 'Next', bg='lightgreen', command=self.next)
        self.calc_button = Button(text = 'Calc', bg='lightgreen', command=self.calc, state='disabled')
        
        canvas.create_window(self.point[0]-100, self.point[1], window=self.radiobutton, anchor='nw')
        canvas.create_window(self.point[0]-100, self.point[1]+30, window=self.sort_button, anchor='nw')
        canvas.create_window(self.point[0]+100, self.point[1]-30, window=self.next_button, anchor='nw')
        canvas.create_window(self.point[0]+450, self.point[1]-30, window=self.calc_button, anchor='nw')
  
    def insert_card(self, card):
        canvas.coords(card.id, (self.point[0]+card_w*(len(self.hand)+0.5),self.point[1]+card_h*0.5))
        self.hand.append(card.n)  
        if len(self.hand) >= 13: self.calc_button.config(state='normal')
        else: self.calc_button.config(state='disabled')
    def drop_card(self, card):
        self.dropped.append(card.n)
        canvas.coords(card.id, (self.point[0]+card_w*((len(self.dropped)+12)),self.point[1]+card_h*0.5))
    def remove_card(self, card):
        if card.n in self.hand:
            self.hand.remove(card.n)
            self.sort_cards()
    def sort_cards(self):
        for i in range(len(self.hand)):
            canvas.coords(cards[self.hand[i]].id, (self.point[0]+card_w*(i+0.5)),self.point[1]+card_h*0.5)
   
    def reset(self):
        self.hand = []
        self.dropped = []
        self.step = 0
        self.calc_button.config(state='disabled')
        rb_value.set(8)
        test_deal(seed)
    def sort_fantasy(self):
        suits = Counter([item % 4 for item in self.hand])
        if self.sort == 'rank': 
            self.hand.sort(reverse=True, key=lambda item: (item // 4, item % 4))
            self.sort = 'suit'
        else: 
            self.hand.sort(reverse=True, key=lambda item: (suits[item % 4], item % 4, item // 4))
            self.sort = 'rank'
        for i in range(len(self.hand)):
            canvas.coords(cards[self.hand[i]].id, (self.point[0]+card_w*(i+0.5)),self.point[1]+card_h*0.5)

    def next(self):
        match self.step:
            case 0: 
                for i in range(5): 
                    card = cards[deal[i]]
                    #hand.deal.append(card.n)
                    card.state = 'selected'
                    fantasy.insert_card(card)
                    hand_.cards.remove(card.n)

            case 1:
                for p in range(2):
                    for c in range(5):
                        ind = p*5+5+c
                        card = cards[deal[ind]]
                        players[p].insert_card(card, 1)
                        card.place = (p, 1)
                        card.state = 'placed'
                        #hand.remove_card(card.n)
                        hand_.cards.remove(card.n)
                for i in range(3): 
                    card = cards[deal[15+i]]
                    fantasy.insert_card(card)
                    card.state = 'selected'
                    #hand.deal.append(card.n)
                    hand_.cards.remove(card.n)
            case 2:
                for item in fantasy.hand: 
                    card = cards[item]
                    self.remove_card(card)
                    card.state ='dropped'
                    #hand.remove_card(card.n)
                    self.drop_card(cards[item])
                for p in range(2):
                    for c in range(2):
                        ind = p*2+c+18
                        card = cards[deal[ind]]
                        players[p].insert_card(card, 2)
                        card.place = (p, 2)
                        card.state = 'placed'
                        #hand.remove_card(card.n)
                        hand_.cards.remove(card.n)
                for i in range(3): 
                    card = cards[deal[22+i]]
                    fantasy.insert_card(card)
                    card.state = 'selected'
                    #hand.deal.append(card.n)
                    hand_.cards.remove(card.n)
            case 3:
                for item in fantasy.hand: 
                    card = cards[item]
                    fantasy.remove_card(card)
                    card.state ='dropped'
                    #hand.remove_card(card.n)
                    self.drop_card(cards[item])
                for p in range(2):
                    for c in range(2):
                        ind = p*2+c+25
                        card = cards[deal[ind]]
                        players[p].insert_card(card, 2)
                        card.place = (p, 2)
                        card.state = 'placed'
                        #hand.remove_card(card.n)
                        hand_.cards.remove(card.n)
                for i in range(3): 
                    card = cards[deal[29+i]]
                    fantasy.insert_card(card)
                    card.state = 'selected'
                    #hand.deal.append(card.n)
                    hand_.cards.remove(card.n)
            case 4:
                for item in fantasy.hand: 
                    card = cards[item]
                    fantasy.remove_card(card)
                    card.state ='dropped'
                    #hand.remove_card(card.n)
                    self.drop_card(cards[item])
                for p in range(2):
                    for c in range(2):
                        ind = p*2+c+32
                        card = cards[deal[ind]]
                        players[p].insert_card(card, 0)
                        card.place = (p, 0)
                        card.state = 'placed'
                        #hand.remove_card(card.n)
                        hand_.cards.remove(card.n)
                for i in range(3): 
                    card = cards[deal[36+i]]
                    fantasy.insert_card(card)
                    card.state = 'selected'
                    #hand.deal.append(card.n)
                    hand_.cards.remove(card.n)
            case 5:
                for item in fantasy.hand: 
                    card = cards[item]
                    fantasy.remove_card(card)
                    card.state ='dropped'
                    #hand.remove_card(card.n)
                    self.drop_card(cards[item])
                for p in range(2):
                        ind = p*2+39
                        card = cards[deal[ind]]
                        players[p].insert_card(card, 0)
                        card.place = (p, 0)
                        card.state = 'placed'
                        hand_.cards.remove(card.n)
                        card = cards[deal[ind+1]]
                        players[p].insert_card(card, 2)
                        card.place = (p, 2)
                        card.state = 'placed'
                        #hand.remove_card(card.n)
                        hand_.cards.remove(card.n)
        self.step += 1

    def high_row(self, free_cards: list):
        sets = list(combinations(free_cards, 3))
        result = []
        for item in sets:
            ranks = [r // 4 for r in item]
            counter = Counter(ranks).most_common()
            match len(counter):
                case 3: result.append([0, tuple(sorted(ranks, reverse=True)), set(item)])
                case 2: result.append([1, (counter[0][0], counter[1][0]), set(item)])
                case 1: result.append([3, (ranks[0],), set(item)])
        return result

    def fantasy(self, size = 14):
        rb_value.set(9)
        deck = list(range(52))
        random.seed()
        sample = random.sample(deck, size)
        for n in sample: 
            self.insert_card(cards[n])

    def calc(self):
        straights = ({12,11,10,9,8}, {11,10,9,8,7}, {10,9,8,7,6}, {9,8,7,6,5}, {8,7,6,5,4},{7,6,5,4,3},{6,5,4,3,2},{5,4,3,2,1},{4,3,2,1,0},{3,2,1,0,12})
        result = []
        rank_dict = {}
        suit_dict = {}
        
        for card in self.hand:
            if card // 4 in rank_dict: rank_dict[card // 4].append(card % 4)
            else: rank_dict[card // 4] = [card % 4]
            if card % 4 in suit_dict: suit_dict[card % 4].append(card // 4)
            else: suit_dict[card % 4] = [card // 4]
        
        for key in suit_dict:
            if len(suit_dict[key]) >= 5:
                if straights[0] <= set(suit_dict[key]): 
                    result.append([9, (12,), set(item * 4 + key for item in straights[0])])
                for i in range(1, len(straights)):
                    if straights[i] <= set(suit_dict[key]): 
                        result.append([8, (12 - i,), set(item * 4 + key for item in straights[i])])
                for item in list(combinations(suit_dict[key], 5)):
                    result.append([5, item, set(i * 4 + key for i in item)])
        
        for key in rank_dict:
            if len(rank_dict[key]) == 4:
                result.append([7, (key,), set(key * 4 + suit for suit in rank_dict[key])])
            if len(rank_dict[key]) >= 3:
                sets = list(combinations(rank_dict[key], 3))
                for item in sets: result.append([3, (key,), set(key * 4 + suit for suit in item)])
            if len(rank_dict[key]) >= 2:
                pairs = list(combinations(rank_dict[key], 2))
                for item in pairs: result.append([1, (key,), set(key * 4 + suit for suit in item)])
        
        sets = list([item for item in result if item[0] == 3])
        pairs = list([item for item in result if item[0] == 1])
        sets.sort(reverse=True)
        pairs.sort(reverse=True)
        for s in sets:
            for p in pairs:
                if s[1][0] != p[1][0]: result.append([6, (s[1][0], p[1][0]), s[2] | p[2]])
        for i1 in range(len(pairs) - 1):
            for i2 in range(i1 + 1, len(pairs)):
                if pairs[i1] >= pairs[i2]: result.append([2, (pairs[i1][1][0], pairs[i2][1][0]), pairs[i1][2] | pairs[i2][2]])
        ranks = set(rank_dict.keys())
        for i in range(len(straights)):
            if straights[i] <= ranks:
                suits = []
                for item in straights[i]: suits.append(rank_dict[item])
                rows = list(product(*suits))
                for item in rows: result.append([4, (12 - i,), set(map(lambda r, s: r * 4 + s, straights[i], item))])
        
        result.sort(reverse=True, key=lambda item: (item[0], item[1]))
        for item in result: print(item)
        print('\n')
        results = []
        for i2 in range(len(result) - 1):
            hand2 = result[i2]
            for i1 in range(i2+1, len(result)):
                hand1 = result[i1]
                if hand2[2].isdisjoint(hand1[2]):
                    free_cards = set(self.hand) - hand1[2] - hand2[2]
                    hand0 = self.high_row(free_cards)
                    hand0.sort(reverse=True, key=lambda x: (x[0], x[1]))
                    if hand0[0] <= hand1:
                        p = points(hand0[0], 0) + points(hand1, 1) + points(hand2, 2)
                        results.append([p, hand0[0], hand1, hand2])
        results.sort(reverse=True, key=lambda item: (item[0], item[3], item[1]))
        for item in results: 
            print(f'{item[0]}: {item[1][0]} {show_cards(list(item[1][2]))}, {item[2][0]} {show_cards(list(item[2][2]))}, {item[3][0]} {show_cards(list(item[3][2]))}')
        print('\n')
        hand = results[0]
        for row in range(3):
            for n in hand[row + 1][2]: players[2].insert_card(cards[n], row)

class Row_:
    def __init__(self, row: int):
        self.row = row
        match row:
            case 0:
                self.max_cells = 3
                self.add_card = self.add_card3
                self.add_pair = self.add_pair3
                self.get_points = self.points0
            case 1:
                self.max_cells = 5
                self.add_card = self.add_card5
                self.add_pair = self.add_pair5
                self.get_points = self.points1
            case 2:
                self.max_cells = 5
                self.add_card = self.add_card5
                self.add_pair = self.add_pair5
                self.get_points = self.points2
        self.reset()

    def reset(self):
        self.cells = self.max_cells
        self.flush = -1
        self.straight = 0
        self.combo = (-1, [0])
        self.max_combo = (9, [12])
        self.points = 0
    def points2(self):
        match self.combo[0]:
            case 5: return 4
            case 6: return 6
            case 4: return 2
            case 0 | 1 | 2 | 3: return 0
            case 8: return 15
            case 7: return 10
            case 9: return 25
    def points1(self):
        match self.combo[0]:
            case 0 | 1 | 2: return 0
            case 3: return 2
            case 4: return 4
            case 5: return 8
            case 6: return 12
            case 8: return 30
            case 7: return 20
            case 9: return 50
    def points0(self):
        if self.combo[0] == 0: return 0
        elif self.combo[0] == 1:
            if self.combo[1][0] < 4: return 0
            if self.combo[1][0] < 10: return self.combo[1][0] - 3
            return self.combo[1][0] - 3 + premium
        return self.combo[1][0] + 10 + premium

    def add_card5(self, card):
        self.cells -= 1
        rank, suit = card // 4, card % 4
        match self.cells:
            case 0:
                self.combo = combos.c5_4(self.combo, rank)
                match self.combo[0]:
                    case 0:
                        if self.straight:
                            if self.combo[1][0] - self.combo[1][4] <= 4: self.straight = self.combo[1][0]
                            elif self.combo[1][0] == 12 and self.combo[1][1] == 3: self.straight = 3
                            else: self.straight = 0
                        if self.flush == suit:
                            if self.straight == 0:
                                self.combo = (5, self.combo[1])
                                self.max_combo = self.combo
                                self.points = self.get_points()
                                return
                            else:
                                self.combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                                self.max_combo = self.combo
                                self.points = self.get_points()
                                return
                        elif self.straight: 
                            self.combo = (4, [self.straight])
                            self.max_combo = self.combo
                            self.points = self.get_points()
                            return
                self.max_combo = self.combo
                self.points = self.get_points()
                return
            case 1:
                self.combo = combos.c4_3(self.combo, rank)
                match self.combo[0]:
                    case 0:
                        if self.straight:
                            if self.combo[1][0] - self.combo[1][3] <= 4: self.straight = min(self.combo[1][3] + 4, 12)
                            elif self.combo[1][0] == 12 and self.combo[1][1] <= 3: self.straight = 3
                            else: self.straight = 0
                        if self.flush == suit:
                            if self.straight == 0:
                                self.max_combo = (5, [12])
                                return
                            else:
                                self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                                return
                        else:
                            self.flush = -1
                            if self.straight: 
                                self.max_combo = (4, [self.straight])
                                return
                            else:
                                self.max_combo = (1, self.combo[1])
                                return
                    case 1:
                        self.straight = 0
                        self.flush = -1
                        self.max_combo = (3, self.combo[1])
                        return
                    case 2:
                        self.max_combo = (6, self.combo[1])
                        return
                    case 3:
                        self.max_combo = (7, self.combo[1])
                        return
            case 2:
                self.combo = combos.c3_2(self.combo, rank)
                if self.combo[0] == 0:
                    if self.straight:
                        if self.combo[1][0] - self.combo[1][2] <= 4: self.straight = min(self.combo[1][1] + 4, 12)
                        elif self.combo[1][0] == 12 and self.combo[1][1] <= 3: self.straight = 3
                        else: self.straight = 0
                    if self.flush == suit:
                        if self.straight == 0:
                            self.max_combo = (5, [12])
                            return
                        else:
                            self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                            return
                    else: 
                        self.flush = -1
                        if self.straight:
                            self.max_combo = (4, [self.straight])
                            return
                        self.max_combo = (3, self.combo[1])
                        return
                else:
                    self.straight = 0
                    self.flush = -1
                    self.max_combo = (7, self.combo[1])
                    return
            case 3:
                if self.combo[1][0] == rank:
                    self.straight = 0
                    self.flush = -1
                    self.combo = (1, [rank])
                    self.max_combo = (7, [rank])
                    return
                else:
                    self.combo = (0, [self.combo[1][0], rank]) if self.combo[1][0] > rank else (0, [rank, self.combo[1][0]])
                    if self.combo[1][0] - self.combo[1][1] <= 4: self.straight = min(self.combo[1][1] + 4, 12)
                    elif self.combo[1][0] == 12 and self.combo[1][1] <= 3: self.straight = 3
                    else: self.straight = 0
                    if self.flush == suit:
                        if self.straight == 0:
                            self.max_combo = (7, [self.combo[1][0]])
                            return
                        else:
                            self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                            return
                    else: 
                        self.flush = -1
                        self.max_combo = (7, self.combo[1])
                    return
            case 4:
                self.combo = (0, [rank])
                self.flush = suit
                self.straight = min(rank + 4, 12)
                self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
    def add_card3(self, card):
        self.cells -= 1
        rank = card // 4
        match self.cells:
            case 0:
                self.combo = combos.c3_2(self.combo, rank)
                self.points = self.get_points()
                return
            case 1:
                if self.combo[1][0] == rank: 
                    self.combo = (1, [rank])
                    return
                else:
                    self.combo = (0, [self.combo[1][0], rank]) if self.combo[1][0] > rank else (0, [rank, self.combo[1][0]])
                    return
            case 2:
                self.combo = (0, [rank])
    def add_pair5(self, pair: list):
        self.cells -= 2
        rank0, rank1 = pair[0] // 4, pair[1] // 4
        suit0, suit1 = pair[0] % 4, pair[1] % 4
        match self.cells:
            case 0:
                self.combo = combos.c5_3(self.combo, [rank0, rank1])
                match self.combo[0]:
                    case 0:
                        if self.straight:
                            if self.combo[1][0] - self.combo[1][4] <= 4: self.straight = self.combo[1][0]
                            elif self.combo[1][0] == 12 and self.combo[1][1] == 3: self.straight = 3
                            else: self.straight = 0
                        if self.flush == suit0 and suit0 == suit1:
                            if self.straight == 0:
                                self.combo = (5, self.combo[1])
                                self.max_combo = self.combo
                                self.points = self.get_points()
                                return
                            else:
                                self.combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                                self.max_combo = self.combo
                                self.points = self.get_points()
                                return
                        elif self.straight: 
                            self.combo = (4, [self.straight])
                            self.max_combo = self.combo
                            self.points = self.get_points()
                            return
                self.max_combo = self.combo
                self.points = self.get_points()
                return
            case 1:
                self.combo = combos.c4_2(self.combo, [rank0, rank1])
                match self.combo[0]:
                    case 0:
                        if self.straight:
                            if self.combo[1][0] - self.combo[1][3] <= 4: self.straight = min(self.combo[1][3] + 4, 12)
                            elif self.combo[1][0] == 12 and self.combo[1][1] <= 3: self.straight = 3
                            else: self.straight = 0
                        if self.flush == suit0 and suit0 == suit1:
                            if self.straight == 0:
                                self.max_combo = (5, [12])
                                return
                            else:
                                self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                                return
                        else:
                            self.flush = -1
                            if self.straight: 
                                self.max_combo = (4, [self.straight])
                                return
                            else:
                                self.max_combo = (1, self.combo[1])
                                return
                    case 1:
                        self.straight = 0
                        self.flush = -1
                        self.max_combo = (3, self.combo[1])
                        return
                    case 2:
                        self.max_combo = (6, self.combo[1])
                        return
                    case 3:
                        self.max_combo = (7, self.combo[1])
                        return
            case 2:
                self.combo = combos.c3_1(self.combo, [rank0, rank1])
                if self.combo[0] == 0:
                    if self.combo[1][0] - self.combo[1][2] <= 4: self.straight = min(self.combo[1][1] + 4, 12)
                    elif self.combo[1][0] == 12 and self.combo[1][1] <= 3: self.straight = 3
                    else: self.straight = 0
                    if self.flush == suit0 and suit0 == suit1:
                        if self.straight == 0:
                            self.max_combo = (5, [12])
                            return
                        else:
                            self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                            return
                    else: 
                        self.flush = -1
                        if self.straight:
                            self.max_combo = (4, [self.straight])
                            return
                        self.max_combo = (3, self.combo[1])
                        return
                else:
                    self.straight = 0
                    self.flush = -1
                    self.max_combo = (7, self.combo[1])
                    return
            case 3:
                if rank0 == rank1:
                    self.straight = 0
                    self.flush = -1
                    self.combo = (1, [rank0])
                    self.max_combo = (7, [rank0])
                    return
                else:
                    self.combo = (0, [rank0, rank1]) if rank0 > rank1 else (0, [rank1, rank0])
                    if self.combo[1][0] - self.combo[1][1] <= 4: self.straight = min(self.combo[1][1] + 4, 12)
                    elif self.combo[1][0] == 12 and self.combo[1][1] <= 3: self.straight = 3
                    else: self.straight = 0
                    if suit0 == suit1:
                        self.flush = suit0
                        if self.straight == 0:
                            self.max_combo = (7, [self.combo[1][0]])
                            return
                        else:
                            self.max_combo = (9, [12]) if self.straight == 12 else (8, [self.straight])
                            return
                    else: 
                        self.flush = -1
                        self.max_combo = (7, self.combo[1])
                        return
    def add_pair3(self, pair: list):
        self.cells -= 2
        rank0, rank1 = pair[0] // 4, pair[1] // 4
        if self.cells == 0:
            self.combo = combos.c3_1(self.combo, [rank0, rank1])
            self.points = self.get_points()
            return
        else:
            if rank0 == rank1:
                self.combo = (1, [rank0])
                return
            self.combo = (0, [rank0, rank1]) if rank0 > rank1 else (0, [rank1, rank0])
            return
    def final_card(self, card) -> tuple:
        rank = card // 4
        combo = combos.c5_4(self.combo, rank)
        if combo[0] == 0:
            suit = card % 4
            straight = self.straight
            if straight:
                if combo[1][0] - combo[1][4] <= 4: straight = combo[1][0]
                elif combo[1][0] == 12 and combo[1][1] == 3: straight = 3
                else: straight = 0
            if self.flush == suit:
                if straight == 0:
                    return (5, combo[1])
                else:
                    return (9, [12]) if straight == 12 else (8, [straight])
            elif straight: 
                return (4, [straight])
        return combo
    def final_pair(self, pair) -> tuple:
        rank0, rank1 = pair[0] // 4, pair[1] // 4
        combo = combos.c5_3(self.combo, [rank0, rank1])
        if combo[0] == 0:
            suit0, suit1 = pair[0] % 4, pair[1] % 4
            straight = self.straight
            if straight:
                if combo[1][0] - combo[1][4] <= 4: straight = combo[1][0]
                elif combo[1][0] == 12 and combo[1][1] == 3: straight = 3
                else: straight = 0
            if self.flush == suit0 and suit0 == suit1:
                if straight == 0:
                    return (5, combo[1])
                else:
                    return (9, [12]) if straight == 12 else (8, [straight])
            elif straight: 
                return (4, [straight])
        return combo

class Hand_:
    def __init__(self):
        self.rows = [Row_(0), Row_(1), Row_(2)]
        self.cards = list(range(52))
        self.reset()
    def reset(self):
        for row in self.rows: row.reset()
        self.cards = list(range(52))
    def place_cards(self, placement):
        if placement:
            for pair in placement:
                card, row = pair[0], pair[1]
                match row:
                    case 0: add_card3(self.rows[row], card)
                    case 1 | 2: add_card5(self.rows[row], card)
                #self.rows[pair[1]].add_card(pair[0])
                players[2].insert_card(cards[card], row)
                cards[pair[0]].state = 'placed'
                fantasy.remove_card(cards[card])
    def s4(self, hand, deal: list):
        pairs = list(combinations(deal, 2))
        if hand.rows[0].cells == 2:
            max_combo = hand.rows[0].combo
            for pair in pairs:
                combo = combos.c3_1(hand.rows[0].combo, [pair[0]//4, pair[1]//4])
                if combo <= hand.rows[1].combo and combo > max_combo: max_combo = combo
            return points0(max_combo) + hand.rows[1].points + hand.rows[2].points if max_combo > hand.rows[0].combo else penalty
        if hand.rows[1].cells == 2:
            max_combo = hand.rows[1].combo
            for pair in pairs:
                combo = final_pair(hand.rows[1], pair)
                if combo <= hand.rows[2].combo and combo >= hand.rows[0].combo and combo > max_combo: max_combo = combo
            return points1(max_combo) + hand.rows[0].points + hand.rows[2].points if max_combo > hand.rows[1].combo else penalty
        if hand.rows[2].cells == 2:
            max_combo = hand.rows[2].combo
            for pair in pairs:
                combo = final_pair(hand.rows[2], pair)
                if combo >= hand.rows[1].combo and combo > max_combo: max_combo = combo
            return points2(max_combo) + hand.rows[0].points + hand.rows[1].points if max_combo > hand.rows[2].combo else penalty
        if hand.rows[0].cells and hand.rows[1].cells:
            max_points = penalty
            for pair in pairs:
                combo0 = combos.c3_2(hand.rows[0].combo, pair[0] // 4)
                combo1 = final_card(hand.rows[1], pair[1])
                if combo1 >= combo0 and hand.rows[2].combo >= combo1:
                    points = points0(combo0) + points1(combo1)
                    if points > max_points: max_points = points
                combo0 = combos.c3_2(hand.rows[0].combo, pair[1] // 4)
                combo1 = final_card(hand.rows[1], pair[0])
                if combo1 >= combo0 and hand.rows[2].combo >= combo1:
                    points = points0(combo0) + points1(combo1)
                    if points > max_points: max_points = points
            return max_points + hand.rows[2].points if max_points > penalty else penalty
        if hand.rows[0].cells and hand.rows[2].cells:
            max_points = penalty
            for pair in pairs:
                combo0 = combos.c3_2(hand.rows[0].combo, pair[0] // 4)
                combo2 = final_card(hand.rows[2], pair[1])
                if hand.rows[1].combo >= combo0 and combo2 >= hand.rows[1].combo:
                    points = points0(combo0) + points2(combo2)
                    if points > max_points: max_points = points
                combo0 = combos.c3_2(hand.rows[0].combo, pair[1] // 4)
                combo2 = final_card(hand.rows[2], pair[0])
                if hand.rows[1].combo >= combo0 and combo2 >= hand.rows[1].combo:
                    points = points0(combo0) + points2(combo2)
                    if points > max_points: max_points = points
            return max_points + hand.rows[1].points if max_points > penalty else penalty
        if hand.rows[1].cells and hand.rows[2].cells:
            max_points = penalty
            for pair in pairs:
                combo1 = final_card(hand.rows[1], pair[0])
                combo2 = final_card(hand.rows[2], pair[1])
                if combo1 >= hand.rows[0].combo and combo2 >= combo1:
                    points = points1(combo1) + points2(combo2)
                    if points > max_points: max_points = points
                combo1 = final_card(hand.rows[1], pair[1])
                combo2 = final_card(hand.rows[2], pair[0])
                if combo1 >= hand.rows[0].combo and combo2 >= combo1:
                    points = points1(combo1) + points2(combo2)
                    if points > max_points: max_points = points
            return max_points + hand.rows[0].points if max_points > penalty else penalty
    def s4p(self, deal: list):
        placement = 0
        pairs = combinations(deal, 2)
        if self.rows[0].cells == 2:
            row = self.rows[0]
            max_combo = row.combo
            for pair in pairs:
                rank0, rank1 = pair[0] // 4, pair[1] // 4
                combo = combos.c3_1(row.combo, [rank0, rank1])
                if combo <= self.rows[1].combo and combo > max_combo:
                    max_combo = combo
                    placement = ([pair[0], 0], [pair[1], 0])

        if self.rows[1].cells == 2:
            row = self.rows[1]
            max_combo = row.combo
            for pair in pairs:
                combo = row.final_pair(pair)
                if combo <= self.rows[2].combo and combo >= self.rows[0].combo and combo > max_combo:
                    max_combo = combo
                    placement = ([pair[0], 1], [pair[1], 1])

        if self.rows[2].cells == 2:
            row = self.rows[2]
            max_combo = row.combo
            for pair in pairs:
                combo = row.final_pair(pair)
                if combo >= self.rows[1].combo and combo > max_combo:
                    max_combo = combo
                    placement = ([pair[0], 2], [pair[1], 2])

        if self.rows[0].cells and self.rows[1].cells:
            max_points = penalty
            row0 = self.rows[0]
            row1 = self.rows[1]
            for pair in pairs:
                combo0 = combos.c3_2(row0.combo, pair[0] // 4)
                combo1 = row1.final_card(pair[1])
                if combo1 >= combo0 and self.rows[2].combo >= combo1:
                    points = points0(combo0) + points1(combo1) + self.rows[2].points
                    if points > max_points: 
                        max_points = points
                        placement = ([pair[0], 0], [pair[1], 1])
                combo0 = combos.c3_2(row0.combo, pair[1] // 4)
                combo1 = row1.final_card(pair[0])
                if combo1 >= combo0 and self.rows[2].combo >= combo1:
                    points = points0(combo0) + points1(combo1) + self.rows[2].points
                    if points > max_points:
                        max_points = points
                        placement = ([pair[0], 1], [pair[1], 0])

        if self.rows[0].cells and self.rows[2].cells:
            max_points = penalty
            row0 = self.rows[0]
            row2 = self.rows[2]
            for pair in pairs:
                combo0 = combos.c3_2(row0.combo, pair[0] // 4)
                combo2 = row2.final_card(pair[1])
                if self.rows[1].combo >= combo0 and combo2 >= self.rows[1].combo:
                    points = points0(combo0) + points2(combo2) + self.rows[1].points
                    if points > max_points:
                        max_points = points
                        placement = ([pair[0], 0], [pair[1], 2])
                combo0 = combos.c3_2(row0.combo, pair[1] // 4)
                combo2 = row2.final_card(pair[0])
                if self.rows[1].combo >= combo0 and combo2 >= self.rows[1].combo:
                    points = points0(combo0) + points2(combo2) + self.rows[1].points
                    if points > max_points:
                        max_points = points
                        placement = ([pair[1], 0], [pair[0], 2])

        if self.rows[1].cells and self.rows[2].cells:
            max_points = penalty
            row1 = self.rows[1]
            row2 = self.rows[2]
            for pair in pairs:
                combo1 = row1.final_card(pair[0])
                combo2 = row2.final_card(pair[1])
                if combo1 >= self.rows[0].combo and combo2 >= combo1:
                    points = self.rows[0].points + points1(combo1) + points2(combo2)
                    if points > max_points:
                        max_points = points
                        placement = ([pair[0], 1], [pair[1], 2])
                combo1 = row1.final_card(pair[1])
                combo2 = row2.final_card(pair[0])
                if combo1 >= self.rows[0].combo and combo2 >= combo1:
                    points = self.rows[0].points + points1(combo1) + points2(combo2)
                    if points > max_points:
                        max_points = points
                        placement = ([pair[1], 1], [pair[0], 2])
        self.place_cards(placement)
    def s3p(self, deal: list):
        start = dt.now()
        pairs = list(combinations(deal, 2))
        next_deals = list(combinations(self.cards, 3))
        max_points = penalty * len(next_deals)
        placement = 0

        if self.rows[0].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair3(h.rows[0], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 0])
        if self.rows[1].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair5(h.rows[1], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 1])
        if self.rows[2].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair5(h.rows[2], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 2])
        if self.rows[0].cells and self.rows[1].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[1], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 1])
                h = deepcopy(self)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[1], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 0])
        if self.rows[0].cells and self.rows[2].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 2])
                h = deepcopy(self)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 0])
        if self.rows[1].cells and self.rows[2].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card5(h.rows[1], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 2])
                h = deepcopy(self)
                add_card5(h.rows[1], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 1])
        print(f'elapsed time for 4 free cells {(dt.now() - start).total_seconds()}')
        self.place_cards(placement)
    def s3(self, hand, deal: list, sample):
        pairs = list(combinations(deal, 2))
        next_deals = random.sample(list(combinations(hand.cards, 3)), sample)
        max_points = penalty * sample

        if hand.rows[0].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair3(h.rows[0], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
        if hand.rows[1].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair5(h.rows[1], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
        if hand.rows[2].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair5(h.rows[2], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
        if hand.rows[0].cells and hand.rows[1].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[1], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[1], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
        if hand.rows[0].cells and hand.rows[2].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
        if hand.rows[1].cells and hand.rows[2].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card5(h.rows[1], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card5(h.rows[1], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s4(h, next_deal)
                    if r > max_points:
                        max_points = r
        return max_points
    def s2p(self, deal: list, sample):
        start = dt.now()
        pairs = list(combinations(deal, 2))
        next_deals = random.sample(list(combinations(self.cards, 3)), sample)
        max_points = penalty * len(next_deals)
        placement = 0

        if self.rows[0].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair3(h.rows[0], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 0])
        if self.rows[1].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair5(h.rows[1], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 1])
        if self.rows[2].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair5(h.rows[2], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 2])
        if self.rows[0].cells and self.rows[1].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[1], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 1])
                h = deepcopy(self)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[1], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 0])
        if self.rows[0].cells and self.rows[2].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 2])
                h = deepcopy(self)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 0])
        if self.rows[1].cells and self.rows[2].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card5(h.rows[1], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 2])
                h = deepcopy(self)
                add_card5(h.rows[1], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 1])
        print(f'elapsed time for 6 free cells {(dt.now() - start).total_seconds()}')
        self.place_cards(placement)
    def s2(self, hand, deal: list, sample):
        pairs = list(combinations(deal, 2))
        next_deals = random.sample(list(combinations(hand.cards, 3)), sample)
        max_points = penalty * sample * sample // 2

        if hand.rows[0].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair3(h.rows[0], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[1].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair5(h.rows[1], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[2].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair5(h.rows[2], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[0].cells and hand.rows[1].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[1], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[1], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[0].cells and hand.rows[2].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[1].cells and hand.rows[2].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card5(h.rows[1], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card5(h.rows[1], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        return max_points
    def s2p_(self, pair: list, sample):
        start = dt.now()
        next_deals = random.sample(list(combinations(self.cards, 3)), sample)
        max_points = penalty * sample * sample
        placement = 0

        if self.rows[0].cells:
            for card in pair:
                hand_c = deepcopy(self)
                hand_c.rows[0].add_card3(card)
                if hand_c.rows[0].combo <= hand_c.rows[1].max_combo and hand_c.rows[1].combo <= hand_c.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(hand_c, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = [[card, 0]]
        if self.rows[1].cells:
            for card in pair:
                hand_c = deepcopy(self)
                hand_c.rows[1].add_card5(card)
                if hand_c.rows[0].combo <= hand_c.rows[1].max_combo and hand_c.rows[1].combo <= hand_c.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(hand_c, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = [[card, 1]]
        if self.rows[2].cells >= 2:
            for card in pair:
                hand_c = deepcopy(self)
                hand_c.rows[2].add_card5(card)
                if hand_c.rows[0].combo <= hand_c.rows[1].max_combo and hand_c.rows[1].combo <= hand_c.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s3(hand_c, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = [[card, 2]]
        print(f'elapsed time for 5 free cells {(dt.now() - start).total_seconds()} seconds')
        self.place_cards(placement)
    def s1p_(self, pair: list, sample):
        start = dt.now()
        next_deals = random.sample(list(combinations(self.cards, 3)), sample)
        max_points = penalty * 10000
        placement = 0

        if self.rows[0].cells:
            for card in pair:
                hand_c = deepcopy(self)
                hand_c.rows[0].add_card3(card)
                if hand_c.rows[0].combo <= hand_c.rows[1].max_combo and hand_c.rows[1].combo <= hand_c.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(hand_c, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = [[card, 0]]
        if self.rows[1].cells:
            for card in pair:
                hand_c = deepcopy(self)
                hand_c.rows[1].add_card5(card)
                if hand_c.rows[0].combo <= hand_c.rows[1].max_combo and hand_c.rows[1].combo <= hand_c.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(hand_c, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = [[card, 1]]
        if self.rows[2].cells >= 2:
            for card in pair:
                hand_c = deepcopy(self)
                hand_c.rows[2].add_card5(card)
                if hand_c.rows[0].combo <= hand_c.rows[1].max_combo and hand_c.rows[1].combo <= hand_c.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(hand_c, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = [[card, 2]]
        print(f'elapsed time for 7 free cells {(dt.now() - start).total_seconds()} seconds')
        self.place_cards(placement)
    def s1(self, hand, deal: list, sample):
        pairs = list(combinations(deal, 2))
        next_deals = random.sample(list(combinations(hand.cards, 3)), sample)
        max_points = penalty * sample * sample * sample // 8

        if hand.rows[0].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair3(h.rows[0], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[1].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair5(h.rows[1], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[2].cells >= 2:
            for pair in pairs:
                h = deepcopy(hand)
                add_pair5(h.rows[2], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[0].cells and hand.rows[1].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[1], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[1], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[0].cells and hand.rows[2].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        if hand.rows[1].cells and hand.rows[2].cells:
            for pair in pairs:
                h = deepcopy(hand)
                add_card5(h.rows[1], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                h = deepcopy(hand)
                add_card5(h.rows[1], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
        return max_points
    def s1p(self, deal: list, sample):
        start = dt.now()
        pairs = list(combinations(deal, 2))
        next_deals = random.sample(list(combinations(self.cards, 3)), sample)
        max_points = penalty * len(next_deals)
        placement = 0

        if self.rows[0].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair3(h.rows[0], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 0])
        if self.rows[1].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair5(h.rows[1], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 1])
        if self.rows[2].cells >= 2:
            for pair in pairs:
                h = deepcopy(self)
                add_pair5(h.rows[2], pair)
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 2])
        if self.rows[0].cells and self.rows[1].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[1], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 1])
                h = deepcopy(self)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[1], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 0])
        if self.rows[0].cells and self.rows[2].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card3(h.rows[0], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 0], [pair[1], 2])
                h = deepcopy(self)
                add_card3(h.rows[0], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 0])
        if self.rows[1].cells and self.rows[2].cells:
            for pair in pairs:
                h = deepcopy(self)
                add_card5(h.rows[1], pair[0])
                add_card5(h.rows[2], pair[1])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 1], [pair[1], 2])
                h = deepcopy(self)
                add_card5(h.rows[1], pair[1])
                add_card5(h.rows[2], pair[0])
                if h.rows[0].combo <= h.rows[1].max_combo and h.rows[1].combo <= h.rows[2].max_combo and h.rows[0].combo <= h.rows[2].max_combo:
                    r = 0
                    for next_deal in next_deals:
                        r += self.s2(h, next_deal, sample // 2)
                    if r > max_points:
                        max_points = r
                        placement = ([pair[0], 2], [pair[1], 1])
        print(f'elapsed time for 8 free cells {(dt.now() - start).total_seconds()}')
        self.place_cards(placement)
hand_ = Hand_()

def set_field():
    global players, cards, fantasy
    set_card_imgs()
    players = []
    cards = []
    fantasy = Fantasy()
    for i in range(52): cards.append(Card(i))
    for i in range(3): players.append(Player(i))
set_field()

deal = []
deal_ = []
seed = 2000
def test_deal(seed: int):
    global deal
    random.seed(seed)
    random.seed()
    deal = list(range(52))
    random.shuffle(deal)
    """
    start_hand = random.sample(deck,5)
    for item in start_hand: deck.remove(item)
    random.seed()
    next_cards = random.sample(deck,47)
    deal = start_hand + next_cards
    """

test_deal(seed)

root.mainloop()