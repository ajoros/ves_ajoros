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
                 dpi=150, hold=False, alpha=0.5, color=None, colors=None):

        # Save figure input parameters as class properties
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
        self.colors = colors
        self.color = colors[0]

        self.rectCoordinates = []
        self.mplRectangles = []

        # Initialize a figure, axis, and axes
        self.fig = Figure(dpi=self.dpi)
        self.ax = plt.gca()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(self.hold)

        # Initialize a FigureCanvas from the figure
        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.ax.figure.canvas)

        self.initFigure(self.xdata, self.ydata)

        # Allow the FigureCanvas to adjust with Main window using mpl Qt5 API
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Connect the mouse/trackpad to the FigureCanvas
        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        # Super from the class for Qt
        super(MplCanvas, self).__init__(self.fig)


    def initFigure(self, xdata, ydata):

        # if color is None:
        print('initFigure: color should be yellow')
        self.rect = Rectangle(
            (0, 0), 0, 0, alpha=self.alpha, color='yellow')

        plt.loglog(
            xdata, ydata, linestyle=self.linestyle, color=self.color)

        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()

        if self.mplRectangles:
            self.drawRectangles()

        self.fig = plt.gcf()


    def addPointsAndLine(self, xdata, ydata, color='#003366'):

        if len(xdata) != len(ydata):
            xdata = xdata[:len(ydata)]

        plt.loglog(
            xdata, ydata, linestyle='--', marker='o', color=color)

        self.ax.figure.canvas.draw()



    def updateFigure(self, rectangle, color='yellow', index=0, freeze=False):

        xy, width, height = rectangle
        self.rect = Rectangle(
            xy, width, height, alpha=self.alpha, color=color)

        if freeze:
            self.freezeRect = self.rect
            self.ax.add_patch(self.freezeRect)
        else:
            self.ax.add_path(self.rect)

        # if self.rectangles:
        #     # print(dir(self.ax))
        #     self.ax.clear()
        #     self.initFigure(self.xdata, self.ydata)
        #     self.drawRectangles()

        # if self.rectangles:
        #     self.drawRectangles()

        self.addPointsAndLine(self.xdata + 1, self.ydata + 1)

        self.ax.figure.canvas.draw()


    def onPress(self, event):

        self.x0 = event.xdata
        self.y0 = event.ydata

        # if self.mplRectangles:
        #     self.drawRectangles()


    def onRelease(self, event): # consider a decorator or something of the sort to drop in main.initPlot() as a function

        try:
            self.x1 = event.xdata
            self.y1 = event.ydata

            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))

            self.rectxy = (
                self.rect.get_xy(), self.rect._width, self.rect._height)

            # if self.mplRectangles:
            #     self.drawRectangles()

            self.ax.figure.canvas.draw()

            return self.rectxy

        except TypeError:
            pass


    def drawRectangles(self):
        # for i, rectangle in enumerate(self.rectangles):
        #     self.rectColor = self.colors[i * 4]
        #     self.updateFigure(
        #         rectangle, self.rectColor, index=i, freeze=True)
        # self.rectColor = self.colors[(i + 1) * 4]
        for i, rectangle in enumerate(self.rectCoordinates):
            color = self.colors[i * 4]
            xy, width, height = rectangle

            rect = Rectangle(
                xy, width, height, alpha=self.alpha, color=color)

            self.ax.add_patch(rect)

        # self.ax.figure.cavas.draw()


if __name__ == '__main__':
    from aggregate import aggregateTable
    from templates.tempData import (
        columns, colors, headers, rowCount, tableData)

    voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
        tableData, len(tableData))

    canvas = MplCanvas(
        voltageSpacing, meanVoltage, parent=None,
        xlabel='Voltage Probe Spacing (m)',
        ylabel='Resistivity (Ohm-m)',
        colors=colors)
    plt.loglog(voltageSpacing, meanCurrent)
    plt.show()

