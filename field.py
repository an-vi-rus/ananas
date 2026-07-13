import tkinter as tk
from tkinter import ttk, IntVar
from PIL import Image, ImageTk



# test

def set_card_imgs(w, h):
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
    def __init__(self, n, root: tk.Tk, canvas: tk.Canvas, w, h):
        self.n = n
        self.x = root.winfo_width()/2 - (6-self.n // 4) * w + 10
        #self.x = 640  - (6-self.n // 4) * w + 10
        self.y = self.n % 4 * h + h // 2 + 10
        self.state = 'free'
        self.id = canvas.create_image(self.x, self.y, image = card_imgs[n], anchor='center')
        #canvas.tag_bind(self.id, "<Button-1>", self.select)

class Field:
    def __init__(self, root):
        global cards, canvas, rb_value
        cards = []
        root.title("Ananas")
        root.attributes("-fullscreen", True)
        root.update_idletasks()
        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(frame, bg='lightgreen', bd=0)
        canvas.pack(fill='both', expand=True)
        rb_value = IntVar()
        rb_value.set(0)
        card_h = int(root.winfo_height() / 12)
        card_w = int(card_h / 1.4)
        set_card_imgs(card_w, card_h)
        for i in range(52): cards.append(Card(i, root, canvas, card_w, card_h))

        


     
