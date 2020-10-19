import View.Editor as Editor
import View.Simulation as Sim

import tkinter as tk
from tkinter import messagebox


class View(tk.Tk):
    """
    Main Tkinter Application
    """
    # Constructor
    def __init__(self):
        tk.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Size configuration")
        self.resizable(False, False)

        self.eval('tk::PlaceWindow . center')

        self.map_dim = [0, 0]

        self.size_dialog = Editor.SizeDialog(self)
        self.size_dialog.pack()
        self.editor_window = Editor.Window(self)
        self.simulation_window = Sim.Window(self)
        self.simulation_window.withdraw()

    def updateSimulation(self, pos_list):
        self.simulation_window.updateSimulation(pos_list)

    def addCluster(self, r, x, y, v, theta):
        self.editor_window.addCluster(r, x, y, v, theta)

    def removeCluster(self, index):
        self.editor_window.removeCluster(index)

    def selectCluster(self, index):
        self.editor_window.selectCluster(index)

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.editor_window.updateClusterSettings(r, x, y, v, theta, index)

    def updateRadius(self, r):
        self.editor_window.updateRadius(r)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.editor_window.setMapDim(map_dim)
        self.simulation_window.setMapDim(map_dim)
        self.size_dialog.destroy()
        self.editor_window.pack()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            self.destroy()

    def initSimulation(self, pos_list):
        self.simulation_window.deiconify()
        self.simulation_window.initSimulation(pos_list)