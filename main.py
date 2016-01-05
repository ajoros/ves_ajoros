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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure, Axes
import matplotlib.pyplot as plt
plt.style.use('bmh')
from matplotlib.patches import Rectangle
import numpy as np

# from DraggableRectangles import DraggableRectangle
from aggregate import voltageSpacing, meanVoltage, meanCurrent
# from aggregate import aggregateTable


os.chdir(os.path.join(os.path.dirname(__file__), 'ves'))
UI_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


class Main(QMainWindow, UI_MainWindow):

    def __init__(self, tableData, headers, colors,
                 xy, width, height, angle=0., alpha=0.5, color='red'):

        super(Main, self).__init__()

        self.setupUi(self)

        # Set up the model and tableView
        self.model = PalettedTableModel(tableData, headers, colors)

        self.tableViewWidget.setModel(self.model)
        for row in range(0, rowCount, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()
        self.tableViewWidget.show()

        # self.fig = Figure()
        figureViewWidget = MplCanvas(
            voltageSpacing, meanVoltage, parent=None, title='hey',
            xlabel='Spacing', ylabel='Other thing')
        self.canvas = figureViewWidget

        # self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)
        # self.ax = plt.gca()

        self.toolbar = NavigationToolbar(
            self.canvas, self.canvas, coordinates=True)

        self.mplvl.addWidget(self.canvas)
        self.mplvl.addWidget(self.toolbar)

        self.canvas.mpl_connect(
            'button_press_event', self.canvas.onPress)
        self.canvas.mpl_connect(
            'button_release_event', self.canvas.onRelease)


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


    def initTableView(self, model):

        self.tableViewWidget.setModel(model)

        for row in range(0, rowCount, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()

        self.tableViewWidget.show()



    # def addmpl(self, fig, color=None, alpha=0.5):

    #     if color is None:
    #         color = 'red'

    #     self.x0 = None
    #     self.y0 = None
    #     self.x1 = None
    #     self.y1 = None

    #     self.fig = Figure()
    #     self.canvas = Canvas(self.fig)
    #     self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

    #     # print(dir(self.fig))
    #     # self.axes = self.fig.add_subplot(111)
    #     self.ax = plt.gca()

    #     self.canvas = Canvas(fig.figure)
    #     self.mplvl.addWidget(self.canvas)

    #     self.toolbar = NavigationToolbar(
    #         self.canvas, self.figureViewWidget, coordinates=True)
    #     self.mplvl.addWidget(self.toolbar)

    #     self.canvas.mpl_connect(
    #         'button_press_event', self.canvas.onPress)
    #     self.canvas.mpl_connect(
    #         'button_release_event', self.canvas.onRelease)

    #     self.canvas.draw()


    # def onPress(self, event):
    #     print('main press')

    #     self.x0 = event.xdata
    #     self.y0 = event.ydata


    # def onRelease(self, event):
    #     print('main release')
    #     try:
    #         self.x1 = event.xdata
    #         self.y1 = event.ydata

    #         self.rect.set_width(self.x1 - self.x0)
    #         self.rect.set_height(self.y1 - self.y0)
    #         self.rect.set_xy((self.x0, self.y0))

    #         # self.ax.figure.canvas.draw()
    #         self.canvas.draw()

    #         self.rectangle = (
    #             self.rect.get_xy(), self.rect._width,
    #             self.rect._height, self.rect._angle)

    #         return self.rectangle

    #     except TypeError:
    #         pass




class MplCanvas(FigureCanvas):

    def __init__(self, x, y, parent=None, title='',
                 xlabel='x label', ylabel='y label', linestyle='--',
                 dpi=150, hold=False, alpha=0.5, color=None):
        try:
            import matplotlib.pyplot as plt
            plt.style.use('bmh')
        except:
            pass

        self.xdata = x
        self.ydata = y
        self.parent = parent
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.linestyle = linestyle
        self.dpi = dpi
        self.hold = hold
        self.alpha = alpha
        self.color = color

        fig = Figure(dpi=self.dpi)
        super(MplCanvas, self).__init__(fig)

        self.axes = fig.add_subplot(111)
        self.axes.hold(self.hold)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.initFigure()

        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        self.draw()


    def initFigure(self):

        self.rect = Rectangle(
            (0, 0), 100, 100, alpha=self.alpha, color=self.color)
        self.axes.plot(
            self.xdata, self.ydata, linestyle=self.linestyle, color=self.color)
        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.add_patch(self.rect)
        self.draw()
        # self.axes.set_tight_layout()
        # self.draw()


    def updateFigure(self, rectangle):

        xy, width, height = rectangle
        self.axes.plot(
            self.xdata, self.ydata, linestyle=self.linestyle, color=self.color)
        self.rect = Rectangle(
            xy, width, height, alpha=self.alpha, color=self.color)
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()
        self.draw()
        Canvas.draw(self)


    def onPress(self, event):
        print('MplCanvas press')
        self.x0 = event.xdata
        self.y0 = event.ydata
        print('x0: {}'.format(self.x0))
        print('y0: {}'.format(self.y0))



    def onRelease(self, event):
        print('MplCanvas release')
        try:
            self.x1 = event.xdata
            self.y1 = event.ydata

            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            print('x1 {}'.format(self.x1))
            print('y1 {}'.format(self.y1))
            self.rect.figure.canvas.draw()

            self.ax.figure.canvas.draw()
            self.draw()
            # for thing in dir(self.canvas):
            #     print(thing)
            # self.canvas.draw()

            self.rectangle = (
                self.rect.get_xy(), self.rect._width, self.rect._height)

            self.updateFigure(self.rectangle)
            print(self.rectangle)
            return self.rectangle

        except TypeError as e:
            print(e)
            pass



# class MatplotlibFigure(Canvas, Figure):

#     def __init__(self, parent=None, title='', xlabel='x label',
#                  ylabel='y label', dpi=150, hold=False, alpha=0.5, color=None):

#         super(MatplotlibFigure, self).__init__(Figure())

#         if color is None:
#             color = 'red'

#         self.setParent = parent
#         self.figure = Figure(dpi=dpi)
#         self.canvas = Canvas(self.figure)
#         self.mplPlot = self.figure.add_subplot(111)

#         self.mplPlot.set_title(title)
#         self.mplPlot.set_xlabel(xlabel)
#         self.mplPlot.set_ylabel(ylabel)

#         self.rect = Rectangle((0, 0), 1, 1, alpha=alpha, color=color)

#         self.ax = plt.gca()
#         self.ax.add_patch(self.rect)
#         self.ax.figure.canvas.mpl_connect(
#             'button_press_event', self.onPress)
#         self.ax.figure.canvas.mpl_connect(
#             'button_release_event', self.onRelease)


#     def plotData(self, x, y):

#         self.mplPlot.plot(x, y)
#         self.draw()


#     def onPress(self, event):
#         print('MatplotlibFigure press')
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
#             print(self.rectangle)
#             return self.rectangle

#         except TypeError:
#             pass
# # class Plot(Figure, Axes):

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
               (0, 0.5), 50, 50, angle=0.)
    # for thing in sorted(dir(plotWidget)):
    #     print('the thing: {}'.format(thing))
    # main.addmpl(plotWidget)
# plotWidget, tableData, headers, colors,
#                  xy, width, height, angle=0.
    # main.addmpl()
    main.show()

    sys.exit(app.exec_())
