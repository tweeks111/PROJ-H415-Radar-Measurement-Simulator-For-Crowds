import tkinter as tk
import numpy as np
from constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib import cm


class RDMCanvas(FigureCanvasTkAgg):
    def __init__(self, parent):
        self.fig = Figure(figsize=(4, 4))
        self.ax = self.fig.add_subplot(111)
        self.fig.set_facecolor("#f0f0f0")
        self.cb = None
        self.background = None
        FigureCanvasTkAgg.__init__(self, self.fig, master=parent)

        self.x = 0
        self.y = 0
        #self.toolbar = NavigationToolbar2Tk(self, parent)

    def initRDM(self, x, y, z):
        self.x = x
        self.y = y
        pc = self.ax.pcolormesh(x, y, z, cmap='jet', shading='auto', vmin=-200, vmax=-40)
        self.cb = self.fig.colorbar(pc)
        #plt.show()
        self.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def updateRDM(self, z):
        self.fig.canvas.restore_region(self.background)
        pc = self.ax.pcolormesh(self.x, self.y, z, cmap='jet', shading='auto', vmin=-200, vmax=-40)
        self.ax.draw_artist(pc)
        self.fig.canvas.blit(self.ax.bbox)

