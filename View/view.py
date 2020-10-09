import tkinter as tk
from tkinter import messagebox
from View.leftPanel import LeftPanel
from View.canvas import Canvas


class View(tk.Tk):
    """
    Main Tkinter Application
    """
    # Constructor
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.left_side_panel = LeftPanel(self)
        self.canvas = Canvas(self)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            self.destroy()
