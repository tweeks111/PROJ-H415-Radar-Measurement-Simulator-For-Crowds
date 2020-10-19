

class Person:

    def __init__(self, *args):
        # Person(x, y)
        self.x = args[0]
        self.y = args[1]

        # Person(x, y, vx, vy)
        if len(args) == 4:
            self.vx = args[2]
            self.vy = args[3]
        else:
            self.vx = 0
            self.vy = 0

    # Get Functions

    def getPos(self):
        return [self.x, self.y]

    def getVelocity(self):
        return [self.vx, self.vy]

    # Set Functions

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def setVelocity(self, vel):
        self.vx = vel[0]
        self.vy = vel[1]
