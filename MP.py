from concurrent.futures import ProcessPoolExecutor as executor
import tkinter
from field import Field, Player, init_data


root = tkinter.Tk()
init_data(root)
field_ = Field()
players = [Player(0), Player(1), Player(2)]
root.mainloop()
