import tkinter as tk
from constants import *


class RightPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.map_dim = [0, 0]

        # Radar Frame
        self.radar_frame = tk.LabelFrame(self, text="Radar")
        self.radar_frame.configure(padx=5, pady=5)
        self.radar_frame.pack(fill=tk.X)
        TX_label = tk.Label(self.radar_frame, text="TX :")
        TX_label.grid(row=0, column=0)
        TX_x_label = tk.Label(self.radar_frame, text="x :\n[m]")
        TX_x_label.grid(row=0, column=1)
        self.TX_x_scale = tk.Scale(self.radar_frame, from_=0, to=0, orient=tk.HORIZONTAL, resolution=0.1)
        self.TX_x_scale.grid(row=0, column=2)
        TX_y_label = tk.Label(self.radar_frame, text="y :\n[m]")
        TX_y_label.grid(row=1, column=1)
        self.TX_y_scale = tk.Scale(self.radar_frame, from_=0, to=0, orient=tk.HORIZONTAL, resolution=0.1)
        self.TX_y_scale.grid(row=1, column=2)
        RX_label = tk.Label(self.radar_frame, text="RX :")
        RX_label.grid(row=2, column=0)
        RX_x_label = tk.Label(self.radar_frame, text="x :\n[m]")
        RX_x_label.grid(row=2, column=1)
        self.RX_x_scale = tk.Scale(self.radar_frame, from_=0, to=0, orient=tk.HORIZONTAL, resolution=0.1)
        self.RX_x_scale.grid(row=2, column=2)
        RX_y_label = tk.Label(self.radar_frame, text="y :\n[m]")
        RX_y_label.grid(row=3, column=1)
        self.RX_y_scale = tk.Scale(self.radar_frame, from_=0, to=0, orient=tk.HORIZONTAL, resolution=0.1)
        self.RX_y_scale.grid(row=3, column=2)

        self.run_btn = tk.Button(self, text="Run Simulation")
        self.run_btn['state'] = 'disabled'
        self.run_btn.pack(fill=tk.BOTH)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

        self.TX_x_scale.configure(from_=0, to=map_dim[0])
        self.TX_y_scale.configure(from_=0, to=map_dim[1])
        self.RX_x_scale.configure(from_=0, to=map_dim[0])
        self.RX_y_scale.configure(from_=0, to=map_dim[1])

        self.TX_x_scale.set(0.2*map_dim[0])
        self.TX_y_scale.set(map_dim[1])
        self.RX_x_scale.set(0.8*map_dim[0])
        self.RX_y_scale.set(map_dim[1])

    def getRadarSettings(self):
        return [self.TX_x_scale.get(), self.TX_y_scale.get(), self.RX_x_scale.get(), self.RX_y_scale.get()]
