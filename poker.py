import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial
from graphics import init_graphics, update_graphics

root = tk.Tk()
tabs = {}
c_w, c_h = 50, 72

def card_images():
    global cards
    cards = []
    card_ranks=('2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace')
    card_suits = ('hearts', 'spades', 'diamonds', 'clubs')
    for i in range(13):
        for j in range(4):
            filename = 'images/' + card_ranks[i] + '_of_' + card_suits[j]
            filename = filename + '2.png' if i > 8 and i < 12 else filename + '.png'
            with Image.open(filename) as f:
                img = ImageTk.PhotoImage(f.resize((48, 70), 2))
                cards.append(img)
card_images()

def clear(tab_name: str):
    params = tabs[tab_name]
    hand, table, cnv = params['h'], params['t'], params['cnv']
    d_x, d_y = params['d_x'], params['d_y']
    for item in params['cards']: item.selected = False
    l = hand[:]
    for tag in l:
        ID = cnv.find_withtag(tag)[0]
        n = int(tag.replace('t',''))
        x, y = d_x + (n // 4) * c_w, d_y + (n % 4) * (c_h+3)
        cnv.coords(ID, x, y)
        hand.remove(tag)
    l = table[:]
    for tag in l:
        ID = cnv.find_withtag(tag)[0]
        n = int(tag.replace('t',''))
        x, y = d_x + (n // 4) * c_w, d_y + (n % 4) * (c_h+3)
        cnv.coords(ID, x, y)
        table.remove(tag)
class Card:
    def __init__(self, n: int, key: str):
        self.tab = tabs[key]
        self.cnv = tabs[key]['cnv']
        self.key = key
        self.num = n
        self.rank = n // 4
        self.suit = n % 4
        d_x, d_y = tabs[key]['d_x'], tabs[key]['d_y']
        self.x, self.y = d_x + self.rank * c_w, d_y + self.suit * (c_h+3)
        self.selected = False
        self.tag = 't' + str(n)
        self.id = self.cnv.create_image(self.x, self.y, image = cards[n], anchor='nw', tag=self.tag)
        self.cnv.tag_bind(self.id, "<Button-1>", self.select)

    def select(self, event):
        cnv = self.cnv
        tag = self.tag
        id = self.id
        tab = self.tab
        hand, table = tab['h'], tab['t']
        hand_size = tab['h_s']
        hand_x, hand_y = tab['h_x'], tab['h_y']
        table_x, table_y = tab['t_x'], tab['t_y']
        if self.selected:
            cnv.coords(id, self.x, self.y)
            if tag in hand:
                hand.remove(tag)
                for i in range(len(hand)):
                    ID = cnv.find_withtag(hand[i])[0]
                    cnv.coords(ID, hand_x + i * c_w, hand_y)
            else:
                table.remove(tag)
                for i in range(len(table)):
                    ID = cnv.find_withtag(table[i])[0]
                    cnv.coords(ID, table_x + i * c_w, table_y)                
            self.selected = False
        else:
            if len(hand) < hand_size:
                cnv.coords(id, hand_x + len(hand) * c_w, hand_y) 
                hand.append(tag)
                self.selected = True
            elif len(table) < 5:
                cnv.coords(id, table_x + len(table) * c_w, table_y)
                table.append(tag)
                self.selected = True 
        update_graphics(tabs,self.key) 
                      
      

def init_gui():
  root.title('POKER')
  style = ttk.Style(root)
  style.configure("TNotebook", background="lightgray", padding=[0, 0])
  notebook1 = ttk.Notebook(root)
  notebook1.pack(expand=True, fill='both')
  tab_names = ('Player stats', 'Holdem', 'Texas', 'Omaha')
  root.attributes('-fullscreen', True)

  for item in tab_names:
    frame1 = ttk.Frame(notebook1)
    frame1.pack(fill="both", expand=True)
    notebook1.add(frame1, text=item)
    if item == 'Player stats': continue
    notebook2 = ttk.Notebook(frame1)
    notebook2.pack(expand=True, fill='both')
    for i in range(1, 5):
      frame2 = ttk.Frame(notebook2)
      frame2.pack(fill="both", expand=True)
      shift = 3 if item == 'Omaha' else 0
      h_s = i + shift if item == 'Omaha' else 2
      start = 4 if item == 'Texas' else 0
      d_x, d_y = 510, 10
      h_x, h_y = d_x - (h_s+1-start) * c_w, 10
      t_x, t_y = d_x - (6 - start) * c_w, 82
      key = item+' '+str(i+shift)
      notebook2.add(frame2, text=key)
      cnv = tk.Canvas(frame2, width=1240, height=800, bg='lime green', bd=0)
      clear_button = tk.Button(root, text='Clear all', command=partial(clear, key))
      cnv.create_window(10, 10, window=clear_button, anchor='nw')
      cnv.create_rectangle((0, 314, 1240, 740), fill='white', width=0)
      tabs[key] = {'cnv':cnv,'d_x':d_x,'d_y':d_y,'h_x':h_x,'h_y':h_y,'t_x':t_x,'t_y':t_y,'h_s':h_s,'h':[],'t':[]}
      cards = []
      for i in range(start*4, 52): 
          card = Card(i,key)
          cards.append(card)
      tabs[key]['cards'] = cards
      for i1 in range(start,13):
        for i2 in range(4): cnv.create_rectangle((d_x-1+c_w*i1,d_y-3+(c_h+3)*i2,d_x-1+c_w*(i1+1),d_y-3+(c_h+3)*(i2+1)),width=1,outline='indigo')
      for i in range(h_s): cnv.create_rectangle((h_x+c_w*i,h_y,h_x+(i+1)*c_w,h_y+72),width=1,outline='indigo')
      for i in range(5): cnv.create_rectangle((t_x+c_w*(i),t_y,t_x+(i+1)*c_w,t_y+72),width=1,outline='indigo')
      cnv.pack()
  init_graphics(tabs)
init_gui()

def draw_hyst(data: list, tab: str, x=300, y=700, color='red'):
    cnv = tabs[tab]['cnv']
    for i in range(len(data)):
        cnv.create_line((x,y-i,x+data[i],y-i),fill=color,width=1)





root.mainloop()