import tkinter as tk
from constants import *


class LeftPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.LEFT, fill=tk.BOTH)

        self.map_dim = [0, 0]
        self.radius = tk.DoubleVar()

        # Clusters Frame
        #    Listbox
        self.cluster_frame = tk.LabelFrame(self, text="Clusters")
        self.cluster_frame.configure(padx=5, pady=5)
        self.cluster_frame.pack()
        yScroll = tk.Scrollbar(self.cluster_frame, orient=tk.VERTICAL)
        self.clusters_listbox = tk.Listbox(self.cluster_frame, yscrollcommand=yScroll.set, activestyle='none', selectbackground="red")
        self.clusters_listbox.grid(row=1, column=0, sticky='nsew')
        yScroll.grid(row=1, column=1, sticky='ns')
        yScroll['command'] = self.clusters_listbox.yview()
        self.clusters_colors = []
        #   Buttons
        self.remove_cluster_btn = tk.Button(self.cluster_frame, text="Remove")
        self.remove_cluster_btn.grid(row=2, column=0, sticky='e')
        self.remove_cluster_btn['state'] = "disabled"
        self.add_cluster_btn = tk.Button(self.cluster_frame, text="Add")
        self.add_cluster_btn.grid(row=2, column=1)

        # Clusters configuration
        self.clusters_config = tk.LabelFrame(self, text="Configuration")
        self.clusters_config.configure(padx=5, pady=5)
        self.clusters_config.pack(fill=tk.X)

        radius_label = tk.Label(self.clusters_config, text="Radius :\n[m]")
        radius_label.grid(row=0, column=0)
        self.radius_scale = tk.Scale(self.clusters_config, from_=MIN_RADIUS, to=MAX_RADIUS, orient=tk.HORIZONTAL, resolution=0.1, var=self.radius)
        self.radius_scale.grid(row=0, column=1)
        x_label = tk.Label(self.clusters_config, text="x :\n[m]")
        x_label.grid(row=1, column=0)
        self.x_scale = tk.Scale(self.clusters_config, from_=0, to=0, orient=tk.HORIZONTAL, resolution=0.1)
        self.x_scale.grid(row=1, column=1)
        y_label = tk.Label(self.clusters_config, text="y :\n[m]")
        y_label.grid(row=2, column=0)
        self.y_scale = tk.Scale(self.clusters_config, from_=0, to=0, orient=tk.HORIZONTAL, resolution=0.1)
        self.y_scale.grid(row=2, column=1)
        v_label = tk.Label(self.clusters_config, text="v :\n[km/h]")
        v_label.grid(row=3, column=0)
        self.v_scale = tk.Scale(self.clusters_config, from_=MIN_SPEED, to=MAX_SPEED, resolution=0.5, orient=tk.HORIZONTAL)
        self.v_scale.grid(row=3, column=1)
        angle_label = tk.Label(self.clusters_config, text="\u03B8 :\n[°]")
        angle_label.grid(row=4, column=0)
        self.angle_scale = tk.Scale(self.clusters_config, from_=0, to=360, resolution=15, orient=tk.HORIZONTAL)
        self.angle_scale.grid(row=4, column=1)
        lambda_label = tk.Label(self.clusters_config, text="\u03BB :")
        lambda_label.grid(row=5, column=0)
        self.lambda_scale = tk.Scale(self.clusters_config, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.lambda_scale.set(0.5)
        self.lambda_scale.grid(row=5, column=1)

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
        self.run_btn.pack()

    def updateRadius(self, r):
        self.x_scale.configure(from_=float(r), to=self.map_dim[0]-float(r))
        self.y_scale.configure(from_=float(r), to=self.map_dim[1]-float(r))

    def addCluster(self, color):
        self.clusters_listbox.insert('end', "Cluster "+str(self.clusters_listbox.size()+1))
        self.clusters_listbox.itemconfig('end', {'bg':color})
        self.clusters_listbox.select_clear(0, 'end')
        self.clusters_listbox.select_set('end')
        self.clusters_listbox.event_generate("<<ListboxSelect>>")
        self.remove_cluster_btn['state'] = 'normal'

    def removeCluster(self):
        selected_index = self.clusters_listbox.curselection()
        self.clusters_listbox.delete(selected_index)

        self.clusters_listbox.select_clear(0, 'end')
        self.clusters_listbox.select_set('end')

        if not self.clusters_listbox.curselection():
            self.remove_cluster_btn['state'] = "disabled"

    def selectCluster(self, r, x, y, v, theta, lambda0):
        self.remove_cluster_btn['state'] = "normal"
        self.setSliders(r, x, y, v, theta, lambda0)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.x_scale.configure(from_=self.radius.get(), to=map_dim[0]-self.radius.get())
        self.y_scale.configure(from_=self.radius.get(), to=map_dim[0]-self.radius.get())
        self.radius_scale.set((MAX_RADIUS - MIN_RADIUS) / 2 + MIN_RADIUS)
        self.x_scale.set(map_dim[0]/2)
        self.y_scale.set(map_dim[1]/2)
        self.v_scale.set((MAX_SPEED-MIN_SPEED)/2+MIN_SPEED)
        self.update()

    def getClustersSettings(self):
        return [self.radius_scale.get(), self.x_scale.get(), self.y_scale.get(), self.v_scale.get(), self.angle_scale.get(), self.lambda_scale.get()]

    def setSliders(self, r, x, y, v, theta, lambda0):
        self.radius_scale.set(r)
        self.x_scale.set(x)
        self.y_scale.set(y)
        self.v_scale.set(v)
        self.angle_scale.set(theta)
        self.lambda_scale.set(lambda0)

