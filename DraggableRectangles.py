import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas


class DraggableRectangle(Canvas):

    def __init__(self, xy=None, width=None, height=None,
                 alpha=None, color=None):

        super(DraggableRectangle, self).__init__()

        self.ax = plt.gca()
        self.rect = Rectangle(xy, width, height, alpha=alpha, color=color)

        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        self.ax.add_patch(self.rect)
        self.press = None
        self.dblclick = False


    def connect(self):

        'connect to all the events we need'

        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)


    def on_press(self, event):

        'on button press we will see if the mouse is over us and store some data'

        if event.dblclick:
            self.dblclick = True
            contains, attrd = self.rect.contains(event)

            if not contains:
                return

            x0, y0 = event.xdata, event.ydata
            self.press = x0, y0, event.xdata, event.ydata

        else:
            self.x0 = event.xdata
            self.y0 = event.ydata


    def on_motion(self, event):

        'on motion we will move the rect if the mouse is over us'

        if self.press is None:
            return

        if event.inaxes != self.rect.axes:
            return

        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        self.rect.set_x(x0 + dx)
        self.rect.set_y(y0 + dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):

        # if self.dblclick:
        #     x0 = event.x
        #     y0 = event.y
        #     x1 = event.xdata
        #     y1 = event.ydata
        #     self.rect.set_width(x1 - x0)
        #     self.rect.set_height(y1 - y0)
        #     self.rect.set_xy((x0, y0))
        #     self.ax.figure.canvas.draw()
        #     self.dblclick = False
        #     return

        # else:
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()
        return


    def disconnect(self):

        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = [0, 1]
    y = [1, 1]
    rects = [1]
    drs = []

    dr = DraggableRectangle((0, 0), 1, 1, 0.5, 'red')
    dr.connect()

    plt.show()
