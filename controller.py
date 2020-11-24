from View import View
from Model import Model
import time
import random
from constants import *
import numpy as np

class Controller:
    # Constructor
    def __init__(self):
        self.map_dim = [0, 0]
        self.colors = ['#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#FFE4C4', '#000000', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#A9A9A9', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#F8F8FF', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#808080', '#F0FFF0', '#FF69B4', '#CD5C5C', '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#D3D3D3', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080', '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#663399', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3', '#FFFFFF', '#F5F5F5', '#FFFF00', '#9ACD32']
        
        self.view = View()
        self.model = Model()
        self.configureSizeDialog()
        self.configureEditorWindow()

        self.view.simulation_window.protocol("WM_DELETE_WINDOW", self.closeSimulation)
        self.is_running = False

        self.view.editor_window.mainloop()

    # Controller Functions
    def addCluster(self):
        random_color_index = random.randrange(0, len(self.colors))
        color = self.colors[random_color_index]
        self.colors.remove(color)

        if self.view.editor_window.left_panel.clusters_listbox.size() == 0:
            [r, x, y, v, theta, lambda0] = self.view.editor_window.left_panel.getClustersSettings()
            self.view.editor_window.right_panel.run_btn['state'] = 'normal'
        else:
            [r, x, y, v, theta, lambda0] = [(MAX_RADIUS - MIN_RADIUS) / 2 + MIN_RADIUS, self.map_dim[0] / 2, self.map_dim[1] / 2, (MAX_SPEED - MIN_SPEED) / 2 + MIN_SPEED, 0, 0.5]
        self.model.addCluster(r, x, y, v, theta, lambda0, color)
        self.view.addCluster(r, x, y, v, theta, color)

    def removeCluster(self):
        index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
        self.colors.append(self.view.editor_window.canvas.clusters_colors[index])
        self.view.removeCluster(index)
        self.model.removeCluster(index)
        self.selectCluster(None)
        if self.view.editor_window.left_panel.clusters_listbox.size() == 0:
            self.view.editor_window.right_panel.run_btn['state'] = 'disabled'

    def selectCluster(self, event):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
            [r, x, y, v, theta, lambda0] = self.model.getClusterSettings(index)
            self.view.selectCluster(index, r, x, y, v, theta, lambda0)

    # Configuration
    def configureSizeDialog(self):
        self.view.size_dialog.ok_button.configure(command=self.initMapSize)

    def configureEditorWindow(self):
        self.view.editor_window.left_panel.add_cluster_btn.configure(command=self.addCluster)
        self.view.editor_window.left_panel.remove_cluster_btn.configure(command=self.removeCluster)
        self.view.editor_window.left_panel.clusters_listbox.bind('<<ListboxSelect>>', self.selectCluster)
        self.view.editor_window.left_panel.radius_scale.configure(command=self.updateRadius)
        self.view.editor_window.left_panel.x_scale.configure(command=self.updateClusterSettings)
        self.view.editor_window.left_panel.y_scale.configure(command=self.updateClusterSettings)
        self.view.editor_window.left_panel.v_scale.configure(command=self.updateClusterSettings)
        self.view.editor_window.left_panel.angle_scale.configure(command=self.updateClusterSettings)
        self.view.editor_window.left_panel.lambda_scale.configure(command=self.updateClusterSettings)
        self.view.editor_window.right_panel.run_btn.configure(command=self.runSimulation)

        self.view.editor_window.right_panel.TX_x_scale.configure(command=self.updateRadarSettings)
        self.view.editor_window.right_panel.TX_y_scale.configure(command=self.updateRadarSettings)
        self.view.editor_window.right_panel.RX_x_scale.configure(command=self.updateRadarSettings)
        self.view.editor_window.right_panel.RX_y_scale.configure(command=self.updateRadarSettings)

    def initMapSize(self):
        self.map_dim = self.view.size_dialog.getValues()
        self.view.setMapDim(self.map_dim)
        self.model.setMapDim(self.map_dim)

        [tx_x, tx_y, rx_x, rx_y] = self.view.editor_window.right_panel.getRadarSettings()
        self.view.initRadar(tx_x, tx_y, rx_x, rx_y)
        self.model.setRadarPos([tx_x, tx_y], [rx_x, rx_y])

        self.view.centerWindow()
        self.view.title("Editor")

    def updateClusterSettings(self, var):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
            [r, x, y, v, theta, lambda0] = self.view.editor_window.left_panel.getClustersSettings()
            self.view.updateClusterSettings(r, x, y, v, theta, index)
            self.model.updateClusterSettings(r, x, y, v, theta, lambda0, index)

    def updateRadarSettings(self, var):
        [tx_x, tx_y, rx_x, rx_y] = self.view.editor_window.right_panel.getRadarSettings()
        self.model.setRadarPos([tx_x, tx_y], [rx_x, rx_y])
        self.view.updateRadarSettings(tx_x, tx_y, rx_x, rx_y)

    def updateRadius(self, r):
        self.view.updateRadius(r)
        self.updateClusterSettings(None)

    def runSimulation(self):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            # TODO : when moving the window some points change their position
            self.view.editor_window.right_panel.run_btn.configure(command=self.closeSimulation, text="Stop Simulation")

            self.model.initSimulation()

            pos_list = self.model.getPointsPosition()
            color_list = self.model.getPointsColor()
            tx_pos, rx_pos = self.model.getRadarPosition()
            x, y, z = self.model.computeParameters()

            self.view.initSimulation(pos_list, color_list, tx_pos, rx_pos, x, y, z)
            self.view.simulation_window.update()
            self.is_running = True

            Ts = 0.01
            duration = 10
            tlist = np.arange(0, duration, Ts)
            RDM_list = []
            all_pos_list = []

            for t in tlist:
                all_pos_list.append(self.model.updatePointsPosition(Ts))
                if (t % 0.5) == 0:
                    RDM_list.append(self.model.computeParameters()[2])
                    print(t)

            i = 0
            j = 0


            while self.is_running:

                self.view.updateSimulation(all_pos_list[i])
                if (tlist[i] % 0.5) == 0:
                    self.view.updateRDM(RDM_list[j])
                    j = j + 1
                    if j > len(RDM_list) - 1:
                        j = 0
                self.view.simulation_window.update()
                time.sleep(Ts)
                i = i + 1

                if i > len(tlist) - 1:
                    i = 0

    def closeSimulation(self):
        self.is_running = False
        self.view.editor_window.right_panel.run_btn.configure(command=self.runSimulation, text="Run Simulation")
        self.view.simulation_window.withdraw()
        self.view.clearSimulation()
