from View import View
from Model import Model


class Controller:
    # Constructor
    def __init__(self):
        self.map_dim = [0, 0]

        self.view = View()
        self.model = Model()
        self.configureSizeDialog()
        self.configureEditorWindow()

        self.view.mainloop()

    # Controller Functions
    def addCluster(self):
        [r, x, y, v, theta] = self.view.editor_window.left_panel.getClustersSettings()
        self.view.addCluster(r, x, y, v, theta)
        self.model.addCluster(r, x, y, v, theta)

    def removeCluster(self):
        index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
        self.view.removeCluster(index)
        self.model.removeCluster(index)
        self.selectCluster(None)

    def selectCluster(self, event):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
            self.view.selectCluster(index)

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

    def initMapSize(self):
        self.map_dim = self.view.size_dialog.getValues()
        self.view.setMapDim(self.map_dim)

    def updateClusterSettings(self, var):
        if self.view.editor_window.left_panel.clusters_listbox.size() > 0:
            index = self.view.editor_window.left_panel.clusters_listbox.curselection()[0]
            [r, x, y, v, theta] = self.view.editor_window.left_panel.getClustersSettings()
            self.view.updateClusterSettings(r, x, y, v, theta, index)
            self.model.updateClusterSettings(r, x, y, v, theta, index)

    def updateRadius(self, r):
        self.view.updateRadius(r)
        self.updateClusterSettings(None)
