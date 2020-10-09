from Model.rectangle import Rectangle
from Model.crowd import Crowd
import time

class Model:

    # Constructor
    def __init__(self):
        self.rectangle = Rectangle((Rectangle.MAX_RECTANGLE - Rectangle.MIN_RECTANGLE) / 2 + Rectangle.MIN_RECTANGLE,
                                   (Rectangle.MAX_RECTANGLE - Rectangle.MIN_RECTANGLE) / 2 + Rectangle.MIN_RECTANGLE)

        self.crowd = Crowd(self.rectangle)

    # Class Functions
    def initCrowd(self):
        self.crowd.initPoints()

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

    def getSpeedList(self):
        return self.crowd.getSpeedList()

    def getLambda(self):
        return self.crowd.getLambda()