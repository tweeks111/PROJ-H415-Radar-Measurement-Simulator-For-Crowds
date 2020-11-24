import tkinter as tk
from View.Editor import LeftPanel
from View.Editor import RightPanel
from View.Editor import Canvas


class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.map_dim = [0, 0]

        self.left_panel = LeftPanel(self)
        self.canvas = Canvas(self)
        self.right_panel = RightPanel(self)

    def addCluster(self, r, x, y, v, theta, color):
        self.canvas.addCluster(r, x, y, v, theta, color)
        self.left_panel.addCluster(color)

    def removeCluster(self, index):
        self.left_panel.removeCluster()
        self.canvas.removeCluster(index)

    def selectCluster(self, index, r, x, y, v, theta, lambda0):
        self.canvas.selectCluster(index)
        self.left_panel.selectCluster(r, x, y, v, theta, lambda0)

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.canvas.updateClusterSettings(r, x, y, v, theta, index)

    def updateRadarSettings(self, tx_x, tx_y, rx_x, rx_y):
        self.canvas.updateRadarSettings(tx_x, tx_y, rx_x, rx_y)

    def updateRadius(self, r):
        self.left_panel.updateRadius(r)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.left_panel.setMapDim(map_dim)
        self.right_panel.setMapDim(map_dim)
        self.canvas.setMapDim(map_dim)

    def initRadar(self, tx_x, tx_y, rx_x, rx_y):
        self.canvas.initRadar([tx_x, tx_y], [rx_x, rx_y])
