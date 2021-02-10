from matplotlib import colors
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class RDMCanvas(FigureCanvasTkAgg):
    def __init__(self, parent):
        self.fig            = Figure()#figsize=(6, 3))
        self.fig.subplots_adjust(wspace=0.5)
        self.ax1            = None
        self.ax2            = None
        self.ax3            = None
        self.cb1            = None
        self.cb2            = None
        self.cmapbw         = colors.ListedColormap(['white', 'black'])
        self.RDM_map        = None
        self.detection_map  = None
        self.angles_plot    = None
        self.ax1background  = None
        self.ax2background  = None
        self.ax3background  = None
        self.angles         = np.arange(-90, 90.05, 0.05)
        FigureCanvasTkAgg.__init__(self, self.fig, master=parent)

        self.x = 0
        self.y = 0

    def initRDM(self, x, y, z, dmap, AoA):
        self.ax1    = self.fig.add_subplot(221)
        self.ax2    = self.fig.add_subplot(223)
        self.ax3    = self.fig.add_subplot(122)

        self.fig.set_facecolor("#f0f0f0")
        self.x = x
        self.y = y
        self.RDM_map = self.ax1.pcolormesh(x, y, z, cmap='jet', shading='auto', vmin=-180, vmax=-40)
        self.detection_map = self.ax2.pcolormesh(x, y, dmap, cmap=self.cmapbw, shading='auto', vmin=0, vmax=1)
        self.cb1 = self.fig.colorbar(self.RDM_map, ax=self.ax1)
        self.cb2 = self.fig.colorbar(self.detection_map, ax=self.ax2, ticks=[0, 1])
        self.ax1background = self.fig.canvas.copy_from_bbox(self.ax1.bbox)
        self.ax2background = self.fig.canvas.copy_from_bbox(self.ax2.bbox)
        (self.angles_plot,) = self.ax3.plot(self.angles, AoA, animated=True)
        self.ax3background = self.fig.canvas.copy_from_bbox(self.ax3.bbox)
        self.draw()

    def updateRDM(self, z, dmap, AoA):
        self.fig.canvas.restore_region(self.ax1background)
        self.fig.canvas.restore_region(self.ax2background)
        self.fig.canvas.restore_region(self.ax3background)
        self.RDM_map = self.ax1.pcolormesh(self.x, self.y, z, cmap='jet', shading='auto', vmin=-180, vmax=-40)
        self.detection_map = self.ax2.pcolormesh(self.x, self.y, dmap, cmap=self.cmapbw, shading='auto', vmin=0, vmax=1)
        self.ax1.draw_artist(self.RDM_map)
        self.ax2.draw_artist(self.detection_map)
        self.angles_plot.set_ydata(AoA)
        self.ax3.draw_artist(self.angles_plot)
        self.fig.canvas.blit(self.fig.bbox)

    def clearRDM(self):
        self.fig.clear()
        self.draw()
