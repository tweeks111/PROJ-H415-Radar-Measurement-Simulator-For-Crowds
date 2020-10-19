import tkinter as tk
import View.Simulation


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Simulation")

        self.map_dim = [0, 0]

        self.canvas = View.Simulation.Canvas(self)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.canvas.setMapDim(map_dim)

    def updateSimulation(self, pos_list):
        self.canvas.updatePoints(pos_list)

    def initSimulation(self, pos_list):
        self.canvas.initPoints(pos_list)
