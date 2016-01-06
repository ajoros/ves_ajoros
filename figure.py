import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
plt.style.use('bmh')
from PyQt5.QtWidgets import QSizePolicy

import numpy as np


class MplCanvas(FigureCanvas):

    def __init__(self, xdata, ydata, parent=None, title='',
                 xlabel='x label', ylabel='y label', linestyle='--',
                 dpi=150, hold=False, alpha=0.5, color=None):

        self.xdata = xdata
        self.ydata = ydata
        self.parent = parent
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.linestyle = linestyle
        self.dpi = dpi
        self.hold = hold
        self.alpha = alpha
        self.color = color

        self.fig = Figure(dpi=self.dpi)
        self.ax = plt.gca()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(self.hold)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.ax.figure.canvas)

        self.initFigure(self.xdata, self.ydata)

        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        super(MplCanvas, self).__init__(self.fig)


    def initFigure(self, xdata, ydata):

        self.rect = Rectangle(
            (0, 0), 0, 0, alpha=self.alpha, color=self.color)

        plt.loglog(
            xdata, ydata, linestyle=self.linestyle, color=self.color)

        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()

        self.fig = plt.gcf()



    def updateFigure(self, rectangle):

        xy, width, height = rectangle

        self.rect = Rectangle(
            xy, width, height, alpha=self.alpha, color=self.color)

        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()


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
            self.rect.figure.canvas.draw()

            self.rectangle = (
                self.rect.get_xy(), self.rect._width, self.rect._height)

            self.ax.figure.canvas.draw()

            return self.rectangle

        except TypeError:
            pass
