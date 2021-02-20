import tkinter as tk
from tkinter import ttk
from constants import *


class InfoPanel(tk.LabelFrame):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text="Informations :")
        self.nbpoints = tk.IntVar(value=0)
        self.estnbpoints = tk.IntVar(value=0)
        self.totalEst   = tk.IntVar(value=0)
        tk.Label(self, text="Number of points : ").grid(sticky=tk.W, row=0, column=0)
        tk.Label(self, textvariable=self.nbpoints).grid(row=0, column=1)
        tk.Label(self, text="Estimate nb of points :").grid(row=1, column=0)
        tk.Label(self, textvariable=self.estnbpoints).grid(row=1, column=1)
        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, rowspan=8, sticky='ns')
        tk.Label(self, text="Total estimation :").grid(row=0, column=3, sticky=tk.W)
        tk.Label(self, textvariable=self.totalEst).grid(row=0, column=4)

    def setNbPoints(self, nb):
        self.nbpoints.set(nb)

    def setEstNbPoints(self, est):
        self.estnbpoints.set(est)