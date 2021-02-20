from View import View
from Model import Model
import time
import random
import math
from constants import *
import numpy as np


class Controller:
    # Constructor
    def __init__(self):
        self.colors = ['#CF1020', '#FBC028', '#2863FB', '#FB6828', '#FF6F6F', '#EFFF9F', '#7FFFCF', '#CFFF8F',
                       '#B56357', '#D8D8D6', '#2F5D8C', '#A0B3C1', '#EE1AB0', '#53555C', '#4DEAE6', '#BE95EA', '#A7EA9D']

        self.map_dim        = [0, 0]
        self.Ts             = 0.01
        self.tlist          = None
        self.all_pos_list   = []
        self.RDM_list       = []
        self.AoA_list = []
        self.est_list = []
        self.dmap_list      = []
        self.rdm_time       = 0
        self.time_index     = 0
        self.detectionMode = "Threshold"

        self.view = View()
        self.model = Model()
        self.model.computeResolutionParameters()
        self.configureSizeDialog()
        self.configureEditorWindow()
        self.configureSimulationWindow()

        self.view.simulation_window.protocol("WM_DELETE_WINDOW", self.closeSimulation)
        self.is_running = False
        self.is_paused  = False
        self.view.editor_window.mainloop()

    # Controller Functions
    def addCluster(self):
        random_color_index = random.randrange(0, len(self.colors))
        color = self.colors[random_color_index]
        self.colors.remove(color)
        is_checked = self.view.editor_window.left_panel.btnVar.get()
        if self.view.editor_window.left_panel.clusters_listbox.size() == 0:
            [r, x, y, v, theta, lambda0] = self.view.editor_window.left_panel.getClustersSettings()
            if is_checked == 1:
                r = 0.15
            self.view.editor_window.right_panel.run_btn['state'] = 'normal'
            self.view.editor_window.right_panel.analysis_btn['state'] = 'normal'
        else:
            [r, x, y, v, theta, lambda0] = [(MAX_RADIUS - MIN_RADIUS) / 2 + MIN_RADIUS, self.map_dim[0] / 2,
                                            self.map_dim[1] / 2, (MAX_SPEED - MIN_SPEED) / 2 + MIN_SPEED, 0, 0.5]
        self.model.addCluster(r, x, y, v, theta, lambda0, color, self.view.editor_window.left_panel.btnVar.get())

        self.view.addCluster(r, x, y, v, theta, color, is_checked)

    def removeCluster(self):
        index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
        self.colors.append(self.view.editor_window.canvas.clusters_colors[index])
        self.view.removeCluster(index)
        self.model.removeCluster(index)
        self.selectCluster(None)
        if self.view.editor_window.left_panel.clusters_listbox.size() == 0:
            self.view.editor_window.right_panel.run_btn['state'] = 'disabled'
            self.view.editor_window.right_panel.analysis_btn['state'] = 'disabled'

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
        self.view.editor_window.left_panel.point_btn.configure(command=self.checkBtn)
        self.view.editor_window.left_panel.TX_x_scale.configure(command=self.updateRadarSettings)
        self.view.editor_window.left_panel.TX_y_scale.configure(command=self.updateRadarSettings)
        self.view.editor_window.left_panel.RX_x_scale.configure(command=self.updateRadarSettings)
        self.view.editor_window.left_panel.RX_y_scale.configure(command=self.updateRadarSettings)

        self.view.editor_window.right_panel.run_btn.configure(command=self.runSimulation)

    def configureSimulationWindow(self):
        self.view.simulation_window.play_btn.configure(command=self.pauseSimulation)
        self.view.simulation_window.time_scale.configure(command=self.changeTimeScale)

    def initMapSize(self):
        self.map_dim = self.view.size_dialog.getValues()
        self.view.setMapDim(self.map_dim)
        self.model.setMapDim(self.map_dim)

        [tx_x, tx_y, rx_x, rx_y] = self.view.editor_window.left_panel.getRadarSettings()
        self.view.initRadar(tx_x, tx_y, rx_x, rx_y)
        self.model.setRadarPos([tx_x, tx_y], [rx_x, rx_y])

        self.view.centerWindow()
        self.view.title("Editor")

    def updateClusterSettings(self, var):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
            [r, x, y, v, theta, lambda0]    = self.view.editor_window.left_panel.getClustersSettings()
            is_checked = self.view.editor_window.left_panel.btnVar.get()
            if is_checked == 1:
                r = 0.15
            self.view.updateClusterSettings(r, x, y, v, theta, index, is_checked)
            self.model.updateClusterSettings(r, x, y, v, theta, lambda0, index)

    def updateRadarSettings(self, var):
        [tx_x, tx_y, rx_x, rx_y]    = self.view.editor_window.left_panel.getRadarSettings()
        self.model.setRadarPos([tx_x, tx_y], [rx_x, rx_y])
        is_smaller = self.model.getRadarIsSmaller()
        self.view.updateRadarSettings(tx_x, tx_y, rx_x, rx_y, is_smaller)

    def updateRadius(self, r):
        self.view.updateRadius(r)
        self.updateClusterSettings(None)

    def runSimulation(self):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            self.view.editor_window.right_panel.run_btn.configure(command=self.closeSimulation, text="Stop Simulation")
            self.view.editor_window.right_panel.analysis_btn['state'] = 'disabled'

            N, M = int(self.view.editor_window.right_panel.n_scale.get()), int(self.view.editor_window.right_panel.n_scale.get())
            pfa = self.view.editor_window.right_panel.proba_scale.get()
            Ncfar = self.view.editor_window.right_panel.NCFAR_scale.get()
            guard = self.view.editor_window.right_panel.guard_scale.get()
            kcfar = self.view.editor_window.right_panel.kCFAR_scale.get()
            detectionMode = self.view.editor_window.right_panel.combo_detect.get()
            self.model.initSimulation(N, M, self.view.editor_window.right_panel.detect_thresh.get(), pfa, kcfar, Ncfar, guard, self.view.editor_window.right_panel.aoa_thresh.get(), detectionMode)

            pos_list                = self.model.getPointsPosition()
            color_list              = self.model.getPointsColor()
            tx_pos, rx_pos          = self.model.getRadarPosition()
            x, y, z, dmap, AoA, est = self.model.computeRDM()

            self.view.initSimulation(pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap, AoA)
            self.view.simulation_window.update()
            self.view.simulation_window.setNbPoints(len(pos_list))

            self.is_running     = True
            self.is_paused      = False

            self.rdm_time       = round(1 / self.view.editor_window.right_panel.rdm_scale.get(), 2)
            duration            = self.view.editor_window.right_panel.time_scale.get()
            self.view.simulation_window.setScaleLength(duration-self.Ts)
            self.tlist          = np.arange(0, duration, self.Ts)
            self.RDM_list       = []
            self.dmap_list      = []
            self.AoA_list       = []
            self.est_list       = []
            self.all_pos_list   = []
            totalEst            = 0

            for t in self.tlist:
                self.all_pos_list.append(self.model.updatePointsPosition(self.Ts))
                if ((t / self.rdm_time) % 1) == 0:
                    _, _, z, dmap, AoA, est = self.model.computeRDM()

                    self.RDM_list.append(z)
                    self.dmap_list.append(dmap)
                    self.AoA_list.append(AoA)
                    self.est_list.append(est)
                    totalEst = totalEst + est

                    # TODO : correct the problem of 0.99%0.33 = 1 and not 1 => delay
                self.view.editor_window.right_panel.bar(t)

            totalEst = round(totalEst/len(self.est_list))

            self.view.simulation_window.deiconify()
            self.time_index = 0

            self.view.updateSimulation(self.all_pos_list[0])
            self.view.updateRDM(self.RDM_list[0], self.dmap_list[0], self.AoA_list[0], self.est_list[0])
            self.view.setTotalEst(totalEst)
            self.view.simulation_window.update_idletasks()

            while self.is_running:
                if not self.is_paused:

                    self.view.simulation_window.setScaleValue(self.time_index * self.Ts)
                    # TODO : correct fact that time is not equal to real time

                    self.displayAtTimeIndex()

                    self.time_index = self.time_index + 1
                    if self.time_index > len(self.tlist) - 1:
                        self.time_index = 0

                    self.view.simulation_window.update()
                else:
                    self.view.simulation_window.update()
                    time.sleep(0.1)

    def closeSimulation(self):
        self.is_running = False
        self.view.editor_window.right_panel.analysis_btn['state'] = 'normal'
        self.view.simulation_window.play_btn.configure(text="\u23F8")
        self.view.editor_window.right_panel.run_btn.configure(command=self.runSimulation, text="Run Simulation")
        self.view.editor_window.right_panel.bar(0)
        self.view.simulation_window.withdraw()
        self.view.clearSimulation()

    def pauseSimulation(self):
        if self.is_paused:
            self.view.simulation_window.play_btn.configure(text="\u23F8")
        else:
            self.view.simulation_window.play_btn.configure(text="\u25B6")
        self.is_paused = not self.is_paused

    def changeTimeScale(self, unused):
        value = self.view.simulation_window.time_value.get()
        self.time_index = int(value / self.Ts)
        self.displayAtTimeIndex()

    def displayAtTimeIndex(self):
        self.view.updateSimulation(self.all_pos_list[self.time_index])
        rdm_index = math.floor((self.time_index*self.Ts) / self.rdm_time)
        self.view.updateRDM(self.RDM_list[rdm_index], self.dmap_list[rdm_index], self.AoA_list[rdm_index], self.est_list[rdm_index])
        time.sleep(self.Ts)

    def checkBtn(self):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            is_checked = self.view.editor_window.left_panel.btnVar.get()
            index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
            self.model.setIsPoint(is_checked, index)
            [r, x, y, v, theta, lambda0] = self.view.editor_window.left_panel.getClustersSettings()

            if is_checked == 1:
                self.view.editor_window.left_panel.lambda_scale['state'] = 'disable'
                self.view.editor_window.left_panel.lambda_scale['sliderrelief'] = "sunken"
                self.view.editor_window.left_panel.radius_scale['state'] = 'disable'
                self.view.editor_window.left_panel.radius_scale['sliderrelief'] = "sunken"
                r = 0.15

            else:
                self.view.editor_window.left_panel.lambda_scale['state'] = 'normal'
                self.view.editor_window.left_panel.lambda_scale['sliderrelief'] = 'raised'
                self.view.editor_window.left_panel.radius_scale['state'] = 'normal'
                self.view.editor_window.left_panel.radius_scale['sliderrelief'] = "raised"

            self.updateRadius(r)
            self.model.updateClusterSettings(r, x, y, v, theta, lambda0, index)
            self.view.updateClusterSettings(r, x, y, v, theta, index, is_checked)
