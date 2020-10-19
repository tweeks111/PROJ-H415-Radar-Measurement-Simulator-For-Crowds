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

        self.rect_list = []
        self.points_list = None
        self.speed_list = None
        self.clusters_list = None

        self.nb_points = 0
        self.avr_nb_points = 0
        self.division = 2
        self.nb_clusters = 2

    # Class Functions

    def randomCircle(self):
        print("ok")

    def computeLambda(self):
        self.lambda0 = self.avr_nb_points / self.rectangle.getArea()

    def randomSpeed(self, nb_points):
        self.speed_list = np.empty((nb_points, 2))
        phi = random.uniform(0, 2 * math.pi)
        speed = random.uniform(cst.MIN_SPEED, cst.MAX_SPEED)
        vx = speed * math.cos(phi)
        vy = speed * math.sin(phi)
        for i in range(nb_points):
            self.speed_list[i][0] = vx
            self.speed_list[i][1] = vy

    def initPoints(self, clusters_check):
        self.computeLambda()
        print(self.lambda0)

        if not clusters_check:
            self.rect_list.append(self.rectangle)
            self.points_list = poissonPointProcess(self.rectangle, self.lambda0)
        else:
            self.rect_list = divideRectangle(self.rectangle)
            for i in range(self.nb_clusters):
                temp_rectangle_list = []
                for rect in self.rect_list:
                    temp_rectangle_list.extend(divideRectangle(rect))
                self.rect_list = temp_rectangle_list

            temp_list = []
            print(len(self.rect_list))
            for i in range(len(self.rect_list)):
                rand_lambda0 = round(random.uniform(0.1, 1), 1)
                temp_list.append(poissonPointProcess(self.rect_list[i], rand_lambda0))
            self.points_list = np.vstack(temp_list)

        self.nb_points = len(self.points_list)
        self.randomSpeed(self.nb_points)

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

    def setNbPoints(self, nb_points):
        self.avr_nb_points = nb_points

    # Get Functions
    def getPointsList(self):
        return self.points_list

    def getRectList(self):
        return self.rect_list

    def getSpeedList(self):
        return self.speed_list

    def getLambda(self):
        return self.lambda0

    def getNbPoints(self):
        return self.nb_points
