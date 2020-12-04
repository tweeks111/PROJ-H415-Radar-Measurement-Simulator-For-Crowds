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

        self.map_dim = [0, 0]

        self.size_dialog        = Editor.SizeDialog(self)
        self.size_dialog.pack()
        self.editor_window      = Editor.Window(self)
        self.simulation_window  = Sim.Window(self)
        self.simulation_window.withdraw()

        self.centerWindow()

    def updateSimulation(self, pos_list):
        self.simulation_window.updateSimulation(pos_list)

    def addCluster(self, r, x, y, v, theta, color):
        self.editor_window.addCluster(r, x, y, v, theta, color)

    def removeCluster(self, index):
        self.editor_window.removeCluster(index)

    def selectCluster(self, index, r, x, y, v, theta, lambda0):
        self.editor_window.selectCluster(index, r, x, y, v, theta, lambda0)

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.editor_window.updateClusterSettings(r, x, y, v, theta, index)

    def updateRadarSettings(self, tx_x, tx_y, rx_x, rx_y):
        self.editor_window.updateRadarSettings(tx_x, tx_y, rx_x, rx_y)

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

    def initSimulation(self, pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap):
        self.simulation_window.initSimulation(pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap)

    def initRadar(self, tx_x, tx_y, rx_x, rx_y):
        self.editor_window.initRadar(tx_x, tx_y, rx_x, rx_y)

    def updateRDM(self, z, detection_map):
        self.simulation_window.plotRDM(z, detection_map)

    def clearSimulation(self):
        self.simulation_window.clearSimulation()

    def centerWindow(self):
        w   = self.winfo_reqwidth()
        h   = self.winfo_reqheight()
        ws  = self.winfo_screenwidth()
        hs  = self.winfo_screenheight()
        x   = (ws / 2) - (w / 2)
        y   = (hs / 2) - (h / 2)
        self.geometry('+%d+%d' % (x, y))
