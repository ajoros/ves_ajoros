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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QTableView
from PyQt5.uic import loadUiType

from aggregate import voltageSpacing, meanVoltage, meanCurrent
from interactivePlot import Plot
from table import PalettedTableModel
from templates.tempData import (
    columnCount, columns, colors, headers, rowCount, tableData)


os.chdir(os.path.join(os.path.dirname(__file__), 'ves'))
UI_MainWindow, QMainWindow = loadUiType('mainwindow.ui')


class Main(QMainWindow, UI_MainWindow):

    def __init__(self, tableData, headers, colors,
                 xy, width, height, angle=0.):

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



    def initUi(self):

        saveAction = QAction(QIcon('save.png'), '&Save As', self)
        saveAction.setShortcut('Ctrl+S')

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Alt+F4')

        saveAction.triggered.connect(QApplication.saveStateRequest)
        exitAction.triggered.connect(QApplication.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        self.show()


    def addmpl(self, fig):

        self.canvas = Canvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(
            self.canvas, self.FigureWidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)


    def initTableView(self, model):

        self.tableViewWidget.setModel(model)

        for row in range(0, rowCount, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()

        self.tableViewWidget.show()


if __name__ == '__main__':
    width = 8
    height = 5
    dpi = 300

    fig = plt.subplot(111)
    # figure = Plot(
    #     (0, 0), 1, 1, alpha=0.5, color='red')
    # # ax = figure.add_subplot(111)
    # figure.add_subplot(111)
    # print(dir(figure))
    # print(dir(Figure))

    # a = Plot((0, 0.5), 0.25, 0.25)
    plt.style.use('bmh')
    # plt.plot(voltageSpacing, meanVoltage, '--')
    # plt.plot(voltageSpacing, meanCurrent, '--')

    # figure = Figure(figsize=(width, height), dpi=dpi)
    # ax1fig1 = figure.add_subplot(111)
    # ax1fig1.plot(voltageSpacing, meanVoltage, '--')
    # ax1fig1.plot(voltageSpacing, meanCurrent, '--')
    # figure.add_subplot(voltageSpacing, meanVoltage, '--')
    # figure.add_subplot(voltageSpacing, meanCurrent, '--')
    # plt.tight_layout()

    app = QApplication(sys.argv)
    main = Main(tableData, headers, colors, (0, 0.5), 0.25, 0.25)

    # print(dir(self.tableViewWidget))
    # model = PalettedTableModel(tableData, headers, colors)
    # main.initTableView(model)
    # main.addmpl(fig)
    main.show()

    sys.exit(app.exec_())
