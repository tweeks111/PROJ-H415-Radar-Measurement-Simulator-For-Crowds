import View.Editor as Editor
import View.Simulation as Sim
import View.Analysis as Analysis

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
        self.iconbitmap('icon.ico')

        self.title("RRS Map Size")
        self.resizable(False, False)

        self.map_dim = [0, 0]

        self.size_dialog        = Editor.SizeDialog(self)
        self.size_dialog.pack(padx=10, pady=5)
        self.editor_window      = Editor.Window(self)
        self.simulation_window  = Sim.Window(self)
        self.analysis_window    = Analysis.Window(self)
        self.simulation_window.withdraw()
        self.analysis_window.withdraw()

        self.centerWindow()

    def updateSimulation(self, pos_list):
        self.simulation_window.updateSimulation(pos_list)

    def addCluster(self, r, x, y, v, theta, color, is_checked):
        self.editor_window.addCluster(r, x, y, v, theta, color, is_checked)

    def addParam(self, param):
        self.editor_window.addParam(param)

    def removeCluster(self, index):
        self.editor_window.removeCluster(index)

    def removeParam(self, index):
        self.editor_window.removeParam(index)

    def selectCluster(self, index, r, x, y, v, theta, lambda0):
        self.editor_window.selectCluster(index, r, x, y, v, theta, lambda0)

    def updateClusterSettings(self, r, x, y, v, theta, index, is_point):
        self.editor_window.updateClusterSettings(r, x, y, v, theta, index, is_point)

    def updateRadarSettings(self, tx_x, tx_y, rx_x, rx_y, is_smaller):
        self.editor_window.updateRadarSettings(tx_x, tx_y, rx_x, rx_y, is_smaller)

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

    def initSimulation(self, pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap, AoA):
        self.simulation_window.initSimulation(pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap, AoA)

    def initRadar(self, tx_x, tx_y, rx_x, rx_y):
        self.editor_window.initRadar(tx_x, tx_y, rx_x, rx_y)

    def updateRDM(self, z, detection_map, AoA_list, est_list):
        self.simulation_window.plotRDM(z, detection_map, AoA_list, est_list)

    def setTotalEst(self, totalEst):
        self.simulation_window.info_panel.totalEst.set(totalEst)

    def clearSimulation(self):
        self.simulation_window.clearSimulation()

    def centerWindow(self):
        w   = self.winfo_reqwidth()
        h   = self.winfo_reqheight()
        ws  = self.winfo_screenwidth()
        hs  = self.winfo_screenheight()
        x   = (ws / 4) - (w / 2)
        y   = (hs / 4) - (h / 2)
        self.geometry('+%d+%d' % (x, y))
