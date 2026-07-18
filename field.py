import sys
import tkinter as tk
from tkinter import ttk, IntVar, Radiobutton, Button
from PIL import Image, ImageTk
import hand
import utils

hand = None
def init_data():
    global w, h, canvas, root, rb_value, screen_width, screen_height, field, hand
    root = tk.Tk()
    root.title("Ananas")
    if sys.platform == "darwin": root.attributes("-fullscreen", True)
    else: root.state("zoomed")
    root.update_idletasks()
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()
    rb_value = IntVar()
    rb_value.set(0)
    root.bind('<Key>', key_pressed)
    h = int(screen_height / 12)
    w = int(h / 1.4)
    field = Field()
    hand = hand.hand
    root.mainloop()
def reset():
    for player in players: player.reset()
    for card in cards: card.reset()
    fantasy.reset()
    hand.reset()
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
                img = ImageTk.PhotoImage(f.resize((w - 2, h - 2), 2))
                card_imgs.append(img)
def key_pressed(event):
    global deck
    match event.keysym:
        case 'f': rb_value.set(9)
        case 'Escape': reset()
        case 'd': deck = fantasy.deck
        case 'D': fantasy.deck = deck
        case 'c':
            match hand.rows[0].cells + hand.rows[1].cells + hand.rows[2].cells:
                case 2: hand.s4p(players[2], fantasy, hand)
        case 'n': fantasy.Next(5, 2000)
        case p:
            print('pause')
class Card:
    def __init__(self, n):
        self.n = n
        self.x = screen_width / 2 - (6 - self.n // 4) * w + 10
        self.y = self.n % 4 * h + h // 2 + 10
        self.state = 'free'
        self.id = canvas.create_image(self.x, self.y, image = card_imgs[n], anchor='center')
        canvas.tag_bind(self.id, "<Button-1>", self.select)
    def select(self, event):
        if self.state == 'free':
            if rb_value.get() < 9:
                player = players[rb_value.get() // 3]
                row = rb_value.get() % 3
                if player.cells[row]: 
                    player.append_card(self.n, row)
                return
            else:
                fantasy.append_card(self.n)
                hand.cards.remove(self.n)
                return
        if self.state == 'placed':
            for player in players:
                for i in range(3):
                    if self.n in player.rows[i]:
                        player.remove_card(self.n, i)
                        return
        if self.state == 'selected':
            if rb_value.get() // 3 == 2:
                if players[2].cells[rb_value.get() % 3]:
                    players[2].append_card(self.n, rb_value.get() % 3)
                    fantasy.remove_card(self.n)
            else:
                fantasy.remove_card(self.n)
                self.reset()                  
    def reset(self):
        self.state = 'free'
        canvas.coords(self.id, (self.x, self.y))
class Field:
    def __init__(self):
        global canvas, players, cards, fantasy
        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(frame, bg='lightgreen', bd=0)
        canvas.pack(fill='both', expand=True)
        set_card_imgs()
        cards = []
        for i in range(52): cards.append(Card(i))
        players = [Player(0), Player(1), Player(2)]
        fantasy = Fantasy(5, 2000)
class Player:
    def __init__(self, n):
        self.n = n
        match n:
            case 0:
                self.x = 2 * w
                self.y = screen_height - 9 * h
            case 1: 
                self.x = screen_width - 6 * w
                self.y = screen_height - 9 * h
            case 2: 
                self.x = screen_width // 2 - 2.5 * w
                self.y = screen_height - 3.5 * h
        self.x1, self.y1 = [self.x + 1.5*w, self.x + 0.5*w, self.x + 0.5*w], [self.y + 0.5*h, self.y + 1.5*h, self.y + 2.5*h]
        self.rows = [[], [], []]
        self.combos = [(0, []), (0, []), (0, [])]
        self.cells = [3, 5, 5]
        rb_labels = ['High', 'Mid', 'Low']
        for c in range(1,4): canvas.create_rectangle(self.x + w*c, self.y, self.x+w*(c+1), self.y + h)
        for c in range(0,5): canvas.create_rectangle(self.x + w*c, self.y+h, self.x+w*(c+1), self.y + h*2)
        for c in range(0,5): canvas.create_rectangle(self.x + w*c, self.y+h*2, self.x+w*(c+1), self.y + h*3)
        for i in range(3): 
            rb = Radiobutton(text=rb_labels[i], variable=rb_value, value=3*self.n+i, indicatoron=False, font=("TkinterDefaultFont", 10))
            canvas.create_window(self.x-w, self.y+h*i, window=rb, width=w-5, height=h, anchor='nw')
    def reset(self):
        self.rows = [[], [], []]
        self.cells = [3, 5, 5]
    def append_card(self, card, row):
        shift = 0.5 if row == 0 else -0.5
        self.rows[row].append(card)
        canvas.coords(cards[card].id, (self.x+w*(len(self.rows[row])+shift),self.y+h*(row+0.5)))
        self.cells[row] -= 1
        cards[card].state = 'placed'
        if card in hand.cards: hand.cards.remove(card)
        if self.n == 2:
            hand.rows[row].cells -=1 
            hand.rows[row].add_card(hand.rows[row], card)
    def remove_card(self, card, row):
        self.rows[row].remove(card)
        self.cells[row] += 1
        cards[card].reset()
        self.sort_cards(row)
    def sort_cards(self, row):
        shift = 1.5 if row == 0 else 0.5
        for i in range(len(self.rows[row])):
            canvas.coords(cards[self.rows[row][i]].id, (self.x+w*(i+shift)),self.y+h*(row+0.5))
class Fantasy:
    def __init__(self, starter, seed):
        self.starter = starter
        self.seed = seed
        self.point = (screen_width // 2 - 7 * w, screen_height - 5 * h)
        self.radiobutton = Radiobutton(text = 'Fantasy', variable=rb_value, value=9, bg='lightgreen', font=('TkDefaultFont, 11'))
        self.next_button = Button(text = 'Next', bg='lightgreen', command=self.Next, font=('TkDefaultFont, 11'))
        canvas.create_window(self.point[0] - 2 * w, self.point[1] + h, window=self.radiobutton, anchor='sw')
        canvas.create_window(self.point[0] - 1.5 * w, self.point[1], window=self.next_button, anchor='nw')
        self.reset()
    def reset(self):
        self.cards = []
        self.dropped = []
        self.step = 0
        rb_value.set(9)
        self.deck = utils.test_deck(self.starter, self.seed)
    def append_card(self, card: int):
        canvas.coords(cards[card].id, (self.point[0]+w*(len(self.cards)+0.5),self.point[1]+h*0.5))
        self.cards.append(card)
        cards[card].state = 'selected'     
    def sort_cards(self):
        for i in range(len(self.cards)):
            canvas.coords(cards[self.cards[i]].id, (self.point[0]+w*(i+0.5)),self.point[1]+h*0.5)
    def drop_card(self, card: int):
        cards[card].state = 'dropped'
        self.cards.remove(card)
        self.dropped.append(card)
        canvas.coords(cards[card].id, (self.point[0]+w*((len(self.dropped)+12)),self.point[1]+h*0.5))
        self.sort_cards()
    def drop_cards(self):
        while self.cards:
            n = self.cards.pop()
            cards[n].state = 'dropped'
            self.dropped.append(n)
            canvas.coords(cards[n].id, (self.point[0]+w*((len(self.dropped)+12)),self.point[1]+h*0.5))

    def remove_card(self, card: int):
        self.cards.remove(card)
        self.sort_cards()
    def Next(self, starter, seed):
        match self.step:
            case 0:
                for i in range(5):
                    fantasy.append_card(self.deck[i])
                self.step += 1
            case 1:
                for p in range(2):
                    for c in range(5):
                        players[p].append_card(self.deck[p*5+5+c], 1)
                for i in range(3):
                    fantasy.append_card(self.deck[15+i])
                self.step += 1
            case 2:
                self.drop_cards()
                for p in range(2):
                    for c in range(2):
                        players[p].append_card(self.deck[p*2+c+18], 2)
                for i in range(3):
                    fantasy.append_card(self.deck[i+22])
                self.step += 1
            case 3:
                self.drop_cards()
                for p in range(2):
                    for c in range(2):
                        players[p].append_card(self.deck[p*2+c+25], 2)
                for i in range(3):
                    fantasy.append_card(self.deck[i+29])
                self.step += 1
            case 4:
                self.drop_cards()
                for p in range(2):
                    for c in range(2):
                        players[p].append_card(self.deck[p*2+c+32], 0)
                for i in range(3):
                    fantasy.append_card(self.deck[i+36])
                self.step += 1
            case 5:
                self.drop_cards()
                players[0].append_card(self.deck[39], 0)
                players[0].append_card(self.deck[40], 2)
                players[1].append_card(self.deck[41], 0)
                players[1].append_card(self.deck[42], 2)
                self.step +=1
