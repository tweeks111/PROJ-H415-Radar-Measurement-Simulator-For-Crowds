import math


class Cluster:
    def __init__(self, r, x, y, v, theta):
        self.r = r
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        self.area = self.computeArea()

    def updateClusterSettings(self, r, x, y, v, theta):
        self.r = r
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        self.area = self.computeArea()

    def computeArea(self):
        return math.pi * self.r ** 2
