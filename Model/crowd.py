import numpy as np
import scipy.stats
import random
import math
import constants as cst
from Model.rectangle import Rectangle


class Crowd:
    lambda0 = 0.5

    # Constructor
    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.points_list = None
        self.speed_list = None
        self.rect_list = []
        self.nb_points = 0

    # Class Functions
    def poissonPointProcess(self, rectangle):
        nb_points = scipy.stats.poisson(self.lambda0 * rectangle.getArea()).rvs()
        x = rectangle.width * scipy.stats.uniform.rvs(0, 1, (nb_points, 1)) + rectangle.pos[0]
        y = rectangle.height * scipy.stats.uniform.rvs(0, 1, (nb_points, 1)) + rectangle.pos[1]

        return np.concatenate((x, y), axis=1)

    def randomSpeed(self):
        self.speed_list = np.empty((self.nb_points, 2))
        for i in range(self.nb_points):
            phi = random.uniform(0, 2 * math.pi)
            speed = random.uniform(cst.MIN_SPEED, cst.MAX_SPEED)
            vx = speed * math.cos(phi)
            vy = speed * math.sin(phi)
            self.speed_list[i][0] = vx
            self.speed_list[i][1] = vy

    def initPoints(self, clusters_check):
        self.rect_list = []
        if not clusters_check:
            self.rect_list.append(self.rectangle)
            self.points_list = self.poissonPointProcess(self.rectangle)
        else:
            self.divideRectangle(self.rectangle)
            temp_list = []
            for i in range(len(self.rect_list)):
                temp_list.append(self.poissonPointProcess(self.rect_list[i]))
            self.points_list = np.vstack(temp_list)

        self.nb_points = len(self.points_list)
        self.randomSpeed()

    def divideRectangle(self, rectangle):
        rectWidth = rectangle.getWidth()
        rectHeight = rectangle.getHeight()
        w = random.uniform(0.2 * rectWidth, 0.8 * rectWidth)
        h = random.uniform(0.2 * rectHeight, 0.8 * rectHeight)
        self.rect_list.append(Rectangle(w, h, [0, 0]))
        self.rect_list.append(Rectangle(w, rectHeight - h, [0, h]))
        self.rect_list.append(Rectangle(rectWidth - w, h, [w, 0]))
        self.rect_list.append(Rectangle(rectWidth - w, rectHeight - h, [w, h]))

    def updatePosition(self, delta_time):
        for i in range(self.nb_points):
            x = self.points_list[i][0]
            y = self.points_list[i][1]
            vx = self.speed_list[i][0]
            vy = self.speed_list[i][1]
            new_x = x + vx * delta_time
            new_y = y + vy * delta_time

            # Out of rectangle
            if new_x < 0 or new_x > self.rectangle.getWidth():
                self.speed_list[i][0] = -vx
                new_x = x - vx * delta_time
            if new_y < 0 or new_y > self.rectangle.getHeight():
                self.speed_list[i][1] = -vy
                new_y = y - vy * delta_time

            # New Position Computation
            self.points_list[i] = [new_x, new_y]

    # Set Functions
    def setLambda(self, lambda0):
        self.lambda0 = lambda0

    # Get Functions
    def getPointsList(self):
        return self.points_list

    def getSpeedList(self):
        return self.speed_list

    def getLambda(self):
        return self.lambda0

    def getNbPoints(self):
        return self.nb_points
