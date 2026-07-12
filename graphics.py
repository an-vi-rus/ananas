import tkinter as tk
from tkinter import ttk
import json
from aux import scale, to_key, to_matrix
from prepare_data import omaha_preflop, holdem_flop

hyst_x,hyst_y = 400,650
comb_x,comb_y,comb_h = 700,650,22

def init_graphics(tabs):
    global data
    combos = ['no combo ','pair ','2 pairs ','set ','straight ','flush ','full hause ','4 of a kind ','straight flush']
    with open('data.json') as f: data = json.load(f)
    for key in tabs:
        tab = tabs[key]
        cnv = tab['cnv']
        my_hyst,op_hyst,my_comb,op_comb,target,equity_id = [],[],[],[],[],0
        
        if key.split()[0] == 'Holdem':
            equities, equity_hyst, q = [], [], 6.63
            hyst,comb,equity = data['holdem']['hysto'], data['holdem']['combo'], data['holdem']['equity']
            for i1 in range(13):
                for i2 in range(13): equities += [equity[i1][i2]] * scale([i1, i2])
            equities.sort(reverse=True)
            for i in range(100): equity_hyst.append(round(sum(equities[round(i*q):round((i+1)*q)]) / (round((i+1)*q)-round(i*q)),1))
        if key.split()[0] == 'Texas':
            equities, equity_hyst, q = [], [], 3.15
            hyst,comb,equity = data['texas']['hysto'], data['texas']['combo'], data['texas']['equity']
            for i1 in range(9):
                for i2 in range(9): equities += [equity[i1][i2]] * scale([i1, i2])
            equities.sort(reverse=True)
            for i in range(100): equity_hyst.append(round(sum(equities[round(i*q):round((i+1)*q)]) / (round((i+1)*q)-round(i*q)),1))
            combos[5],combos[6] = 'full hause', 'flush'
        if key.split()[0] == 'Omaha':
            hyst = data['omaha']['omaha'+key.split()[1]]['hysto']
            comb = data['omaha']['omaha'+key.split()[1]]['combo']
            shift = 2

        for i in range(0,9):
            op_comb.append(cnv.create_rectangle(comb_x, comb_y-i*comb_h, comb_x+comb[i]*2, comb_y-(i+0.5)*comb_h,fill='orange',width=0))
            my_comb.append(cnv.create_rectangle(comb_x, comb_y-(i+0.5)*comb_h, comb_x+comb[i]*2, comb_y-(i+1.0)*comb_h,fill='green3',width=0))
        for i in range(100): 
            op_hyst.append(cnv.create_line(hyst_x,hyst_y-i    ,hyst_x+hyst[i]*2,hyst_y-i    ,fill='orange'  ,width=2))
            my_hyst.append(cnv.create_line(hyst_x,hyst_y-i-110,hyst_x+hyst[i]*2,hyst_y-i-110,fill='green3',width=2))
        if key.split()[0] in {'Holdem','Texas'}: 
            equity_curve = []
            for i in range(100): equity_curve.extend((hyst_x+equity_hyst[i]*2,hyst_y-i))
            equity_id = cnv.create_line(equity_curve,width=2,join='round')
      
        for i in range(1,10):
            if i != 5:
                cnv.create_line(hyst_x+20*i,hyst_y,hyst_x+20*i,hyst_y-210,fill='red',dash=(3, 5))
                cnv.create_text(hyst_x+20*i,hyst_y,text=str(10*i),anchor='n',font=('Arial',11))
                cnv.create_text(hyst_x+20*i,hyst_y-210,text=str(10*i),anchor='s',font=('Arial',11))
                cnv.create_line(comb_x+i*20,comb_y,comb_x+i*20,comb_y-100*2,dash=(3, 5))
                cnv.create_text(comb_x+i*20,comb_y,text=str(i*10),anchor='n',font=('Arial',11))
            else:
                cnv.create_line(hyst_x+20*i,hyst_y,hyst_x+20*i,hyst_y-210,fill='red')
                cnv.create_text(hyst_x+20*i,hyst_y,text=str(10*i),anchor='n',font=('Arial',12,'bold')) 
                cnv.create_text(hyst_x+20*i,hyst_y-210,text=str(10*i),anchor='s',font=('Arial',12,'bold'))
                cnv.create_line(comb_x+i*20,comb_y,comb_x+i*20,comb_y-200)
                cnv.create_text(comb_x+i*20,comb_y,text=str(i*10),anchor='n',font=('Arial',12,'bold')) 
            cnv.create_text(comb_x,comb_y-comb_h*(i-0.5),text=combos[i-1],anchor='e')

        target.append(cnv.create_line(hyst_x,hyst_y,hyst_x,hyst_y))
        target.append(cnv.create_line(hyst_x,hyst_y,hyst_x,hyst_y))
        target.append(cnv.create_text(hyst_x,hyst_y,text='',anchor='e',font=('Arial',11)))
        target.append(cnv.create_text(hyst_x,hyst_y,text='',anchor='se',font=('Arial',11)))

        tab['op_comb'], tab['op_hyst'], tab['equity_id'] = op_comb, op_hyst, equity_id       
        tab['my_comb'], tab['my_hyst'], tab['target'] = my_comb, my_hyst, target         

def update_graphics(tabs, key):
    cnv = tabs[key]['cnv']
    params = tabs[key]
    target = params['target']   
    def update_graph(graph_data: list, graph_id: list, scale=2):
        for i in range(len(graph_data)):
            coord = cnv.coords(graph_id[i])
            cnv.coords(graph_id[i],coord[0],coord[1],coord[0]+graph_data[i]*scale,coord[3])
    def update_target(point = (0,0)):
        cnv.coords(target[0],hyst_x,hyst_y-point[0],hyst_x+point[1]*2,hyst_y-point[0])
        cnv.coords(target[1],hyst_x+point[1]*2,hyst_y-point[0],hyst_x+point[1]*2,hyst_y)
        cnv.coords(target[2],hyst_x,hyst_y-point[0])
        cnv.coords(target[3],hyst_x+point[1]*2,hyst_y)
        if point == (0,0):
            cnv.itemconfig(target[2],text='')
            cnv.itemconfig(target[3],text='')
        else:            
            cnv.itemconfig(target[2],text=str(int(point[0])))
            cnv.itemconfig(target[3],text=str(int(point[1])))
    def target_point(hystogram: list, my_equity):
        for i in range(100):
            if my_equity >= hystogram[i]: return (i, hystogram[i])
        return (0, 0)

    tab = tabs[key]
    game = key.split()[0].lower()
    hand = [int(item.replace('t','')) for item in tab['h']]
    table = [int(item.replace('t','')) for item in tab['t']]
    hand_size = tab['h_s']
    stats = data[game] if game != 'omaha' else data[game]['omaha'+key.split()[1]]
    if len(hand) < hand_size:
        update_target()
        update_graph(stats['combo'],tab['op_comb'])
        update_graph(stats['hysto'],tab['op_hyst'])
        update_graph(stats['combo'],tab['my_comb'])
        update_graph(stats['hysto'],tab['my_hyst'])
    else:
        match len(table):
            case 0 | 1 | 2:
                if hand_size == 2:
                    matrix = to_matrix(hand)
                    hand_key = to_key(matrix)
                    point = target_point(stats['hysto'],stats['equity'][matrix[0]][matrix[1]])
                    update_target(point)
                    update_graph(stats['combo'],tab['op_comb'])
                    update_graph(stats['hysto'],tab['op_hyst'])
                    update_graph(stats['combos'][hand_key],tab['my_comb'])
                    update_graph(stats['hystos'][hand_key],tab['my_hyst'])
                else:
                    result = omaha_preflop(hand)
                    point = target_point(result['op_hysto'],result['equity'])
                    update_target(point)
                    update_graph(result['op_combo'],tab['op_comb'])
                    update_graph(result['op_hysto'],tab['op_hyst'])
                    update_graph(result['my_combo'],tab['my_comb'])
                    update_graph(result['my_hysto'],tab['my_hyst'])
            case 3:
                match game:
                    case 'holdem':
                        result = holdem_flop(hand,table)
                        point = target_point(result['op_hystos'],result['equity'])
                        update_target(point)
                        update_graph(result['op_combos'],tab['op_comb'])
                        update_graph(result['op_hystos'],tab['op_hyst'])
                        update_graph(result['my_combos'],tab['my_comb'])
                        update_graph(result['my_hystos'],tab['my_hyst'])
                    case _: print('other')
            
            case 4:
                print('turn')
            case 5:
                print('river')
        











def show_hysto(tab: str, cnv: tk.Canvas):
    hysto_x, hysto_y, hysto_scale = 400, 650, 2
    combo_x, combo_y, combo_h, combo_scale = 700, 650, 22, 2
    cum_combo = []
    combos = ['no combo','pair','2 pairs','set','straight','flush','fullhouse','care','straightflush']
    shift = 0
    with open('preflop_data.json') as f: data = json.load(f)
    if tab.startswith('Holdem'): 
        hysto = data['holdem']['hysto']
        combo = data['holdem']['combo']
    if tab.startswith('Texas'): 
        hysto = data['texas']['hysto']
        combo = data['texas']['combo']
        combos[5], combos[6] = combos[6], combos[5]
    if tab.startswith('Omaha'): 
        hysto = data['omaha']['omaha'+tab.split()[1]]['hysto']
        combo = data['omaha']['omaha'+tab.split()[1]]['combo']
        shift = 2
    for i in range(9):
        cum_combo.append(round(sum(combo[i:])))
        cnv.create_rectangle(combo_x, combo_y-i*combo_h, combo_x+cum_combo[i]*combo_scale, combo_y-(i+0.5)*combo_h,fill='orange',width=0)
        cnv.create_rectangle(combo_x, combo_y-i*combo_h, combo_x+combo[i]*combo_scale, combo_y-(i+0.5)*combo_h,fill='red',width=0)
    for i in range(100): cnv.create_line(hysto_x,hysto_y-i*hysto_scale,hysto_x+hysto[i]*hysto_scale,hysto_y-i*hysto_scale,fill='red',width=2)
    for i in range(3,10-shift):
        if i != 5:
            cnv.create_line(hysto_x+i*10*hysto_scale,hysto_y,hysto_x+i*10*hysto_scale,hysto_y-100*hysto_scale,dash=(3, 5))
            cnv.create_text(hysto_x+i*10*hysto_scale,hysto_y,text=str(i*10),anchor='n',font=('Arial',11))
        else:
            cnv.create_line(hysto_x+i*10*hysto_scale,hysto_y,hysto_x+i*10*hysto_scale,hysto_y-100*hysto_scale)
            cnv.create_text(hysto_x+i*10*hysto_scale,hysto_y,text=str(i*10),anchor='n',font=('Arial',12,'bold'))   
    for i in range(1,10): 
        if i != 5:
            cnv.create_line(combo_x+i*10*combo_scale,combo_y,combo_x+i*10*combo_scale,combo_y-100*combo_scale,dash=(3, 5))
            cnv.create_text(combo_x+i*10*combo_scale,combo_y,text=str(i*10),anchor='n',font=('Arial',11))
        else:
            cnv.create_line(combo_x+i*10*combo_scale,combo_y,combo_x+i*10*combo_scale,combo_y-100*combo_scale)
            cnv.create_text(combo_x+i*10*combo_scale,combo_y,text=str(i*10),anchor='n',font=('Arial',12,'bold'))   
        cnv.create_text(combo_x,combo_y-combo_h*(i-0.5),text=combos[i-1],anchor='e')

     



