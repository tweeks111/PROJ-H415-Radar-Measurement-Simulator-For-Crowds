
class Rectangle:
    MIN_RECTANGLE = 10
    MAX_RECTANGLE = 40

    # Constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # Set Functions
    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height

    def setDimension(self, width, height):
        self.width = width
        self.height = height

    # Get Functions
    def getArea(self):
        return self.width*self.height

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
