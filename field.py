import tkinter as tk
from tkinter import ttk, IntVar, Radiobutton
from PIL import Image, ImageTk



# test
def init_data(root_g):
    global w, h, canvas, root, rb_value, screen_width, screen_height
    root = root_g
    root.title("Ananas")
    root.attributes("-fullscreen", True)
    root.update_idletasks()
    root.update_idletasks()
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()
    rb_value = IntVar()
    rb_value.set(0)
    h = int(screen_height / 12)
    w = int(h / 1.4)
 

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
                if player.free_cells[row]: 
                    player.append_card(self, row)
                    self.state = 'placed'
                    return
        if self.state == 'placed':
            for player in players:
                for i in range(3):
                    if self.n in player.rows[i]:
                        player.remove_card(self, i)
                        return
    def reset(self):
        self.state = 'free'
        canvas.coords(self.id, (self.x, self.y))

class Field:
    def __init__(self):
        global canvas, players, cards
        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(frame, bg='lightgreen', bd=0)
        canvas.pack(fill='both', expand=True)
        set_card_imgs()
        cards = []
        for i in range(52): cards.append(Card(i))
        players = [Player(0), Player(1), Player(2)]

class Player:
    def __init__(self, n):
        self.n = n
        self.x = 50 + 800 * (n % 2) + 420 * (n // 2)
        self.y = 300 + 300 * (n // 2)
        self.x1, self.y1 = [self.x + 1.5*w, self.x + 0.5*w, self.x + 0.5*w], [self.y + 0.5*h, self.y + 1.5*h, self.y + 2.5*h]
        self.rows = [[], [], []]
        self.combos = [(0, []), (0, []), (0, [])]
        self.free_cells = [3, 5, 5]
        rb_labels = ['High', 'Mid', 'Low']
        for c in range(1,4): canvas.create_rectangle(self.x + w*c, self.y, self.x+w*(c+1), self.y + h)
        for c in range(0,5): canvas.create_rectangle(self.x + w*c, self.y+h, self.x+w*(c+1), self.y + h*2)
        for c in range(0,5): canvas.create_rectangle(self.x + w*c, self.y+h*2, self.x+w*(c+1), self.y + h*3)
        for i in range(3): 
            rb = Radiobutton(text=rb_labels[i], variable=rb_value, value=3*self.n+i, indicatoron=False)
            canvas.create_window(self.x-w, self.y+h*i, window=rb, width=w-5, height=h, anchor='nw')
    def reset(self):
        self.rows = [[], [], []]
        self.free_cells = [3, 5, 5]
    def append_card(self, card: Card, row):
        shift = 0.5 if row == 0 else -0.5
        self.rows[row].append(card.n)
        canvas.coords(card.id, (self.x+w*(len(self.rows[row])+shift),self.y+h*(row+0.5)))
        self.free_cells[row] -= 1
    def remove_card(self, card: Card, row):
        self.rows[row].remove(card.n)
        self.free_cells[row] += 1
        card.reset()
        self.sort_cards(row)
    def sort_cards(self, row):
        shift = 1.5 if row == 0 else 0.5
        for i in range(len(self.rows[row])):
            canvas.coords(cards[self.rows[row][i]].id, (self.x+w*(i+shift)),self.y+h*(row+0.5))


     
