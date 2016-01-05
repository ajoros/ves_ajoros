import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure, Axes
import matplotlib.pyplot as plt
plt.style.use('bmh')
from matplotlib.patches import Rectangle
import numpy as np

# from DraggableRectangles import DraggableRectangle
from aggregate import voltageSpacing, meanVoltage, meanCurrent


# r = Rectangle((0, 0), 1, 1, alpha=0.5, color='red')
# # print(dir(Figure))
# fig = plt.subplot(111)
# # print(dir(fig))
class Plot(Figure, Axes):

    def __init__(self, xy, width, height,
                 xlabel='Voltage Spacing (m)',
                 ylabel='Apperent Resistivity (ohm-m)',
                 angle=0., alpha=0.5, color=None):

        if color is None:
            color = 'red'

        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        self.fig = Figure()
        self.canvas = Canvas(self.fig)

        # print(dir(self.fig))
        # self.axes = self.fig.add_subplot(111)
        self.ax = plt.gca()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        # Canylvas.__init__(self, self.fig)
        # Canvas.setSizePolicy(self, )

        # self.fig = fig
        # self.ax = plt.gca()
        self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        super(Plot, self).__init__()


    def onPress(self, event):

        self.x0 = event.xdata
        self.y0 = event.ydata


    def onRelease(self, event):

        try:
            self.x1 = event.xdata
            self.y1 = event.ydata

            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))

            self.ax.figure.canvas.draw()

            self.rectangle = (
                self.rect.get_xy(), self.rect._width,
                self.rect._height, self.rect._angle)

            return self.rectangle

        except TypeError:
            pass


if __name__ == '__main__':
    np.random.seed(232)
    x = range(0, 10)
    y = np.random.randn(10)

    a_list = []
    for _ in range(1):
        a = Plot((0, 0.5), 0.25, 0.25)
        # plt.style.use('bmh')
        plt.plot(voltageSpacing, meanVoltage, '--')
        plt.plot(voltageSpacing, meanCurrent, '--')
        plt.show()
        a_list.append(a)
        # print(a.rectangle)
        del a

    for a in a_list:
        print(a.x0)
