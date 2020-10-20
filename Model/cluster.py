import math


class Cluster:
    def __init__(self, r, x, y, v, theta, color):
        self.r = r
        self.x = x
        self.y = y
        self.v = v / 3.6
        self.theta = theta * math.pi/180
        self.area = self.computeArea()
        self.color = color

    def updateClusterSettings(self, r, x, y, v, theta):
        self.r = r
        self.x = x
        self.y = y
        self.v = v / 3.6
        self.theta = theta * math.pi/180
        self.area = self.computeArea()

    def computeArea(self):
        return math.pi * self.r ** 2

    def getRadius(self):
        return self.r

    def getArea(self):
        return self.area

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getAngle(self):
        return self.theta

    def getSpeed(self):
        return self.v

    def getClusterSettings(self):
        return [self.r, self.x, self.y, self.v * 3.6, self.theta * 180/math.pi]

    def getColor(self):
        return self.color