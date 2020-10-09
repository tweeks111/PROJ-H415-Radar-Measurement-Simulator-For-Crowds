from view import View
from Model.model import Model
import time

class Controller:
    # Constructor
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.configLeftPanel()
        self.initUI()

        self.is_running = False

    def run(self):
        self.view.title("Crowd Simulation")
        self.view.mainloop()

    # View Configuration
    def configLeftPanel(self):
        # Sliders
        self.view.left_side_panel.height_slider.configure(command=self.changeRectangleHeight, from_=self.model.rectangle.MIN_RECTANGLE, to=self.model.rectangle.MAX_RECTANGLE)
        self.view.left_side_panel.height_slider.set(self.model.getRectangleHeight())
        self.view.left_side_panel.width_slider.configure(command=self.changeRectangleWidth, from_=self.model.rectangle.MIN_RECTANGLE, to=self.model.rectangle.MAX_RECTANGLE)
        self.view.left_side_panel.width_slider.set(self.model.getRectangleWidth())
        self.view.left_side_panel.lambda_slider.configure(command=self.changeLambda, from_=0.1, to=1.0, resolution=0.1)
        self.view.left_side_panel.lambda_slider.set(self.model.getLambda())

        # Button
        self.view.left_side_panel.start_btn.configure(command=self.startSimulation)

    def initUI(self):
        self.view.canvas.computePixelRatio(self.model.rectangle.MAX_RECTANGLE)
        self.view.canvas.updateRectangleDimension(self.model.getRectangleWidth(), self.model.getRectangleHeight())

    # MVC Interaction
    def changeRectangleHeight(self, height):
        rectangleWidth = self.model.getRectangleWidth()
        self.model.setRectangleHeight(int(height))
        self.view.canvas.updateRectangleDimension(rectangleWidth, int(height))

    def changeRectangleWidth(self, width):
        rectangleHeight = self.model.getRectangleHeight()
        self.model.setRectangleWidth(int(width))
        self.view.canvas.updateRectangleDimension(int(width), rectangleHeight)

    def changeLambda(self, lambda0):
        self.model.setLambda(float(lambda0))

    def startSimulation(self):
        self.is_running = True
        self.view.left_side_panel.blockSliders(self.is_running)
        self.view.left_side_panel.start_btn.configure(command=self.stopSimulation)

        self.model.initCrowd()

        delta_time = 0
        while self.is_running:
            start_time = time.time()
            self.model.run(delta_time)
            points_list = self.model.getPointsList()
            self.view.canvas.drawPoints(points_list)
            delta_time = time.time()-start_time

    def stopSimulation(self):
        self.is_running = False
        self.view.left_side_panel.blockSliders(self.is_running)
        self.view.left_side_panel.start_btn.configure(command=self.startSimulation)
        self.view.canvas.erasePoints()
