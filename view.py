import tkinter as tk

# Constants
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 580
PERSON_DIAMETER = 0.5


class View(tk.Tk):
    """
    Main Tkinter Application
    """
    # Constructor
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.left_side_panel = LeftPanel(self)
        self.canvas = Canvas(self)


class LeftPanel(tk.Frame):
    """
    Configuration Panel
    """
    # Constructor
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.pack(side=tk.LEFT, fill=tk.BOTH)

        # Left Frame Components
        self.width_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.height_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.lambda_slider = tk.Scale(self, orient=tk.HORIZONTAL)
        self.start_btn = tk.Button(self, text="Start \u25B6")

        # Components Packing
        tk.Label(self, text="Width :").grid(row=0, column=0)#pack(side="top", fill=tk.BOTH)
        self.width_slider.grid(row=0, column=1)#pack(side="top", fill=tk.BOTH)
        tk.Label(self, text="Height :").grid(row=1, column=0)#pack(side="top", fill=tk.BOTH)
        self.height_slider.grid(row=1, column=1)#pack(side="top", fill=tk.BOTH)
        tk.Label(self, text="\u03BB :").grid(row=2, column=0)
        self.lambda_slider.grid(row=2, column=1)
        self.start_btn.grid(row=3, columnspan=2)#pack(side="top", fill=tk.BOTH)

    def blockSliders(self, is_running):
        if is_running:
            self.width_slider.configure(state=tk.DISABLED, )
            self.height_slider.configure(state=tk.DISABLED)
            self.lambda_slider.configure(state=tk.DISABLED)
            self.start_btn.configure(text="Stop \u25A0")
        else:
            self.width_slider.configure(state=tk.ACTIVE)
            self.height_slider.configure(state=tk.ACTIVE)
            self.lambda_slider.configure(state=tk.ACTIVE)
            self.start_btn.configure(text="Start \u25B6")


class Canvas(tk.Canvas):
    """
    Canvas which inherit from Tkinter.Canvas
    """
    # Constructor
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="ivory")
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

    # Update Functions
    def updateRectangleDimension(self, width, height):
        pixelWidth = self.PIXEL_PER_METER * width
        pixelHeight = self.PIXEL_PER_METER * height
        self.padx = (CANVAS_WIDTH-pixelWidth)/2
        self.pady = (CANVAS_HEIGHT-pixelHeight)/2
        self.coords(self.rectangle, self.padx, self.pady, self.padx+pixelWidth, self.pady+pixelHeight)

        # Legend
        self.coords(self.width_line, self.padx, self.pady - 10, self.padx+pixelWidth, self.pady - 10)
        self.coords(self.height_line, self.padx - 10, self.pady, self.padx - 10, self.pady+pixelHeight)
        self.coords(self.height_label, self.padx-20, CANVAS_HEIGHT/2)
        self.itemconfig(self.height_label, text=str(height) + " m", angle=90)
        self.coords(self.width_label, CANVAS_WIDTH/2, self.pady-20)
        self.itemconfig(self.width_label, text=str(width) + " m")

        self.update()

    def drawPoints(self, points_list):
        self.delete("points")
        self.points.clear()
        for i in range(len(points_list)):
            x = self.padx + points_list[i][0]*self.PIXEL_PER_METER
            y = self.pady + points_list[i][1]*self.PIXEL_PER_METER
            self.points.append(self.create_oval(x - PERSON_DIAMETER * self.PIXEL_PER_METER / 2, y - PERSON_DIAMETER * self.PIXEL_PER_METER / 2, x + PERSON_DIAMETER * self.PIXEL_PER_METER / 2, y + PERSON_DIAMETER * self.PIXEL_PER_METER / 2, fill="red", tag="points"))

        self.update()

    def erasePoints(self):
        self.delete("points")
        self.points.clear()

        self.update()

    # Class Functions
    def computePixelRatio(self, max_rect_size):
        min_canvas_size = min(CANVAS_WIDTH-100, CANVAS_HEIGHT-100)
        self.PIXEL_PER_METER = min_canvas_size / max_rect_size
