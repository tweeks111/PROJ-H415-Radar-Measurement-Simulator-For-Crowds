import tkinter as tk
import View.Simulation


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Simulation")

        self.map_dim = [0, 0]

        self.left_frame     = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT)
        self.canvas         = View.Simulation.Canvas(self.left_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP)

        self.config_frame   = tk.Frame(self.left_frame)
        self.config_frame.pack(side=tk.BOTTOM)
        self.play_btn       = tk.Button(self.config_frame, text="\u23F8") #\u25B6
        self.play_btn.pack(side=tk.LEFT)
        self.time_value     = tk.DoubleVar()
        self.time_scale     = tk.Scale(self.config_frame, from_=0, to=10, variable=self.time_value, orient=tk.HORIZONTAL, resolution=0.01, length=300)
        self.time_scale.pack(side=tk.LEFT, fill=tk.X)

        self.right_frame    = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT)
        self.rdm_canvas     = View.Simulation.RDMCanvas(self.right_frame)
        self.rdm_canvas.get_tk_widget().pack(side=tk.LEFT)

    def initSimulation(self, pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap):
        self.canvas.drawMap()
        self.initRadar(tx_pos, rx_pos)
        self.canvas.initPoints(pos_list, color_list)
        self.rdm_canvas.initRDM(x, y, z, dmap)
        
    def updateSimulation(self, pos_list):
        self.canvas.updatePoints(pos_list)

    def closeSimulation(self):
        self.canvas.clearSimulation()
        self.rdm_canvas.clearRDM()

    def initRadar(self, tx_pos, rx_pos):
        self.canvas.initRadar(tx_pos, rx_pos)

    def clearSimulation(self):
        self.canvas.clearSimulation()
        self.rdm_canvas.clearRDM()

    def plotRDM(self, z, dmap):
        self.rdm_canvas.updateRDM(z, dmap)

    # -- Set Functions -- #

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.canvas.setMapDim(map_dim)

    def setScaleLength(self, value):
        self.time_scale.configure(from_=0, to=value)

    def setScaleValue(self, value):
        self.time_value.set(value)
