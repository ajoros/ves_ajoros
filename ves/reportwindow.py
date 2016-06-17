import os
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)


from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)

import numpy as np
np.seterr(over='ignore')

from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUiType

from table_reportWindow import PalettedTableModel_reportWindow
from templates.tempData import (
    columns_reportWindow, headers_reportWindow,
    rowCount_reportWindow, tableData_reportWindow)


os.chdir(os.path.join(os.path.dirname(__file__), 'templates'))
UI_ReportWindow, QReportWindow = loadUiType('reportwindow.ui')


class ReportWindow(UI_ReportWindow, QReportWindow):

    def __init__(self, canvas, tableData_reportWindow, headers_reportWindow):

        super(QReportWindow, self).__init__()

        self.setupUi(self)

        # Center the window by default
        screenCenter = QApplication.desktop().screen().rect().center()
        windowCenter = self.rect().center()
        self.move(screenCenter - windowCenter)
        # Set the icon
        self.setWindowIcon(QIcon('hand_drill.png'))

        self.canvas = canvas

        # rectCoordinates = canvas.rectCoordinates

        # self.rectCoordinates = rectCoordinates
        # self.nLayers = len(rectCoordinates)

        # if self.nLayers == 0:
        #     self.emptyRectangles(QApplication.quit)

        # if self.nLayers > 0:
        #     self.layersFromRectangles()

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # Set up the model and tableView
        pp.pprint('tableData_reportWindow: {}'.format(tableData_reportWindow))
        pp.pprint('headers_reportWindow: {}'.format(headers_reportWindow))
        self.model_reportWindow = PalettedTableModel_reportWindow(tableData_reportWindow, headers_reportWindow)
        self.initTableView_reportWindow(self.model_reportWindow)

        # Set default lat/long values
        self.longitudeLineEdit.setText('Please enter logitude (E/W)')
        self.latitudeLineEdit.setText('Please enter latitude (N/S)')

        self.LayersTableView.resizeColumnsToContents()
        print('About to SHOW LayersTableView')
        self.LayersTableView.showFullScreen()
        print('SHOWed LayersTableView')

        # Add a plot and matplotlib toolbar to the report window
        self.mplvl.addWidget(self.canvas)
        self.mplvl.addWidget(NavigationToolbar(
            self.canvas, self.canvas, coordinates=True))

    # def launchReportOutput(self):
    #     """ Launches the ReportOutput class on execution of Monte Carlo Simulation """

    def layersFromRectangles(self):

        layerWidths, maxResistivities, minResistivities = [], [], []

        for rectangle in self.rectCoordinates:
            xy, width, height = rectangle

            layerWidths.append(float(xy[0] + width))
            maxResistivities.append(float(xy[1]))
            minResistivities.append(float(xy[1] + height))

            del xy, width, height

        self.layerWidths = layerWidths
        self.maxResistivities = maxResistivities
        self.minResistivities = minResistivities


    def emptyRectangles(self, event):

        msgBox = QMessageBox(self)
        reply = msgBox.question(
            self, 'Warning',
            ('There were no rectangles drawn to define Earth layers. ' +
             'Slect "yes" to exit the program or "no" continue to '+
             'record latitude and longitude.'),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            sys.exit()

        else:
            self.layerWidths = None
            self.maxResistivities = None
            self.minResistivities = None

    def initTableView_reportWindow(self, model):
        """Set up the LayersTableView with the proper data and row spacing

        Parameters
        ----------
        model: `PalettedTableModel`
            An instantiated an active PalettedTableModel instance

        Notes
        -----
        Run once on instantiation of the class to space the rows

        """
        print('Inside initTableView_reportWindow def')
        nRows = len(self.model_reportWindow.table_reportWindow)
        print('nRows is {}'.format(nRows))
        print('There are {} columns'.format(len(columns_reportWindow)))
        self.LayersTableView.setModel(model)
        print('self.LayersTableView.setModel(model)')
        # Set the table to span 4 rows in the spacing columns
        for row in range(0, nRows, 4):
            for col in columns_reportWindow:
                self.LayersTableView.setSpan(row, col, 4, 1)

        self.LayersTableView.resizeColumnsToContents()
        print('self.LayersTableView.resizeColumnsToContents()')
        self.LayersTableView.show()
        print('Inside initTableView_reportWindow def and showed LayersTableView')