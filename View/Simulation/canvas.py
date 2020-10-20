import tkinter as tk
from constants import *


class Canvas(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#f0f0f0")

        self.map_dim = [0, 0]
        self.points_list = []
        self.PIXEL_PER_METER = 0
        self.pixel_map_dim = [0, 0]
        self.pad = [0, 0]

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

        self.PIXEL_PER_METER = self.computePixelRatio()
        self.pixel_map_dim = self.computePixelMapDim()
        self.pad = self.computePad()

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

    def initPoints(self, pos_list, color_list):
        for i in range(0, len(pos_list)):
            self.points_list.append(self.create_oval(self.pad[0]+(pos_list[i][0]-PERSON_DIAMETER)*self.PIXEL_PER_METER,
                                                     self.pad[1]+(pos_list[i][1]-PERSON_DIAMETER)*self.PIXEL_PER_METER,
                                                     self.pad[0]+(pos_list[i][0]+PERSON_DIAMETER)*self.PIXEL_PER_METER,
                                                     self.pad[1]+(pos_list[i][1]+PERSON_DIAMETER)*self.PIXEL_PER_METER,
                                                     fill=color_list[i]))
        self.update()

    def updatePoints(self, pos_list):
        for i in range(0, len(pos_list)):
            self.coords(self.points_list[i],
                        self.pad[0]+(pos_list[i][0]-PERSON_DIAMETER)*self.PIXEL_PER_METER,
                        self.pad[1]+(pos_list[i][1]-PERSON_DIAMETER)*self.PIXEL_PER_METER,
                        self.pad[0]+(pos_list[i][0]+PERSON_DIAMETER)*self.PIXEL_PER_METER,
                        self.pad[1]+(pos_list[i][1]+PERSON_DIAMETER)*self.PIXEL_PER_METER)
        self.update()

    def clearSimulation(self):
        for point in self.points_list:
            self.delete(point)
        self.points_list.clear()
