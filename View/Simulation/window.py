import tkinter as tk
import View.Simulation


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Editor")
        self.canvas = View.Simulation.Canvas(self)

