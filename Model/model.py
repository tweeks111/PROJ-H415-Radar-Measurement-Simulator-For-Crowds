from Model.cluster import Cluster


class Model:
    # Constructor
    def __init__(self):
        self.map_dim = [0, 0]
        self.clusters_list = []

    def addCluster(self, r, x, y, v, theta):
        self.clusters_list.append(Cluster(r, x, y, v, theta))

    def removeCluster(self, index):
        del self.clusters_list[index]

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.clusters_list[index].updateClusterSettings(r, x, y, v, theta)
