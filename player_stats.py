import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
import psycopg
from datetime import datetime


labels = ['Deals', 'VPIP', 'PFR', '3Bet', 'AFq']
records = []
entry_results=[]

conn = psycopg.connect(dbname="poker", user="postgres", password="Av220166", host="127.0.0.1", port="5432")
cur = conn.cursor()

def get_games():
    games = []
    cur.execute("SELECT DISTINCT game FROM tournaments ORDER BY game")
    for item in cur:
        games.append(item[0])
    return games
def get_titles(game: str):
    titles = []
    cur.execute("SELECT DISTINCT title FROM tournaments WHERE game = " + repr(game))
    for item in cur:
        titles.append(item[0])
    titles.sort()
    return titles

players = ['1', '3', '2', '22', '2a22']
#titles = get_titles('Holdem NL')
#titles.sort()               
#cur.execute("SELECT game FROM tournaments ORDER BY game")
#for item in cur:
#    print(item)
#cur.execute("SELECT DISTINCT title FROM tournaments ORDER BY title")
#for item in cur:
#    print(item)
# cur.execute("SELECT DISTINCT name FROM players ORDER by player")
# for item in cur:
#    players.append(item[0])
# cur.execute("SELECT DISTINCT tournament FROM players ORDER by tournament")
# for item in cur:
#    tournaments.append(item[0])

def filter_combobox(event, combo: ttk.Combobox):
    # Get the current text typed by the user
    typed = combo.get()
    
    if typed == '':
        # If nothing is typed, show all values
        combo['values'] = titles
    else:
        # Filter the original list based on the typed substring
        filtered = [item for item in titles if typed.lower() in item.lower()]
        combo['values'] = filtered
    
    # Optional: Automatically open the dropdown to show results
    combo.event_generate('<Down>')

def only_numbers(new_val):
    return new_val.isdigit() or new_val == ""

class Record:
    def __init__(self, frame: ttk.Frame, index: list) -> None:
        self.record = {}
        name = AutocompleteCombobox(frame, completevalues=players, width=12)
        name.place(x=10 + index[0] * 670, y=90*index[1] + 40)
        self.record['Player'] = name
        for i in range(len(labels)):
            entry = ttk.Entry(frame,width=3,justify='right',validate="key", validatecommand=check_numbers)
            entry.place(x = 155 + 40*i + index[0] * 670 , y = 90 * index[1] + 40)
            self.record[labels[i]] = entry
        comments = tk.Text(frame, height=4, width=30)
        comments.place(x = 370 + index[0] * 670, y = 90 * index[1] + 40)
        self.record['Comments'] = comments
    def clear(self):
        for item in labels:
            self.record[item].delete(0, 'end')
        self.record['Comments'].delete('1.0', 'end')
        self.record['Player'].set('')
    def get(self):
        result = {}
        result['Player'] = self.record['Player'].get()
        for item in labels:
            result[item] = self.record[item].get()
        result['Comments'] = self.record['Comments'].get('1.0', 'end-1c')
        result['Tournament'] = tournament.get('1.0', 'end-1c')
        return result

def init_stats(frame: ttk.Frame):
    global check_numbers #, tournament
    check_numbers = (frame.register(only_numbers), "%P")

    titles = get_titles('Holdem NL')
    #titles.sort()
    def filter_combobox(event):
        # Get the current text typed by the user
        typed = title.get()
    
        if typed == '':
            # If nothing is typed, show all values
            title['values'] = titles
        else:
            # Filter the original list based on the typed substring
            filtered = [item for item in titles if item.lower().startswith(typed.lower())]
            title['values'] = filtered
    
        # Optional: Automatically open the dropdown to show results
        title.event_generate('<Down>')
        title.focus_set()

    for i1 in range(2):
        for i2 in range(len(labels)):
            lbl = ttk.Label(text=labels[i2], width=5, anchor='n')
            lbl.place(x=150+40*i2 +i1*670,y=30)
        name=ttk.Label(text='Player', width=12, anchor='n')
        name.place(x=10 + 670*i1,y=30)
        comments = ttk.Label(text='Comments')
        comments.place(x=440+670*i1,y=30)
    for i in range(16):
        records.append(Record(frame, [i // 8, i % 8]))
        entry_results.append({})

    lbl = ttk.Label(text='Title', width=10, anchor='n')
    lbl.place(x=640,y=720) 
    title = ttk.Combobox(frame, values=titles, width=40)
    #title = AutocompleteCombobox(frame, completevalues=titles, width=40)
    title.place(x = 640, y = 720)
    title.bind('<KeyRelease>', filter_combobox)

    clear_button = ttk.Button(frame, text='Clear',command=clear_entry)
    clear_button.place(x=20,y=720)
    upload_button = ttk.Button(frame, text='Upload',command=upload_entry)
    upload_button.place(x=220,y=720)

def clear_entry():
    for i in range(len(records)):
        records[i].clear()
    print('Clear entry')

def upload_entry():
    players = []
    for i in range(16):
        entry_results[i] = records[i].get()
        players.append(entry_results[i])
    for item in players:
        if item['Player'] and item['Deals']:
            name = item['Player']
            dls = int(item['Deals'])
            vpip = 0 if item['VPIP'] == '' else round(int(item['VPIP'])*dls/100)
            pfr = 0 if item['PFR'] == '' else round(int(item['PFR'])*dls/100)
            bet3 = 0 if item['3Bet'] == '' else round(int(item['3Bet'])*dls/100)
            afq = 0 if item['AFq'] == '' else round(int(item['AFq'])*dls/100)
            comment = item['Comments']
            tournament = item['Tournament']
            cur.execute("""
                INSERT INTO players (player, deals, vpip, pfr, bet3, afq, commnts, tournament) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (name,dls,vpip,pfr,bet3,afq,comment,tournament))
            cur.execute("SELECT * FROM players")
            print(cur.fetchone())


    conn.commit()


    


