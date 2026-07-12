import csv, psycopg

conn = psycopg.connect(dbname="poker", user="postgres", password="Av220166", host="127.0.0.1", port="5432")
print("Подключение установлено")
cur = conn.cursor()
"""
fields = ['room', 'buy_in', 'rake', 'extra', 'knockout', 'game', 'opts', 'title', 'gtd', 'currency', 'satellite', 'stack', 'late_registration']
fields1 = ['rebuy_lvl', 'rebuy_fee', 'rebuy_chips', 'addon_lvl', 'addon_fee', 'addon_chips', 'reentry', 'lvl_duration', 'prize_plan']
excel  = ['room', 'buy_in', 'fee', 'bounty', 'knockout', 'game', 'type', 'title', 'gtd', 'ticket',        'next', 'stack', 'LR']
excel1 = [              'rebuy',     'rebuy_chips', 'addon lvl', 'addon',     'addon_chips', 're_entry', 'level',        'prizes']
"""



with open('t01.csv', mode='r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    int_fields = [1,2,3,4,8,11,12,13,14,15,16,17,18,19,20]
    data = []
    for row in reader:
        for i in int_fields:
            row[i] = 0 if row[i] == '' else int(row[i])
        data.append(row)

def fill_tournaments(data):
    cur.executemany(
        """ INSERT INTO tournaments (room,buy_in,rake,extra,knockout,game,opts,title,gtd,currency,satellite,stack,late_registration,
                rebuy_lvl,rebuy_fee,rebuy_chips,addon_lvl,addon_fee,addon_chips,reentry,lvl_duration,prize_plan)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    conn.commit()

fill_tournaments(data)

conn.close()
