import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json, aux, player_stats, approved_functions as af

root = tk.Tk()
root.title("Poker Ultimate App")
root.attributes("-fullscreen", True)
root.update_idletasks()
screen_width = root.winfo_width()
screen_height = root.winfo_height()
card_h = int(screen_height / 10)
card_w = int(card_h / 1.4)


card_imgs = []
def set_card_imgs():
    card_ranks=('2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace')
    card_suits = ('hearts', 'spades', 'diamonds', 'clubs')
    for i in range(13):
        for j in range(4):
            filename = 'images/' + card_ranks[i] + '_of_' + card_suits[j]
            filename = filename + '2.png' if i > 8 and i < 12 else filename + '.png'
            with Image.open(filename) as f:
                img = ImageTk.PhotoImage(f.resize((card_w - 2, card_h - 2), 2))
                card_imgs.append(img)
set_card_imgs()
def set_data():
    with open('data.json') as f:
        data = json.load(f)   
    return data
data = set_data()

class Card:
    def __init__(self, parent, n: int):
        self.parent = parent
        self.n = n
        self.x = screen_width - (13-self.n // 4) * card_w + 10
        self.y = self.n % 4 * card_h + card_h // 2 + 10
        self.selected = False
        self.cnv = parent.canvas
        self.id = self.cnv.create_image(self.x, self.y, image = card_imgs[n], anchor='center')
        self.cnv.tag_bind(self.id, "<Button-1>", self.select)
    def select(self, event):
        cnv = self.cnv
        n = self.n
        id = self.id
        hand, table = self.parent.hand, self.parent.table
        hand_size = self.parent.hand_size
        hand_x, hand_y = self.parent.hand_x, self.parent.hand_y
        table_x, table_y = self.parent.table_x, self.parent.table_y
        if self.selected:
            cnv.coords(id, self.x, self.y)
            if n in hand:
                hand.remove(n)
                for i in range(len(hand)):
                    cnv.coords(self.parent.card_id[hand[i]], hand_x + i * card_w, hand_y)
            else:
                table.remove(n)
                for i in range(len(table)):
                    cnv.coords(self.parent.card_id[table[i]], table_x + i * card_w, table_y)                
            self.selected = False
        else:
            if len(hand) < hand_size:
                cnv.coords(id, hand_x + len(hand) * card_w, hand_y) 
                hand.append(n)
                self.selected = True
            elif len(table) < 5:
                cnv.coords(id, table_x + len(table) * card_w, table_y)
                table.append(n)
                self.selected = True 
        self.parent.update()

class GameField:
    def __init__(self, frame, tabname: str) -> None:
        self.hand = []
        self.hand_size = int(tabname.split()[1]) if tabname.split()[0] == 'Omaha' else 2
        self.tabname = tabname
        self.table = []
        self.cards = []
        self.card_id = {}
        start_ind = 4 if tabname.split()[0] == 'Texas' else 0
        self.hand_x, self.hand_y = screen_width - (14 - start_ind + self.hand_size) * card_w + 10, card_h * 0.5 + 10
        self.table_x, self.table_y = screen_width - (19 - start_ind) * card_w + 10, card_h * 1.5 + 10
        self.canvas = tk.Canvas(frame)
        self.canvas.pack(fill='both', expand=True)
        for i in range(start_ind * 4, 52):
            card = Card(self, i) 
            self.cards.append(card)
            self.card_id[i] = card.id
        clear_button = tk.Button(frame, text='Clear all', command=self.clear_field)
        self.canvas.create_window(10, 10, window=clear_button, anchor='nw')

        match tabname.split()[0]:
            case 'Holdem': dt = data['holdem']
            case 'Texas': dt = data['texas'] 
            case 'Omaha': dt = data['omaha']['omaha'+tabname.split()[1]]
        self.my_combo = dt['combo']
        self.op_combo = dt['combo']
        self.my_hysto = dt['hysto']
        self.op_hysto = dt['hysto']
        self.my_equity_id, self.op_equity_id =0, 0
        self.my_combo_id, self.op_combo_id = [0]*9, [0]*9
        self.my_combo_text, self.op_combo_text = [0]*9, [0]*9
        self.my_hysto_id, self.op_hysto_id = [0]*100, [0]*100
                
        self.init_gui()
        self.update()
    def clear_field(self):
        for card in self.cards:
            card.selected = False
            self.canvas.coords(card.id, card.x, card.y)
        self.hand.clear()
        self.table.clear()
        self.update()

    def init_gui(self):
        match self.tabname.split()[0]:
            case 'Holdem': dt = data['holdem']
            case 'Texas': dt = data['texas'] 
            case 'Omaha': dt = data['omaha']['omaha'+self.tabname.split()[1]]

        w, h = screen_width, screen_height
        combo_marks = ['no combo', 'pair', '2 pairs', 'set', 'straight', 'flush', 'full hause', '4 of a kind', 'straight flush']
        if self.tabname.split()[0] == 'Texas': combo_marks[5], combo_marks[6] = combo_marks[6], combo_marks[5]
        cnv = self.canvas
        cnv.create_rectangle((0, card_h * 4 +20, w, h), fill='white')
        for i in range(100):
            self.my_hysto_id[i] = cnv.create_line((w/2, h- 60-i, w/2+2*dt['hysto'][i], h- 60-i),fill='green')
            self.op_hysto_id[i] = cnv.create_line((w/2, h-180-i, w/2+2*dt['hysto'][i], h-180-i),fill='red')
        for i in range(9):
            self.my_combo_id[i] = cnv.create_rectangle((w/2+250,h-60-i*24,w/2+250+2*dt['combo'][i],h-72-i*24),fill='green',width=0)
            self.op_combo_id[i] = cnv.create_rectangle((w/2+250,h-72-i*24,w/2+250+2*dt['combo'][i],h-84-i*24),fill='red',width=0)
            cnv.create_text((w/2+250,h-72-i*24), text=combo_marks[i],anchor='e',font=('Arial',12))
            cnv.create_line((w/2+225,h-60-i*24,w/2+475,h-60-i*24),dash=(4,2))
            self.my_combo_text[i] = cnv.create_text((w/2+450,h-60-i*24), text=int(dt['combo'][i]),anchor='sw',font=('Arial',11), fill='darkgreen')
            self.op_combo_text[i] = cnv.create_text((w/2+450,h-72-i*24), text=int(dt['combo'][i]),anchor='sw',font=('Arial',11), fill='red3')
        for i in range(1,10):
            d = () if i == 5 else (2,4)
            cnv.create_text((w/2+20*i,h-60),text=str(i*10),anchor='n',font=('Arial', 11))
            cnv.create_line((w/2+20*i,h-60,w/2+20*i,h-160),dash=d)
            cnv.create_text((w/2+20*i,h-180),text=str(i*10),anchor='n',font=('Arial', 11))
            cnv.create_line((w/2+20*i,h-180,w/2+20*i,h-280),dash=d)
            cnv.create_text((w/2+250+20*i,h-60),text=str(i*10),anchor='n',font=('Arial', 11))
            cnv.create_line((w/2+250+20*i,h-60,w/2+250+20*i,h-280),dash=d)
            if i % 2: 
                cnv.create_line((w/2,h-60-10*i,w/2+180,h-60-10*i),dash=d)
                cnv.create_text((w/2, h-60-10*i),text=str(i*10),anchor='e',font=('Arial',11))
                cnv.create_line((w/2,h-180-10*i,w/2+180,h-180-10*i),dash=d)
                cnv.create_text((w/2, h-180-10*i),text=str(i*10),anchor='e',font=('Arial',11))
        
        cnv.create_arc((w-150,h-250,w-10,h-110),start=90, extent=-359.9, fill='red', width=0)
        self.equity_id = cnv.create_arc((w-150,h-250,w-10,h-110),start=90, extent=-360*180/360, fill='green', width=0)
        self.equity_mark = cnv.create_text((w-80,h-180), text='', anchor='n', font=('Arial', 12, 'bold'))

    def update(self):
        h_l, t_l, tab = len(self.hand), len(self.table), self.tabname.split()[0]
        hand, table, h_s = self.hand, self.table, self.hand_size
        dt, result = {}, {}
        if h_l < h_s:
            match tab:
                case 'Holdem': dt = data['holdem']
                case 'Texas': dt = data['texas']
                case 'Omaha': dt = data['omaha']['omaha'+self.tabname.split()[1]]
            result['my_combo'] = dt['combo']
            result['op_combo'] = dt['combo']
            result['my_hysto'] = dt['hysto']
            result['op_hysto'] = dt['hysto']
        else: 
            match t_l:
                case 0:
                    match tab:
                        case 'Holdem': 
                            dt = data['holdem']
                            key = aux.to_key(aux.to_matrix(self.hand))
                            result['my_combo'] = dt['combos'][key]
                            result['my_hysto'] = dt['hystos'][key]
                            result['op_combo'] = dt['combo']
                            result['op_hysto'] = dt['hysto']
                        case 'Texas': 
                            dt = data['texas']
                            key = aux.to_key(aux.to_matrix(self.hand))
                            result['my_combo'] = dt['combos'][key]
                            result['my_hysto'] = dt['hystos'][key]
                            result['op_combo'] = dt['combo']
                            result['op_hysto'] = dt['hysto']
                        case 'Omaha': 
                            result = af.omaha_preflop(self.hand)
                case 1: return
                case 2: return
                case 3:
                    match tab:
                        case 'Holdem': result = af.holdem_flop(hand, table)
                        case 'Texas': result = af.texas_flop(hand, table)
                        case 'Omaha': result = af.omaha_flop(hand, table)
                case 4:
                    match tab:
                        case 'Holdem': result = af.holdem_turn(hand, table)
                        case 'Texas': result = af.texas_turn(hand, table)
                        case 'Omaha': result = af.omaha_turn(hand, table)
                case 5:
                    match tab:
                        case 'Holdem': result = af.holdem_river(hand, table)
                        case 'Texas': result = af.texas_river(hand, table)
                        case 'Omaha': result = af.omaha_river(hand, table)
        cnv = self.canvas
        for i in range(9):
            coord = cnv.coords(self.my_combo_id[i])
            cnv.coords(self.my_combo_id[i],(coord[0],coord[1],coord[0]+result['my_combo'][i]*2,coord[3]))
            coord = cnv.coords(self.op_combo_id[i])
            cnv.coords(self.op_combo_id[i],(coord[0],coord[1],coord[0]+result['op_combo'][i]*2,coord[3]))

            combo, cum_combo = result['my_combo'][i], sum(result['my_combo'][i:])
            mark = f'{combo: 4.0f}{cum_combo: 6.0f}'
            cnv.itemconfigure(self.my_combo_text[i], text = mark)
            combo, cum_combo = result['op_combo'][i], sum(result['op_combo'][i:])
            mark = f'{combo: 4.0f}{cum_combo: 6.0f}'
            cnv.itemconfigure(self.op_combo_text[i], text = mark)
        for i in range(100):
            coord = cnv.coords(self.my_hysto_id[i])
            cnv.coords(self.my_hysto_id[i],(coord[0],coord[1],coord[0]+result['my_hysto'][i]*2,coord[3]))
            coord = cnv.coords(self.op_hysto_id[i])
            cnv.coords(self.op_hysto_id[i],(coord[0],coord[1],coord[0]+result['op_hysto'][i]*2,coord[3]))
        equity = round(sum(result['my_hysto'])/100, 1)
        cnv.itemconfigure(self.equity_id, extent=equity*(-3.6)+0.1)
        cnv.itemconfigure(self.equity_mark, text=equity)




style = ttk.Style(root)
style.theme_use('alt') 
style.configure("TNotebook.Tab", background="lightgrey", padding=[10, 0], font=('Arial', 12))
style.configure('CenterTabs.TNotebook', tabposition='n')
style.map("TNotebook.Tab", background=[("selected", "grey")], foreground=[("selected", "white")])
notebook = ttk.Notebook(root, style='CenterTabs.TNotebook')
notebook.pack(expand=True, fill='both') # Pack the notebook into the main window, padx=0, pady=0
tab_names = ('Player Stats', 'Holdem', 'Texas', 'Omaha')
for item in tab_names:
    frame = ttk.Frame(notebook, name=item.split()[0].lower())
    frame.pack(fill='both', expand=True)
    notebook.add(frame, text=item)
    if item == 'Player Stats': player_stats.init_stats(frame)
    if item in ('Holdem', 'Texas', 'Omaha'):
        sub_notebook = ttk.Notebook(frame, style='CenterTabs.TNotebook')
        sub_notebook.pack(expand=True, fill='both')
        for i in range(1, 5):
            sub_frame = ttk.Frame(sub_notebook, style='My.TFrame')
            sub_frame.pack(fill='both', expand=True)
            shift = 3 if item == 'Omaha' else 0
            sub_tabname = item + ' ' + str(i + shift)
            sub_notebook.add(sub_frame, text=sub_tabname)
            game_field = GameField(sub_frame, sub_tabname) 

#player_stats.init_stats(notebook.nametowidget('player'))
root.mainloop()



