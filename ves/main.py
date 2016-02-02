#!/usr/bin/env python3
import os
import sys
import time

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
plt.style.use('bmh')
from matplotlib.figure import Figure

import numpy as np
np.seterr(over='ignore')

from PyQt5.QtCore import pyqtSlot, QDateTime, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction, QApplication, QMessageBox, QSizePolicy, QSplashScreen)
from PyQt5.uic import loadUiType

from aggregate import aggregateTable
from equations import schlumbergerResistivity, wennerResistivity
from figure import InteractiveCanvas
from reportwindow import ReportWindow
from table import PalettedTableModel
from templates.tempData import (
    columns, colors, headers, rowCount, tableData)


# No need to change directory, as the change from loading
#  reportwindow.ReportWindow has the interpreters working directory still
#  set to the templates folder
UI_StartupWindow, QStartupWindow = loadUiType('mainwindow.ui')


class StartupWindow(QStartupWindow, UI_StartupWindow):

    def __init__(self, tableData, headers, colors):

        super(StartupWindow, self).__init__()

        self.setupUi(self)

        # Set up the propoerties dictating probe layout
        self.schlumbergerLayout = False
        self.wennerLayout = False
        self.colors = colors
        self.color = colors[0]

        # Set up the model and tableView
        self.model = PalettedTableModel(tableData, headers, colors)

        self.initTableView(self.model)

        self.tableViewWidget.resizeColumnsToContents()
        self.tableViewWidget.show()

        self.aggregateTableForPlot()

        # Set up the QWidget with an InteractiveCanvas and
        #  NavigationToolbar instance
        self.rects = []
        self.canvas = InteractiveCanvas(
            np.array([]), np.array([]),
            xlabel='Voltage Probe Spacing (m)',
            ylabel='Resistivity (Ohm-m)',
            linestyle='--', marker='o',
            dpi=150, hold=False, alpha=0.4, colors=self.colors)

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

        # Connect to spacing radio buttons
        self.wennerRadioButton.toggled.connect(self.wenner)
        self.schlumbergerRadioButton.toggled.connect(self.schlumberger)

        # Connect to plot buttons
        self.plotDataButton.clicked.connect(self.compute)
        self.newRectangleButton.clicked.connect(self.newRectangle)
        self.resetPlotButton.clicked.connect(self.resetPlot)

        # Connect to the decimal separator check box
        self.decimalCheckBox.clicked.connect(self.model.stripCommas)
        # self.initUi()

        # Connect to analysis button
        self.launchAnalysisButton.clicked.connect(self.launchReportWindow)

        self.initUi()

    def print_hey(self):
        print('hey')


    @pyqtSlot()
    def launchReportWindow(self):

        self.close()

        self.reportWindowClass = ReportWindow()
        self.reportWindowClass.show()



    def initUi(self):

        saveAction = QAction(QIcon('save.png'), '&Save As', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(QApplication.saveStateRequest)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QApplication.quit)

        # fileMenu = menubar.addMenu('&File')
        self.menuBar.addAction(saveAction)
        self.menuBar.addAction(exitAction)

        # addRowButton = QPushButton()
        # addRowButton.clicked.connect(PalettedTableModel.insertRows(0, 1))

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

    def addRow(self):

        startRow = len(self.model.table)

        self.model.insertRows(startRow, 4)
        self.initTableView(self.model)


    def removeRow(self):

        startRow = len(self.model.table) - 4

        self.model.removeRows(startRow, 4)
        self.initTableView(self.model)


    def initPlot(self, draw=True):

        plt.clf()
        self.aggregateTableForPlot()

        if hasattr(self, 'apparentResistivity'):
            voltageSpacing = self.voltageSpacing

            if self.schlumberger:
                voltageSpacing = self.voltageSpacing[:-1]

            self.canvas.initFigure(voltageSpacing, self.apparentResistivity)

        if draw:
            self.canvas.fig.tight_layout()
            self.canvas.draw()


    def resetPlot(self):

        # Catch ValueError that occurs if reset is clicked prior to plotting
        try:
            self.canvas.mplRectangles = []
            self.canvas.rectCoordinates = []

            plt.clf()
            self.aggregateTableForPlot()
            self.initPlot()

        except ValueError:
            pass


    def stripCommas(self, table):
        pass

    #     for row in len(table):

    #         for column in len(table[0]):

    #             value = self.table[row][column]
    #             value.replace(',', '.')

    #             self.table[row][column] = value
    #             del value


    def newRectangle(self):

        try:
            if self.canvas.rectxy:
                self.canvas.mplRectangles.append(self.rect)
                self.canvas.rectCoordinates.append(self.canvas.rectxy)

            self.initPlot(draw=False)

            self.canvas.addPointsAndLine(
                self.voltageSpacing, self.apparentResistivity, draw=False)

            if self.canvas.mplRectangles:
                self.canvas.drawRectangles()

            plt.tight_layout()

            self.canvas.ax.figure.canvas.draw()

            return


        except AttributeError:
            pass


    def compute(self, suppress=False):

        # Suppress msgBox if this module is not called directly for testing
        if __name__ != '__main__':
            suppress = True

        self.apparentResistivity = None
        self.aggregateTableForPlot()

        # Calculate apparent resistivity using the Wenner array
        if self.wennerLayout == True:

            # Test and let user know spacing does not indicate Wenner Array
            if not np.all(
                self.voltageSpacing * 2 == self.voltageSpacing[0] * 2):
                self.wennerMessageBox(suppress)

            self.apparentResistivity = wennerResistivity(
                self.voltageSpacing, self.meanVoltage, self.meanCurrent)
            self.canvas.addPointsAndLine(
                self.voltageSpacing, self.apparentResistivity)

        elif self.schlumbergerLayout == True:

            # Test and let user know spacing does not indicate Schlum. array
            if np.any(self.voltageSpacing[1:] == self.voltageSpacing[0]):
                self.schlumbergerMessageBox(suppress)

            self.apparentResistivity = schlumbergerResistivity(
                self.voltageSpacing, self.meanVoltage, self.meanCurrent)[:-1] # Leave off last return values as it should be nan
            self.canvas.addPointsAndLine(
                self.voltageSpacing[:-1], self.apparentResistivity)

        # Provide a message box if neither Wenner nor Schlumberger are selected
        else:
            self.noSpacingMessageBox(suppress)
            return

        return self.apparentResistivity


    def wennerMessageBox(self, suppress=False):

        # Suppress argument is to simplify testing
        if suppress:
            return

        self.msgBox = None

        self.msgBox = QMessageBox(self)
        self.msgBox.about(
            self, 'Warning',
            ('The probe spacing radio button has been set to Wenner Spacing ' +
             'all of the Voltage Sep. values are NOT EQUAL. All Voltage ' +
             'Sep. values SHOULD BE EQUAL to eachother.\n\n' +

             'Please ensure that the proper radio box is ' +
             'selected and that the electrodes are placed in ' +
             'the desired arrangement.'))


    def schlumbergerMessageBox(self, suppress=False):

        # Suppress argument is to simplify testing
        if suppress:
            return

        self.msgBox = None

        self.msgBox = QMessageBox(self)
        self.msgBox.about(
            self, 'Warning',
            ('The probe spacing radio button has been set to ' +
             'Schlumberger Spacing and the first and last ' +
             'Voltage Sep. values are EQUAL. The voltage ' +
             'separation must follow a particular pattern, ' +
             'in which the first and last separation values ' +
             'should NOT BE EQUAL.\n\n' +

             'Please ensure that the proper radio box is ' +
             'selected and that the electrodes are placed in ' +
             'the desired arrangement.'))


    def noSpacingMessageBox(self, suppress=False):

        # Suppress argument is to simplify testing
        if suppress:
            return

        self.msgBox = None

        self.msgBox = QMessageBox(self)
        self.msgBox.about(
            self, 'Warning',
            ('The probe spacing radio button has not been set.\n\n' +

             'Please indicate whether a Schlumberger or Wenner layout '
             'has been used by selecting one of the radio buttons. The ' +
             'radio buttons are located at the botton left of the ' +
             'program, near the input table.'))


    def wenner(self):

        self.schlumbergerLayout = False
        self.wennerLayout = True


    def schlumberger(self):

        self.schlumbergerLayout = True
        self.wennerLayout = False



if __name__ == '__main__':

    app = QApplication(sys.argv)

    splashPix = QPixmap('splash.png')
    splashScreen = QSplashScreen(splashPix, Qt.WindowStaysOnTopHint)

    splashScreen.setMask(splashPix.mask())
    splashScreen.show()
    app.processEvents()

    time.sleep(0.1)

    startup = StartupWindow(tableData, headers, colors)
    startup.show()

    splashScreen.finish(startup)

    sys.exit(app.exec_())
