import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
import psycopg
root = tk.Tk()
root.title("Tournaments Info")
root.attributes("-fullscreen", True)
frame = ttk.Frame(root)
frame.pack(fill='both', expand=True)


fields = ['game','fee','nominal','players', 'limit', 'title','prize']
records = {'game': ['Holdem', 'Texas 6+', 'Omaha', 'Omaha 5', 'Omaha 6', 'Omaha 7', 'Ananas', 'Ananas J']}
records['fee'] = ['freeroll', 'ticket', 'TM', 'cash']
records['nominal'] = ['0']
records['prize'] = ['1000']
records['players'] = ['2','3','6','8']
records['limit'] = ['NL', 'PL']
records['title'] = ['']
i = 0
for item in fields:
    field = ttk.Label(text=item.capitalize(), anchor='n')
    field.place(x=50+150*i, y=30)
    print(item,records[item])
    data = AutocompleteCombobox(frame, completevalues=records[item], width=12)
    data.place(x=50 + 150*i, y=90)
    i += 1




root.mainloop()
conn = psycopg.connect(dbname="test", user="postgres", password="Av220166", host="127.0.0.1", port="5432")
print("Подключение установлено")
cur = conn.cursor()
record = cur.execute("SELECT * FROM test01").fetchone()
print(record)


'''
cur.execute("""
    CREATE TABLE test01 (
        id serial PRIMARY KEY,
        num integer,
        data text)
    """)

cur.execute(
            "INSERT INTO test01 (num, data) VALUES (%s, %s)",
            (100, "abc'def"))
cur.execute("SELECT * FROM test01");

'''
conn.commit()
conn.close()


'''
with psycopg.connect("dbname=test user=postgres") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("SELECT version();")
            
                    
#            CREATE TABLE test01 (
#                id serial PRIMARY KEY,
#                num integer,
#                data text)
#            """)

    conn.commit()


        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")
        print(cur.fetchone())
        # will print (1, 100, "abc'def")

        # You can use `cur.executemany()` to perform an operation in batch
        cur.executemany(
            "INSERT INTO test (num) values (%s)",
            [(33,), (66,), (99,)])

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        cur.execute("SELECT id, num FROM test order by num")
        for record in cur:
            print(record)

        # Make the changes to the database persistent
        conn.commit()

'''