import tkinter as tk
import View.Simulation


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Simulation")

        self.map_dim = [0, 0]

        self.canvas = View.Simulation.Canvas(self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT)
        self.rdm_canvas = View.Simulation.RDMCanvas(self)
        self.rdm_canvas.get_tk_widget().pack(side=tk.RIGHT)

    def initSimulation(self, pos_list, color_list, tx_pos, rx_pos, x, y, z):
        self.canvas.drawMap()
        self.initRadar(tx_pos, rx_pos)
        self.canvas.initPoints(pos_list, color_list)
        self.rdm_canvas.initRDM(x, y, z)
        
    def updateSimulation(self, pos_list):
        self.canvas.updatePoints(pos_list)

    def initRadar(self, tx_pos, rx_pos):
        self.canvas.initRadar(tx_pos, rx_pos)

    def clearSimulation(self):
        self.canvas.clearSimulation()

    def plotRDM(self, z):
        self.rdm_canvas.updateRDM(z)

    # -- Set Functions -- #

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.canvas.setMapDim(map_dim)