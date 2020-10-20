from Model.cluster import Cluster
from Model.person import Person
import numpy as np
import scipy.stats
import math


def poissonPointProcess(cluster, lambda0):
    nb_points = scipy.stats.poisson(lambda0 * cluster.getArea()).rvs()
    r = cluster.getRadius() * np.random.uniform(0, 1, nb_points)
    theta = 2 * math.pi * np.random.uniform(0, 1, nb_points)
    x0 = [math.cos(i) for i in theta]
    y0 = [math.sin(i) for i in theta]
    x1 = np.multiply(r, x0)
    y1 = np.multiply(r, y0)
    x = [i + cluster.getX() for i in x1]
    y = [i + cluster.getY() for i in y1]

    return np.array([x, y])


class Model:
    # Constructor
    def __init__(self):
        self.map_dim = [0, 0]
        self.clusters_list = []
        self.points_list = []

    def addCluster(self, r, x, y, v, theta, color):
        self.clusters_list.append(Cluster(r, x, y, v, theta, color))

    def removeCluster(self, index):
        del self.clusters_list[index]

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.clusters_list[index].updateClusterSettings(r, x, y, v, theta)

    def initSimulation(self):
        self.points_list.clear()

        for cluster in self.clusters_list:
            temp_pos_list = poissonPointProcess(cluster, 0.3)
            v = cluster.getSpeed()
            theta = cluster.getAngle()
            color = cluster.getColor()
            for i in range(0, temp_pos_list.shape[1]):
                self.points_list.append(Person(temp_pos_list[0, i], temp_pos_list[1, i], v, theta, color))

    def getPointsPosition(self):
        pos_list = []
        for point in self.points_list:
            pos_list.append([point.getX(), point.getY()])
        return pos_list

    def getPointsColor(self):
        color_list = []
        for point in self.points_list:
            color_list.append(point.getColor())
        return color_list

    def updatePointsPosition(self, time):
        pos_list = []
        for point in self.points_list:
            x = point.getX()
            y = point.getY()
            # TODO : there is a problem in which the point can go through the bounds cause x is already bigger than map_dim
            if x < 0 or x > self.map_dim[0]:
                point.oppositeVX()
            if y < 0 or y > self.map_dim[1]:
                point.oppositeVY()
            point.updatePos(time)
            pos_list.append(point.getPos())

        return pos_list

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

    def getClusterSettings(self, index):
        return self.clusters_list[index].getClusterSettings()
