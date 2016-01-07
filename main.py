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
from PyQt5.QtWidgets import QAction, QApplication, QMessageBox, QSizePolicy
from PyQt5.uic import loadUiType

from aggregate import aggregateTable
from equations import schlumbergerResistivity, wennerResistivity
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

        # Set up the propoerties dictating probe layout
        self.schlumbergerLayout = False
        self.wennerLayout = False
        self.colors = colors

        # Set up the model and tableView
        self.model = PalettedTableModel(tableData, headers, colors)

        self.initTableView(self.model)

        self.tableViewWidget.resizeColumnsToContents()
        self.tableViewWidget.show()

        self.aggregateTableForPlot()

        # Set up the QWidget with a MplCanvas and NavigationToolbar instance
        self.rectangles = []
        self.rects = []
        self.canvas = MplCanvas(
            self.voltageSpacing, self.meanVoltage, parent=None,
            title='hey', xlabel='Voltage Probe Spacing (m)',
            ylabel='Resistivity (Ohm-m)', colors=self.colors)
        plt.plot(self.voltageSpacing, self.meanCurrent)

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

        nRows = len(self.model.table)

        self.tableViewWidget.setModel(model)

        for row in range(0, nRows, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()

        self.tableViewWidget.show()


    def aggregateTableForPlot(self):

        voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
            self.model.table, len(self.model.table))

        self.voltageSpacing = voltageSpacing
        self.meanVoltage = meanVoltage
        self.meanCurrent = meanCurrent

        # if self.schlumbergerLayout == True:

        #     self.apparentResistivity = schlumbergerResistivity(
        #         1., 1., 1., 1.)

        # if self.wennerLayout == True:

        #     self.apparentResistivity = wennerResistivity(
        #         1., 1., 1.)


    def addRow(self):

        startRow = len(self.model.table)

        self.model.insertRows(startRow, 4)
        self.initTableView(self.model)


    def removeRow(self):

        startRow = len(self.model.table) - 4

        self.model.removeRows(startRow, 4)
        self.initTableView(self.model)


    def initPlot(self):

        plt.clf()
        self.aggregateTableForPlot()

        self.canvas.initFigure(self.voltageSpacing, self.meanVoltage)
        plt.plot(self.voltageSpacing, self.meanCurrent)

        self.canvas.draw()



    def plot(self):

        self.initPlot()

        self.rectangles = []


    def newRectangle(self):

        # print(self.canvas.rectangle)
        try:
            self.rectangles.append(self.canvas.rectangle)
            self.initPlot()
            print(self.rectangles)
            for i, rectangle in enumerate(self.rectangles):
                color = self.colors[i  * 4]
                print('color {}; rectangle {}'.format(color, rectangle))
                self.canvas.updateFigure(rectangle, color, freeze=True)
                self.canvas.draw()
        except AttributeError:
            pass


    def compute(self):

        self.apparentResistivity = None
        self.aggregateTableForPlot()

        # Calculate apparent resistivity using the Wenner array
        if self.wennerLayout == True:

            a = self.voltageSpacing[0] * 2 # Does voltage spacing refer to a or a/2 in clark2011? Change below, too, if not.
            Vm = self.meanVoltage
            I = self.meanCurrent

            if a != self.voltageSpacing[-1] * 2:

                message = (
                    'The probe spacing radio button has been set to ' +
                    'Wenner Spacing and the first and last Voltage Sep. ' +
                    'values are NOT EQUAL. All Voltage Sep. values ' +
                    'SHOULD BE EQUAL to eachother.\n\n' +
                    'Please ensure that the proper radio box is ' +
                    'selected and that the electrodes are placed in ' +
                    'the desired arrangement.')
                self.messageBox('Warning', message)
                pass

            self.apparentResistivity = wennerResistivity(a, Vm, I)
            self.canvas.addPoints(
                self.voltageSpacing, self.apparentResistivity)

        elif self.schlumbergerLayout == True:

            if self.voltageSpacing[0] == self.voltageSpacing[-1]:

                message = (
                    'The probe spacing radio button has been set to ' +
                    'Schlumberger Spacing and the first and last ' +
                    'Voltage Sep. values are EQUAL. The voltage ' +
                    'separation must follow a particular pattern, ' +
                    'in which the first and last separation values ' +
                    'should NOT BE EQUAL.\n\n' +
                    'Please ensure that the proper radio box is ' +
                    'selected and that the electrodes are placed in ' +
                    'the desired arrangement.')
                self.messageBox('Warning', message)
                pass

            nRows = len(self.voltageSpacing)

            s, L = np.empty(nRows), np.empty(nRows)
            Vm = self.meanVoltage
            I = self.meanCurrent

            for i in range(nRows):

                if i == len(self.voltageSpacing) - 1:
                    break

                s[i] = self.voltageSpacing[i]
                L[i] = self.voltageSpacing[i + 1]

            self.apparentResistivity = schlumbergerResistivity(
                Vm, L, s, I)[:-1] # Leave off last return values as it should be nan
            self.canvas.addPoints(
                self.voltageSpacing[:-1], self.apparentResistivity)

        # Provide a message box if neither Wenner nor Schlumberger are selected
        else:
            message = (
                'The probe spacing radio button has not been set.\n\n' +
                'Please indicate whether a Schlumberger or Wenner layout '
                'has been used by selecting one of the radio buttons. The ' +
                'radio buttons are located at the botton left of the ' +
                'program, near the input table.')
            self.messageBox('Warning', message)
            pass

        return self.apparentResistivity


    def messageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.about(self, title, message)


    def wenner(self):

        self.schlumbergerLayout = False
        self.wennerLayout = True


    def schlumberger(self):

        self.schlumbergerLayout = True
        self.wennerLayout = False





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main = Main(tableData, headers, colors, (0, 0.5), 50, 50, angle=0.)
    main.show()

    sys.exit(app.exec_())
