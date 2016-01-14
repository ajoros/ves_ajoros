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


class InteractiveCanvas(FigureCanvas):

    def __init__(self, xdata, ydata, parent=None,
                 xlabel='x label', ylabel='y label',
                 linestyle='--', marker='o',
                 dpi=150, hold=False, alpha=0.5, colors=None):

        # Save figure input parameters as class properties
        self.xdata = xdata
        self.ydata = ydata
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.linestyle = linestyle
        self.marker = marker
        self.dpi = dpi
        self.hold = hold
        self.alpha = alpha
        self.colors = colors

        # Initialize empty list to store mpl rectangles and their coordinates
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
        super(InteractiveCanvas, self).__init__(self.fig)


    def initFigure(self, xdata, ydata):

        if xdata is None or ydata is None:
            return

        # Currently ydata is longer than xdata with schlumberger, so handle
        #   that if it makes it this far into the program
        if len(xdata) != len(ydata):
            if len(ydata) > len(xdata):
                xdata = xdata[:len(ydata)]
            else:
                ydata = ydata[:len(xdata)]

        # Set up an empty rectangle for drawing and plot the x/y data
        self.rect = Rectangle(
            (0, 0), 0, 0, alpha=self.alpha, color='grey')
        self.addPointsAndLine(xdata, ydata, draw=False)

        # Create an mpl axis and set the labels, add the rectangle
        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()

        # Draw extant rectangles if applicable
        if self.mplRectangles:
            self.drawRectangles()

        # Update the figure object/property
        self.fig = plt.gcf()

        self.fig.tight_layout()

    def drawRectangles(self):

        # Iterate through the mpl Rectangles to draw them with the proper color
        for i, rectangle in enumerate(self.rectCoordinates):

            color = self.colors[i * 4]
            xy, width, height = rectangle

            rect = Rectangle(
                xy, width, height, alpha=self.alpha, color=color)

            self.ax.add_patch(rect)


    def addPointsAndLine(self, xdata, ydata, color='#003366', draw=True):

        # Currently ydata is longer than xdata with schlumberger, so handle
        #   that if it makes it this far into the program
        if len(xdata) != len(ydata):
            xdata = xdata[:len(ydata)]

        # log/log plot of x and y data
        plt.loglog(
            xdata, ydata, linestyle=self.linestyle,
            marker=self.marker, color=color)

        # Draw the updates
        if draw:
            self.fig.tight_layout()
            self.ax.figure.canvas.draw()


    def onPress(self, event):

        self.x0 = event.xdata
        self.y0 = event.ydata


    def onRelease(self, event):

        try:
            self.x1 = event.xdata
            self.y1 = event.ydata

            # Create a rectangle on the plot
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))

            self.ax.figure.canvas.draw()

            # Store and return the rectangle attributes as a tuple
            self.rectxy = (
                self.rect.get_xy(), self.rect._width, self.rect._height)

            return self.rectxy

        except TypeError:
            pass
