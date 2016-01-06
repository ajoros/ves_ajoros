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
from figure import MplCanvas
from table import PalettedTableModel
from templates.tempData import (
    columns, colors, headers, rowCount, tableData)

import numpy as np


os.chdir(os.path.join(os.path.dirname(__file__), 'templates'))
UI_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


class Main(QMainWindow, UI_MainWindow):

    def __init__(self, tableData, headers, colors,
                 xy, width, height, angle=0., alpha=0.5, color='red'):

        super(Main, self).__init__()

        self.setupUi(self)

        # Set up the model and tableView
        self.model = PalettedTableModel(tableData, headers, colors)

        self.initTableView(self.model)

        self.tableViewWidget.resizeColumnsToContents()
        self.tableViewWidget.show()

        # Set up the QWidget with a MplCanvas and NavigationToolbar instance
        self.canvas = MplCanvas(
            voltageSpacing, meanVoltage, parent=None, title='hey',
            xlabel='Spacing', ylabel='Other thing')
        plt.plot(voltageSpacing, meanCurrent)

        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(
            self.canvas, self.canvas, coordinates=True)

        self.mplvl.addWidget(self.canvas)
        self.mplvl.addWidget(self.toolbar)

        # Connect to the canvas to handle mouse clicks
        self.canvas.mpl_connect(
            'button_press_event', self.canvas.onPress)
        self.canvas.mpl_connect(
            'button_release_event', self.canvas.onRelease)

        # Connect to table buttons
        self.addRowButton.clicked.connect(self.addRow)
        self.removeRowButton.clicked.connect(self.removeRow)
        self.plotButton.clicked.connect(self.plot)

        # Connect to spacing radio buttons
        self.wennerRadioButton.toggled.connect(self.wenner)
        self.schlumbergerRadioButton.toggled.connect(self.schlumberger)

        # Connect to plot buttons
        self.newRectangleButton.clicked.connect(self.newRectangle)
        self.computeButton.clicked.connect(self.compute)

        # self.initUi()


    def initUi(self):

        saveAction = QAction(QIcon('save.png'), '&Save As', self)
        saveAction.setShortcut('Ctrl+S')

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Alt+F4')

        saveAction.triggered.connect(QApplication.saveStateRequest)
        exitAction.triggered.connect(QApplication.quit)

        # fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        addRowButton = QPushButton()
        addRowButton.clicked.connect(PalettedTableModel.insertRows(0, 1))

        # self.show()


    def initTableView(self, model):

        self.tableViewWidget.setModel(model)

        for row in range(0, rowCount, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()

        self.tableViewWidget.show()


    def addRow(self):

        print('add row')


    def removeRow(self):

        print('remove row')


    def plot(self):

        print('plot')


    def newRectangle(self):

        print('new rectangle')


    def compute(self):

        print('compute')


    def wenner(self):

        print('wenner')


    def schlumberger(self):

        print('schlumberger')





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main = Main(tableData, headers, colors, (0, 0.5), 50, 50, angle=0.)
    main.show()

    sys.exit(app.exec_())
