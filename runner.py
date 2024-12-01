#The initial program that starts the GUI
import tkinter as tk
from gui import GUI


if __name__ == "__main__":
    #Start GUI
    root = tk.Tk()
    client_app = GUI(root)
    root.mainloop()
