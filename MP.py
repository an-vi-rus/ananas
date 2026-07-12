from concurrent.futures import ProcessPoolExecutor as executor
import tkinter
from tkinter import ttk
from field import Field

root = tkinter.Tk()
field = Field(root)
root.mainloop()
