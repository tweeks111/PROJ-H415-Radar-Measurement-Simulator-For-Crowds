import tkinter as tk
import constants as cst


class Canvas(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=500, height=500, bg="ivory")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
