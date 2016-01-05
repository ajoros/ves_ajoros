import os

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
plt.style.use('bmh')
from matplotlib.figure import Figure
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QSizePolicy
from PyQt5.uic import loadUiType

from aggregate import voltageSpacing, meanVoltage, meanCurrent
from table import PalettedTableModel
from templates.tempData import (
    columns, colors, headers, rowCount, tableData)

import numpy as np


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

        self.canvas = MplCanvas(
            voltageSpacing, meanVoltage, parent=None, title='hey',
            xlabel='Spacing', ylabel='Other thing')
        self.canvas.setParent(self)

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

        self.initFigure()

        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        super(MplCanvas, self).__init__(self.fig)


    def initFigure(self):

        self.rect = Rectangle(
            (0, 0), 0, 0, alpha=self.alpha, color=self.color)
        plt.plot(
            self.xdata, self.ydata, linestyle=self.linestyle, color=self.color)
        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.add_patch(self.rect)
        self.fig = plt.gcf()
        self.ax.figure.canvas.draw()


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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main = Main(tableData, headers, colors, (0, 0.5), 50, 50, angle=0.)
    main.show()

    sys.exit(app.exec_())
