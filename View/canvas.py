import tkinter as tk
import constants as cst


class Canvas(tk.Canvas):
    """
    Canvas which inherit from Tkinter.Canvas
    """
    # Constructor
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=cst.CANVAS_WIDTH, height=cst.CANVAS_HEIGHT, bg="ivory")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.PIXEL_PER_METER = 0
        self.padx = 0
        self.pady = 0

        # Canvas Components
        self.rectangle = self.create_rectangle(0, 0, 0, 0, fill="white")
        self.width_line = self.create_line(0, 0, 0, 0, fill="gray", arrow=tk.BOTH)
        self.height_line = self.create_line(0, 0, 0, 0, fill="gray", arrow=tk.BOTH)
        self.width_label = self.create_text(0, 0)
        self.height_label = self.create_text(0, 0)
        self.points = []
        self.clusters_list = []

    # Update Functions
    def updateRectangleDimension(self, width, height):
        pixelWidth = self.PIXEL_PER_METER * width
        pixelHeight = self.PIXEL_PER_METER * height
        self.padx = (cst.CANVAS_WIDTH-pixelWidth)/2
        self.pady = (cst.CANVAS_HEIGHT-pixelHeight)/2
        self.coords(self.rectangle, self.padx, self.pady, self.padx+pixelWidth, self.pady+pixelHeight)

        # Legend
        self.coords(self.width_line, self.padx, self.pady - 10, self.padx+pixelWidth, self.pady - 10)
        self.coords(self.height_line, self.padx - 10, self.pady, self.padx - 10, self.pady+pixelHeight)
        self.coords(self.height_label, self.padx-20, cst.CANVAS_HEIGHT/2)
        self.itemconfig(self.height_label, text=str(height) + " m", angle=90)
        self.coords(self.width_label, cst.CANVAS_WIDTH/2, self.pady-20)
        self.itemconfig(self.width_label, text=str(width) + " m")

        self.update()

    def initPoints(self, points_list):
        for i in range(len(points_list)):
            x = self.padx + points_list[i][0]*self.PIXEL_PER_METER
            y = self.pady + points_list[i][1]*self.PIXEL_PER_METER
            self.points.append(self.create_oval(x - cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                                y - cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                                x + cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                                y + cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                                fill="red", tag="points"))

        self.update()

    def movePoints(self, points_list):
        for i in range(len(points_list)):
            x = self.padx + points_list[i][0]*self.PIXEL_PER_METER
            y = self.pady + points_list[i][1]*self.PIXEL_PER_METER
            self.coords(self.points[i], x - cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                        y - cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                        x + cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2,
                                        y + cst.PERSON_DIAMETER * self.PIXEL_PER_METER / 2)

        self.update()

    def erasePoints(self):
        self.delete("points")
        self.points.clear()

        self.update()

    # Class Functions
    def computePixelRatio(self, max_rect_size):
        min_canvas_size = min(cst.CANVAS_WIDTH-100, cst.CANVAS_HEIGHT-100)
        self.PIXEL_PER_METER = min_canvas_size / max_rect_size

    def drawClusters(self, rect_list):
        for rect in rect_list:
            pos = rect.getPos()
            w = rect.getWidth()
            h = rect.getHeight()
            self.clusters_list.append(self.create_rectangle(self.padx + (pos[0]) * self.PIXEL_PER_METER,
                                      self.pady + (pos[1]) * self.PIXEL_PER_METER,
                                      self.padx + (pos[0] + w) * self.PIXEL_PER_METER,
                                      self.pady + (pos[1] + h) * self.PIXEL_PER_METER, tag="clusters", outline="#d4d5d6"))

        self.update()

    def eraseClusters(self):
        self.clusters_list.clear()
        self.delete("clusters")
