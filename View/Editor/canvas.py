import tkinter as tk
from constants import *
import math

class Canvas(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#f0f0f0")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.map_dim = [0, 0]
        self.PIXEL_PER_METER = 0
        self.pixel_map_dim = [0, 0]
        self.pad = [0, 0]

        self.clusters_list = []
        self.arrows_list = []

    def computePixelRatio(self):
        min_canvas_size = min(CANVAS_WIDTH-100, CANVAS_HEIGHT-100)
        max_map_size = max(self.map_dim[0], self.map_dim[1])
        return min_canvas_size / max_map_size

    def computePixelMapDim(self):
        return [self.PIXEL_PER_METER * self.map_dim[0], self.PIXEL_PER_METER * self.map_dim[1]]

    def computePad(self):
        return [(CANVAS_WIDTH - self.pixel_map_dim[0]) / 2, (CANVAS_HEIGHT - self.pixel_map_dim[1]) / 2]

    def drawMap(self):
        self.create_rectangle(self.pad[0], self.pad[1], self.pad[0]+self.pixel_map_dim[0], self.pad[1]+self.pixel_map_dim[1], fill="white")

        # Legend
        self.create_line(self.pad[0], self.pad[1] - 10, self.pad[0] + self.pixel_map_dim[0], self.pad[1] - 10, fill="gray", arrow=tk.BOTH)
        self.create_line(self.pad[0] - 10, self.pad[1], self.pad[0] - 10, self.pad[1] + self.pixel_map_dim[1], fill="gray", arrow=tk.BOTH)
        width_label = self.create_text(CANVAS_WIDTH / 2, self.pad[1]-20)
        self.itemconfig(width_label, text=str(self.map_dim[0])+" m")
        height_label = self.create_text(self.pad[0] - 30, CANVAS_HEIGHT / 2)
        self.itemconfig(height_label, text=str(self.map_dim[1]) + " m")
        self.update()

    def addCluster(self, r, x, y, v, theta):
        self.clusters_list.append(self.create_oval(self.pad[0] + (x - r) * self.PIXEL_PER_METER,
                                                   self.pad[1] + (y - r) * self.PIXEL_PER_METER,
                                                   self.pad[0] + (x + r) * self.PIXEL_PER_METER,
                                                   self.pad[1] + (y + r) * self.PIXEL_PER_METER,
                                                   width=2))
        vx = v*math.cos(theta*math.pi/180) / 3.6
        vy = v*math.sin(theta*math.pi/180) / 3.6
        self.arrows_list.append(self.create_line(self.pad[0] + x * self.PIXEL_PER_METER,
                                                 self.pad[1] + y * self.PIXEL_PER_METER,
                                                 self.pad[0] + (x + vx) * self.PIXEL_PER_METER,
                                                 self.pad[1] + (y + vy) * self.PIXEL_PER_METER,
                                                 width=2,
                                                 arrow=tk.LAST))

    def removeCluster(self, index):
        self.delete(self.clusters_list[index])
        self.delete(self.arrows_list[index])
        del self.clusters_list[index]
        del self.arrows_list[index]
        self.update()

    def selectCluster(self, index):
        for item in self.clusters_list:
            self.itemconfig(item, outline='black')
        for item in self.arrows_list:
            self.itemconfig(item, fill='black')
        self.itemconfig(self.clusters_list[index], outline="red")
        self.itemconfig(self.arrows_list[index], fill="red")

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.coords(self.clusters_list[index],
                    self.pad[0] + (x - r) * self.PIXEL_PER_METER,
                    self.pad[1] + (y - r) * self.PIXEL_PER_METER,
                    self.pad[0] + (x + r) * self.PIXEL_PER_METER,
                    self.pad[1] + (y + r) * self.PIXEL_PER_METER)

        vx = v*math.cos(theta*math.pi/180) / 3.6
        vy = v*math.sin(theta*math.pi/180) / 3.6

        self.coords(self.arrows_list[index],
                    self.pad[0] + x * self.PIXEL_PER_METER,
                    self.pad[1] + y * self.PIXEL_PER_METER,
                    self.pad[0] + (x + vx) * self.PIXEL_PER_METER,
                    self.pad[1] + (y + vy) * self.PIXEL_PER_METER)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

        self.PIXEL_PER_METER = self.computePixelRatio()
        self.pixel_map_dim = self.computePixelMapDim()
        self.pad = self.computePad()

        self.drawMap()