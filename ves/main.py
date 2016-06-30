#!/usr/bin/env python3

import os
import sys
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

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

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction, QApplication, QMessageBox, QSizePolicy, QSplashScreen)
from PyQt5.uic import loadUiType


from aggregate import aggregateTable
from equations import (
    applyFilter, interpolateFieldData,
    schlumbergerResistivityModified,
    wennerResistivity)
from figures import InteractiveCanvas, ReportCanvas
from reportwindow import ReportWindow
from table import PalettedTableModel
from templates.tempData import (
    coefficients, columns, colors, headers,
    rowCount, tableData, old_coefficients,
    columns_reportWindow, headers_reportWindow,
    rowCount_reportWindow, tableData_reportWindow
)


# No need to change directory, as the change from loading
#  reportwindow.ReportWindow has the interpreters working directory still
#  set to the templates folder
UI_StartupWindow, QStartupWindow = loadUiType('mainwindow.ui')


class StartupWindow(QStartupWindow, UI_StartupWindow):
    """A Qt QMainWindow class object that is the first window of the
    Water 4/DRI VES Inverse Analysis software

    """
    def __init__(self, tableData, headers, colors, coefficients):
        """Initialization code that is executed on every instantiation

        Parameters
        ----------
        tableData: list
            A nested list [row][column] of the data that is associated with
            the QTableViewWidget. This data should always be up to date with
            what is present in the table view itself. Passed in to the
            PalettedTableModel
        headers: list
            Column header names passed in as a list of strings. Passed in to
            the PalettedTableModel
        colors: list
            List of strings that include hex colors defining the
            table row coloring. Passed in to the PalettedTableModel

        """
        super(StartupWindow, self).__init__()

        self.setupUi(self)

        # Center the window by default
        screenCenter = QApplication.desktop().screen().rect().center()
        windowCenter = self.rect().center()
        self.move(screenCenter - windowCenter)
        # Set the icon
        self.setWindowIcon(QIcon('hand_drill.png'))

        # Set up the propoerties dictating probe layout
        self.schlumbergerLayout = False
        self.wennerLayout = False
        self.colors = colors
        self.color = colors[0]

        # Set up the coefficients
        (self.shortFilterCoefficients, self.longFilterCoefficients,
            self.wennerCoefficients) = coefficients

        # Set up the model and tableView
        # pp.pprint('tabledata: {}'.format(tableData))
        # pp.pprint('headers: {}'.format(headers))
        # pp.pprint('colors: {}'.format(colors))
        self.model = PalettedTableModel(tableData, headers, colors)

        self.initTableView(self.model)

        self.tableViewWidget.resizeColumnsToContents()
        # self.tableViewWidget.show()

        self.aggregateTableForPlot()

        # Set up the QWidget with an InteractiveCanvas and
        #  NavigationToolbar instance
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

        #### Connect to table buttons
        self.addRowButton.clicked.connect(self.addRow)
        self.removeRowButton.clicked.connect(self.removeRow)

        #### Connect to spacing radio buttons
        # self.wennerRadioButton.toggled.connect(self.wenner)
        # self.schlumbergerRadioButton.toggled.connect(self.schlumberger)

        #### Connect to plot buttons
        self.plotDataButton.clicked.connect(self.compute)
        # self.newRectangleButton.clicked.connect(self.newRectangle)
        self.resetPlotButton.clicked.connect(self.resetPlot)

        #### Connect to the decimal separator check box
        # self.decimalCheckBox.clicked.connect(self.model.stripCommas)
        # self.initUi()

        #### Connect to analysis button
        self.launchAnalysisButton.clicked.connect(self.launchReportWindow)
        self.initUi()


    def launchReportWindow(self):
        """Launches the ReportWindow class on launch of VES Inverse Analysis"""
        # try:
        self.ReportCanvas = ReportCanvas(
            self.samplePoints, self.filteredResistivity,
            self.voltageSpacing, self.apparentResistivity,
            self.voltageSpacingExtrapolated, self.newResistivity)

        # self.close()
        pp.pprint('tableDATA REPORT WINDOW:')
        pp.pprint(tableData_reportWindow)
        self.ReportWindow = ReportWindow(self.ReportCanvas,tableData_reportWindow, headers_reportWindow,
                                         self.apparentResistivity, self.voltageSpacing)
        self.ReportWindow.show()

        # except AttributeError:
            # print('------THERE WAS AN ERROR')
            # print(AttributeError())
            # return


    def initUi(self):
        """Work in progress. Should hook up file menu"""
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
        """Set up the QTableViewWidget with the proper data and row spacing

        Parameters
        ----------
        model: `PalettedTableModel`
            An instantiated an active PalettedTableModel instance

        Notes
        -----
        Run once on instantiation of the class to space the rows

        """
        nRows = len(self.model.table)

        self.tableViewWidget.setModel(model)

        # Set the table to span 4 rows in the spacing columns
        for row in range(0, nRows, 4):
            for col in columns:
                self.tableViewWidget.setSpan(row, col, 4, 1)

        self.tableViewWidget.resizeColumnsToContents()

        self.tableViewWidget.show()


    def aggregateTableForPlot(self):
        """Apply the  aggregation function and assign the outputs to the class

        Notes
        -----
        This method assures that the voltageSpacing, meanVoltage, and
        meanCurrent properties are up to date with the table

        """
        pp.pprint('SELF model TABLE IS: ')
        pp.pprint(self.model.table)
        voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
            self.model.table)

        self.voltageSpacing = voltageSpacing
        self.meanVoltage = meanVoltage
        self.meanCurrent = meanCurrent

    def addRow(self):
        """Add 4 new rows (one sample location) to the table"""
        startRow = len(self.model.table)

        self.model.insertRows(startRow, 4)
        self.initTableView(self.model)


    def removeRow(self):
        """Remove 4 rows (one sample location) from the table"""
        startRow = len(self.model.table) - 4

        self.model.removeRows(startRow, 4)
        self.initTableView(self.model)


    def initPlot(self, draw=True):
        """Initialize the plot for the main window

        Parameters
        ----------
        draw: bool
            If True, the figure canvas will update. Otherwise, it will not

        Notes
        -----
        The plot is only created if apparentResistivity has already
        been calculated

        """
        plt.clf()
        self.aggregateTableForPlot()

        if hasattr(self, 'apparentResistivity'):
            voltageSpacing = self.voltageSpacing

            # computes new resistivity for new voltageSpacing
            self.compute()

            # if self.schlumberger:
            #     voltageSpacing = self.voltageSpacing[:-1]
            # print('VOLTAGE SPACING IN MAIN IS {}'.format(voltageSpacing))prinistivity))

            self.canvas.initFigure(voltageSpacing, self.apparentResistivity)

        if draw:
            self.canvas.fig.tight_layout()
            self.canvas.draw()


    def resetPlot(self):
        """Clear the plot of data and rectangles to redraw the layers"""
        # Catch ValueError that occurs if reset is clicked prior to plotting
        # try:
        #     self.canvas.mplRectangles = []
        #     self.canvas.rectCoordinates = []

        plt.clf()
        self.aggregateTableForPlot()
        self.initPlot()

        # except ValueError:
        #     pass


    def stripCommas(self, table):
        """Work in progress. Worth it?"""
        pass

    #     for row in len(table):

    #         for column in len(table[0]):

    #             value = self.table[row][column]
    #             value.replace(',', '.')

    #             self.table[row][column] = value
    #             del value


    def compute(self, suppress=False):
        """Compute apparent resistivity

        Parameters
        ----------
        suppress: bool
            If True, message boxes should be suppressed. Implemented to allow
            cross platform testing between Mac OS X and Ubuntu. Not currently
            working, likely going to ditch it

        Notes
        -----
        This is where all of the numerical crunching happens. The radioboxes
        in the main window define whether the schlumberger or wenner equation
        is employed, and there are warnings when the data do not fit the
        assumptions of the model. That is, when all of the spacings are not
        equal in a Wenner array, there is a warning. When at least 2 of the
        Schlumberger spacings are equal, there is a warning. Finally, if the
        operator forgets to select a radio button, there is a warning.

        """
        # Suppress msgBox if this module is not called directly for testing
        if __name__ != '__main__':
            suppress = True

        self.apparentResistivity = None
        self.aggregateTableForPlot()
        self.wennerLayout = True
        # Calculate apparent resistivity using the Wenner array
        if self.wennerLayout == True:

            #### Test and let user know spacing does not indicate Wenner Array
            # if not np.all(
            #     self.voltageSpacing * 2 == self.voltageSpacing[0] * 2):
                # self.wennerMessageBox(suppress)

            #Calculate apparent Resistivity
            self.apparentResistivity = wennerResistivity(
                self.voltageSpacing, self.meanVoltage, self.meanCurrent)

            self.canvas.addPointsAndLine(
                self.voltageSpacing, self.apparentResistivity)

            voltageSpacingExtrapolated, newResistivity = interpolateFieldData(
                self.voltageSpacing, self.apparentResistivity, 'wenner')

            self.voltageSpacingExtrapolated = voltageSpacingExtrapolated
            self.newResistivity = newResistivity

            self.filteredResistivity = applyFilter(
                self.newResistivity,
                self.wennerCoefficients)

            sampleInterval = np.log(10) / 3.
            self.samplePoints = np.arange(
                start=(-sampleInterval * 2),
                stop=(sampleInterval * 20),
                step=sampleInterval)

        # Calculate apparent resistivity using the Schlumberger array
        elif self.schlumbergerLayout == True:

            #### Test and let user know spacing does not indicate Schlum. array
            # if np.any(self.voltageSpacing[1:] == self.voltageSpacing[0]):
                # self.schlumbergerMessageBox(suppress)

            self.apparentResistivity = schlumbergerResistivityModified(
                self.voltageSpacing, self.meanVoltage, self.meanCurrent)
            self.canvas.addPointsAndLine(
                self.voltageSpacing, self.apparentResistivity)

            voltageSpacingExtrapolated, newResistivity = interpolateFieldData(
                self.voltageSpacing, self.apparentResistivity, 'schlumberger')
            self.voltageSpacingExtrapolated = voltageSpacingExtrapolated
            self.newResistivity = newResistivity

            self.filteredResistivity = applyFilter(
                self.newResistivity,
                self.longFilterCoefficients)

            sampleInterval = np.log(10) / 3.
            self.samplePoints = np.arange(
                start=(-sampleInterval * 2),
                stop=(sampleInterval * 20),
                step=sampleInterval)

        # Provide a message box if neither Wenner nor Schlumberger are selected
        else:
            # self.noSpacingMessageBox(suppress)
            return

        return self.apparentResistivity


    def wennerMessageBox(self, suppress=False):
        """Warning message box if Wenner assumptions are not met

        Parameters
        ----------
        suppress: bool
            If True, message boxes should be suppressed. Implemented to allow
            cross platform testing between Mac OS X and Ubuntu. Not currently
            working, likely going to ditch it

        """
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
        """Warning message box if Schlumberger assumptions are not met

        Parameters
        ----------
        suppress: bool
            If True, message boxes should be suppressed. Implemented to allow
            cross platform testing between Mac OS X and Ubuntu. Not currently
            working, likely going to ditch it

        """
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
        """Warning message box if no probe layout radiobutton has been selected

        Parameters
        ----------
        suppress: bool
            If True, message boxes should be suppressed. Implemented to allow
            cross platform testing between Mac OS X and Ubuntu. Not currently
            working, likely going to ditch it

        """
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
        """Define Wenner layout is True"""
        self.schlumbergerLayout = False
        self.wennerLayout = True


    def schlumberger(self):
        """Define Schlumberger layout is True"""
        self.schlumbergerLayout = True
        self.wennerLayout = False


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("fusion") #Changed the style to prevent "PyQt5: Gtk-CRITICAL error"
    app.setWindowIcon(QIcon('hand_drill.png'))

    splashPix = QPixmap('splash.png')
    splashScreen = QSplashScreen(splashPix, Qt.WindowStaysOnTopHint)

    splashScreen.setMask(splashPix.mask())
    splashScreen.show()
    app.processEvents()

    time.sleep(3)

    startup = StartupWindow(tableData, headers, colors, old_coefficients)
    startup.show()

    splashScreen.finish(startup)

    sys.exit(app.exec_())
