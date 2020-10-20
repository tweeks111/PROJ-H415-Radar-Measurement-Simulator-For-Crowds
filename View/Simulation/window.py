import tkinter as tk
import View.Simulation


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Simulation")

        self.map_dim = [0, 0]

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP)
        self.nb_points_label = tk.Label(self.top_frame)
        self.nb_points_label.pack()
        self.canvas = View.Simulation.Canvas(self)
        self.canvas.pack()

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.canvas.setMapDim(map_dim)

    def updateSimulation(self, pos_list):
        self.canvas.updatePoints(pos_list)

    def initSimulation(self, pos_list, color_list):

        self.nb_points_label.configure(text=str(len(pos_list)) + " persons")
        self.canvas.drawMap()
        self.canvas.initPoints(pos_list, color_list)

    def clearSimulation(self):
        self.canvas.clearSimulation()