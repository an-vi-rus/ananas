import tkinter as tk
from tkinter import ttk, IntVar, Radiobutton


class Player:
    def __init__(self, n: int, root: tk.Tk, canvas: tk.Canvas, rb_value):
        self.n = n
        self.card_h = int(root.winfo_height() / 12)
        self.card_w = int(self.card_h / 1.4)
        self.x = 50 + 800 * (n % 2) + 420 * (n // 2)
        self.y = 300 + 300 * (n // 2)
        self.x1, self.y1 = [self.x + 1.5*self.card_w, self.x + 0.5*self.card_w, self.x + 0.5*self.card_w], [self.y + 0.5*self.card_h, self.y + 1.5*self.card_h, self.y + 2.5*self.card_h]
        self.rows = [[], [], []]
        self.combos = [(0, []), (0, []), (0, [])]
        self.free_cells = [3, 5, 5]
        self.canvas = canvas
        rb_labels = ['High', 'Mid', 'Low']
        for c in range(1,4): canvas.create_rectangle(self.x + self.card_w*c,self.y,         self.x+self.card_w*(c+1),self.y + self.card_h)
        for c in range(0,5): canvas.create_rectangle(self.x + self.card_w*c,self.y+self.card_h,  self.x+self.card_w*(c+1),self.y + self.card_h*2)
        for c in range(0,5): canvas.create_rectangle(self.x + self.card_w*c,self.y+self.card_h*2,self.x+self.card_w*(c+1),self.y + self.card_h*3)
        for i in range(3): 
            rb = Radiobutton(text=rb_labels[i], variable=rb_value, value=3*self.n+i, indicatoron=False)
            canvas.create_window(self.x-self.card_w, self.y+self.card_h*i, window=rb, width=self.card_w-5, height=self.card_h, anchor='nw')
    def reset(self):
        self.rows = [[], [], []]
        self.free_cells = [3, 5, 5]
    def append_card(self, card, row):
        shift = 0.5 if row == 0 else -0.5
        self.rows[row].append(card.n)
        self.canvas.coords(card.id, (self.x+self.card_w*(len(self.rows[row])+shift),self.y+self.card_h*(row+0.5)))
        self.free_cells[row] -= 1
    def remove_card(self, card, row):
        self.rows[row].remove(card.n)
        self.free_cells[row] += 1
        self.sort_cards(row)
    def sort_cards(self, row):
        shift = 1.5 if row == 0 else 0.5
        for i in range(len(self.rows[row])):
            n = self.rows[row][i]
            self.canvas.coords(cards[self.rows[row][i]].id, (self.x+card_w*(i+shift)),self.y+card_h*(row+0.5))
    
