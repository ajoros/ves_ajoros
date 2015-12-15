import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt


class DraggableRectangle:
    def __init__(self, xy, width, height, alpha, color):
        # print(rect)
        self.ax = plt.gca()
        # self.rect = rect
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
        # if event.inaxes != self.rect.axes:
        #     return
        if event.dblclick:
            self.dblclick = True
            print('DOUBLE CLICK\n')
            contains, attrd = self.rect.contains(event)
            if not contains:
                return

            print('event contains', self.rect.xy)
            # x0, y0 = self.rect.xy
            x0, y0 = event.xdata, event.ydata
            self.press = x0, y0, event.xdata, event.ydata
        else:
            print('NO DOUBLE CLICK\n')

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return

        if event.inaxes != self.rect.axes:
            return

        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        # print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' % (
        #     x0, xpress, event.xdata, dx, x0+dx))
        self.rect.set_x(x0 + dx)
        self.rect.set_y(y0 + dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        if self.dblclick:
            print('Double on release')
            self.dblclick = False
        return
        # print('DOUBLE CLICK\n\n')
        # print('release event:')
        # print(event)
        # # 'on release we reset the press data'
        # # self.press = None
        # x0 = event.x0
        # y0 = event.y0
        # # self.rect.figure.canvas.draw()
        # print('release')
        # x1 = event.xdata
        # y1 = event.ydata
        # self.rect.set_width(x1 - x0)
        # self.rect.set_height(y1 - y0)
        # self.rect.set_xy((x0, y0))
        # self.ax.figure.canvas.draw()
        # print('x1 {}'.format(x1))
        # print('y1 {}'.format(y1))

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
    # rects = ax.bar(x, y, width=0.9)
    # print(range(2), map(lambda x: x * 2, range(2)))
    drs = []
    # for rect in rects:
    # self, xy, width, height, alpha, color
    # print(len([(0,1), 1, 1, 0.5, 'red']))
    dr = DraggableRectangle((0, 0), 1, 1, 0.5, 'red')
    dr.connect()
    # drs.append(dr)

    plt.show()
