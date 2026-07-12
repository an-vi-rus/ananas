import psycopg, csv

data = []
conn = psycopg.connect(dbname="poker", user="postgres", password="Av220166", host="127.0.0.1", port="5432")
cur = conn.cursor()

with open('results.csv', mode='r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    game = next(reader)[1]
    room = next(reader)[1]
    title = next(reader)[1]
    buyin = next(reader)[1]
    gtg = next(reader)[1]
    prize = next(reader)[1]
    logins = next(reader)[1]
    prizes = next(reader)[1]
    duration = next(reader)[1]
    overlay = 0
    start = '2026-03-31 12:00:00'
    for row in reader:
        place = row[0]
        player = row[1]
#        cur.execute(
#                """
#                INSERT INTO player_history (room,player, game, title, place, buyin, gtd, prize, overlay, logins, prizes, duration, start)
#                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
#                (room,player,game,title,place,buyin,gtg,prize,overlay,logins,prizes,duration,start)
#                )
#cur.executemany("INSERT INTO tournament_history (room,title,buyin,gtd,logins,prizes,duration,overlay,prize) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)

conn.commit()
conn.close()