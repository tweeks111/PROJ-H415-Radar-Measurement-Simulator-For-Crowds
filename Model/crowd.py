import numpy as np
import scipy.stats
import random
import math

MIN_SPEED = 0.9
MAX_SPEED = 1.4


class Crowd:
    lambda0 = 0.1

    # Constructor
    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.points_list = None
        self.speed_list = None
        self.nb_points = 0

    # Class Functions
    def poissonPointProcess(self):
        self.nb_points = scipy.stats.poisson(self.lambda0 * self.rectangle.getArea()).rvs()
        x = self.rectangle.width * scipy.stats.uniform.rvs(0, 1, (self.nb_points, 1))
        y = self.rectangle.height * scipy.stats.uniform.rvs(0, 1, (self.nb_points, 1))

        self.points_list = np.concatenate((x, y), axis=1)

    def randomSpeed(self):
        self.speed_list = np.empty((self.nb_points, 2))
        for i in range(self.nb_points):
            phi = random.uniform(0, 2 * math.pi)
            speed = random.uniform(MIN_SPEED, MAX_SPEED)
            vx = speed * math.cos(phi)
            vy = speed * math.sin(phi)
            self.speed_list[i][0] = vx
            self.speed_list[i][1] = vy

    def initPoints(self):
        self.poissonPointProcess()
        self.randomSpeed()

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