import os
import sys

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
plt.style.use('bmh')
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as Canvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QSizePolicy, QTableView
from PyQt5.uic import loadUiType

from aggregate import voltageSpacing, meanVoltage, meanCurrent
from interactivePlot import Plot
from table import PalettedTableModel
from templates.tempData import (
    columnCount, columns, colors, headers, rowCount, tableData)

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



os.chdir(os.path.join(os.path.dirname(__file__), 'ves'))
UI_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


class Main(QMainWindow, UI_MainWindow):

    def __init__(self, tableData, headers, colors,
                 xy, width, height, angle=0., alpha=0.5, color='red'):

        super(Main, self).__init__()

        self.setupUi(self)

        # self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

        # Set up the model and tableView
        self.model = PalettedTableModel(tableData, headers, colors)

        self.tableViewWidget.setModel(self.model)
        for row in range(0, rowCount, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()
        self.tableViewWidget.show()

        self.fig = Figure()
        figureViewWidget = MplCanvas(
            voltageSpacing, meanVoltage, parent=None, title='hey',
            xlabel='Spacing', ylabel='Other thing')
        self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)
        self.ax = plt.gca()

        self.canvas = figureViewWidget
        self.mplvl.addWidget(figureViewWidget)

        self.toolbar = NavigationToolbar(
            self.canvas, self.figureViewWidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

        self.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        self.canvas.draw()

        # self.

        # for thing in (dir(self.figureViewWidget)):
        #     print(thing)
        # self.figureViewWidget = plotWidget

        # self.figureViewWidget.setParent(self.figureViewWidget)
        # self.mplvl.addWidget(self.figureViewWidget)
        # self.figureViewWidget.canvas.draw()

        # self.figureViewWidget.show()

        # self.initUi()



    def initUi(self):

        saveAction = QAction(QIcon('save.png'), '&Save As', self)
        saveAction.setShortcut('Ctrl+S')

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Alt+F4')

        saveAction.triggered.connect(QApplication.saveStateRequest)
        exitAction.triggered.connect(QApplication.quit)
        # for thing in dir(self):
        #     print('thing: {}'.format(thing))
        # input()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        addRowButton = QPushButton()
        addRowButton.clicked.connect(PalettedTableModel.insertRows(0, 1))

        self.show()


    def addmpl(self, fig, color=None, alpha=0.5):

        if color is None:
            color = 'red'

        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        self.fig = Figure()
        self.canvas = Canvas(self.fig)
        self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

        # print(dir(self.fig))
        # self.axes = self.fig.add_subplot(111)
        self.ax = plt.gca()

        self.canvas = Canvas(fig.figure)
        self.mplvl.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(
            self.canvas, self.figureViewWidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

        self.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        self.canvas.draw()


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


    def initTableView(self, model):

        self.tableViewWidget.setModel(model)

        for row in range(0, rowCount, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()

        self.tableViewWidget.show()


class MplCanvas(Canvas):

    def __init__(self, x, y, parent=None, title='',
                 xlabel='x label', ylabel='y label',
                 dpi=150, hold=False, alpha=0.5, color=None):


        fig = Figure(dpi=dpi)
        super(MplCanvas, self).__init__(fig)

        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        self.initFigure(x, y, '--', color=color)

        Canvas.__init__(self, fig)
        self.setParent(parent)

        Canvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


    def initFigure(self, x, y, linestyle='--', color=None):

        self.axes.plot(x, y, linestyle=linestyle, color=color)
        self.draw()

    def addmpl(self, fig, color=None):

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

        self.canvas = Canvas(fig.figure)
        self.mplvl.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(
            self.canvas, self.figureViewWidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

        self.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        self.canvas.draw()


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



class MatplotlibFigure(Canvas, Figure):

    def __init__(self, parent=None, title='', xlabel='x label',
                 ylabel='y label', dpi=150, hold=False, alpha=0.5, color=None):

        super(MatplotlibFigure, self).__init__(Figure())

        if color is None:
            color = 'red'

        self.setParent = parent
        self.figure = Figure(dpi=dpi)
        self.canvas = Canvas(self.figure)
        self.mplPlot = self.figure.add_subplot(111)

        self.mplPlot.set_title(title)
        self.mplPlot.set_xlabel(xlabel)
        self.mplPlot.set_ylabel(ylabel)

        self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

        self.ax = plt.gca()
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)


    def plotData(self, x, y):

        self.mplPlot.plot(x, y)
        self.draw()


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
# class Plot(Figure, Axes):

#     def __init__(self, xy, width, height, xlabel=None, ylabel=None,
#                  angle=0., alpha=0.5, color=None):

#         super(Plot, self).__init__()

#         if color is None:
#             color = 'red'

#         self.x0 = None
#         self.y0 = None
#         self.x1 = None
#         self.y1 = None

#         self.fig = Figure()
#         self.canvas = Canvas(self.fig)
#         # print(dir(self.fig))
#         # self.axes = self.fig.add_subplot(111)
#         self.ax = plt.gca()
#         # self.ax.add_xlabel(xlabel)
#         # self.ax.add_ylabel(ylabel)

#         # Canvas.__init__(self, self.fig)
#         # Canvas.setSizePolicy(self, )

#         # self.fig = fig
#         # self.ax = plt.gca()
#         self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

#         self.ax.add_patch(self.rect)
#         self.ax.figure.canvas.mpl_connect(
#             'button_press_event', self.onPress)
#         self.ax.figure.canvas.mpl_connect(
#             'button_release_event', self.onRelease)


#     def onPress(self, event):

#         self.x0 = event.xdata
#         self.y0 = event.ydata


#     def onRelease(self, event):

#         try:
#             self.x1 = event.xdata
#             self.y1 = event.ydata

#             self.rect.set_width(self.x1 - self.x0)
#             self.rect.set_height(self.y1 - self.y0)
#             self.rect.set_xy((self.x0, self.y0))

#             self.ax.figure.canvas.draw()

#             self.rectangle = (
#                 self.rect.get_xy(), self.rect._width,
#                 self.rect._height, self.rect._angle)

#             return self.rectangle

#         except TypeError:
#             pass


if __name__ == '__main__':
    # plt.plot(voltageSpacing, meanVoltage, '-.')
    # plt.plot(voltageSpacing, meanCurrent, '-.')
    # Plot((0, 0.5), 0.25, 0.25)
    # plt.show()

    # fig = plt.gcf()
    # axes = fig.add_subplot(111)
    # axes.xlabel('Woot')
    # axes.ylabel('Soot')

    app = QApplication(sys.argv)
    # plotWidget = MatplotlibFigure(
    #     parent=None, title='', xlabel='x label', ylabel='y label',
    #     dpi=150, hold=False)
    # plotWidget.plotData(voltageSpacing, meanVoltage)
    # plt.show()

    # plotWidget = MplCanvas(
    #     voltageSpacing, meanVoltage, parent=None, title='hey', xlabel='Spacing',
    #     ylabel='Other thing')
    main = Main(tableData, headers, colors,
               (0, 0.5), 0.25, 0.25, angle=0.)
    # for thing in sorted(dir(plotWidget)):
    #     print('the thing: {}'.format(thing))
    # main.addmpl(plotWidget)
# plotWidget, tableData, headers, colors,
#                  xy, width, height, angle=0.
    # main.addmpl()
    main.show()

    sys.exit(app.exec_())
