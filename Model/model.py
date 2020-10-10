from Model.rectangle import Rectangle
from Model.crowd import Crowd
import constants as cst
import time


class Model:
    # Constructor
    def __init__(self):
        self.rectangle = Rectangle((cst.MAX_RECTANGLE - cst.MIN_RECTANGLE) / 2 + cst.MIN_RECTANGLE,
                                   (cst.MAX_RECTANGLE - cst.MIN_RECTANGLE) / 2 + cst.MIN_RECTANGLE,
                                   [0, 0])

        self.crowd = Crowd(self.rectangle)

    # Class Functions
    def initCrowd(self, clusters_check):
        self.crowd.initPoints(clusters_check)

    def run(self, delta_time):
        self.crowd.updatePosition(delta_time)

    # Set Functions
    def setRectangleWidth(self, width):
        self.rectangle.setWidth(width)

    def setRectangleHeight(self, height):
        self.rectangle.setHeight(height)

    def updateRectangleDimension(self, width, height):
        self.rectangle.setWidth(width)
        self.rectangle.setHeight(height)

    def setLambda(self, lambda0):
        self.crowd.setLambda(lambda0)

    # Get Functions
    def getRectangle(self):
        return self.rectangle

    def getRectangleWidth(self):
        return self.rectangle.getWidth()

    def getRectangleHeight(self):
        return self.rectangle.getHeight()

    def getRectangleArea(self):
        return self.rectangle.getArea()

    def getPointsList(self):
        return self.crowd.getPointsList()

    def getRectList(self):
        return self.crowd.getRectList()

    def getNumberPoints(self):
        return self.crowd.getNbPoints()

    def getSpeedList(self):
        return self.crowd.getSpeedList()

    def getLambda(self):
        return self.crowd.getLambda()
