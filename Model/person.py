import math


class Person:

    def __init__(self, x, y, v, theta):
        # Person(x, y)
        self.x = x
        self.y = y

        self.vx = v * math.cos(theta)
        self.vy = v * math.sin(theta)

    # Get Functions
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return [self.x, self.y]

    def getSpeed(self):
        return [self.vx, self.vy]

    # Set Functions

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def setVelocity(self, vel):
        self.vx = vel[0]
        self.vy = vel[1]

    def oppositeVX(self):
        self.vx = - self.vx

    def oppositeVY(self):
        self.vy = -self.vy

    def updatePos(self, time):
        self.x = self.x + self.vx*time
        self.y = self.y + self.vy*time
