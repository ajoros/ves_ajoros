import os
import sys
import random
from io import BytesIO
import pprint

pp = pprint.PrettyPrinter(indent=4)

from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib
import numpy as np

np.seterr(over='ignore')
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressBar
from PyQt5.uic import loadUiType
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from aggregate import aggregateTable_ReportWindow
from table_reportWindow import PalettedTableModel_reportWindow
from templates.tempData import (
    coefficients, columns_reportWindow, headers_reportWindow,
    rowCount_reportWindow, tableData_reportWindow)
from ves_inverse import (
    montecarlo_sim, readData, error, transf, filters, rmsfit, spline, splint,
    p, r, rl, t, b, asav, asavl, adatl, rdatl, adat, rdat, pkeep, rkeep, rkeepl, pltanswer, pltanswerl,
    pltanswerkeep, pltanswerkeepl, small, xlarge, x, y, y2, u, new_x, new_y)

os.chdir(os.path.join(os.path.dirname(__file__), 'templates'))
UI_ReportWindow, QReportWindow = loadUiType('reportwindow.ui')


class ReportWindow(UI_ReportWindow, QReportWindow):
    def __init__(self, canvas, tableData_reportWindow, headers_reportWindow, apparentResistivity, voltageSpacing):

        super(QReportWindow, self).__init__()

        self.setupUi(self)

        # Center the window by default
        screenCenter = QApplication.desktop().screen().rect().center()
        windowCenter = self.rect().center()
        self.move(screenCenter - windowCenter)
        # Set the icon
        self.setWindowIcon(QIcon('hand_drill.png'))

        self.canvas = canvas
        self.ar = apparentResistivity
        self.vs = voltageSpacing

        # rectCoordinates = canvas.rectCoordinates

        # self.rectCoordinates = rectCoordinates
        # self.nLayers = len(rectCoordinates)

        # if self.nLayers == 0:
        #     self.emptyRectangles(QApplication.quit)

        # if self.nLayers > 0:
        #     self.layersFromRectangles()

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # Set up the model and tableView
        pp.pprint('*** tableData_reportWindow: {}'.format(tableData_reportWindow))
        pp.pprint('*** headers_reportWindow: {}'.format(headers_reportWindow))
        self.model_reportWindow = PalettedTableModel_reportWindow(tableData_reportWindow, headers_reportWindow)
        self.initTableView_reportWindow(self.model_reportWindow)

        # Set default lat/long values
        self.longitudeLineEdit.setText('Please enter longitude (E/W)')
        self.latitudeLineEdit.setText('Please enter latitude (N/S)')

        self.LayersTableView.resizeColumnsToContents()
        self.LayersTableView.showFullScreen()

        # Add a plot and matplotlib toolbar to the report window
        self.mplvl.addWidget(self.canvas)
        self.mplvl.addWidget(NavigationToolbar(
            self.canvas, self.canvas, coordinates=True))

        self.aggregateTableForMonteCarlo()
        self.rerunMontecarlo.clicked.connect(self.computeMonteCarlo)

    def aggregateTableForMonteCarlo(self):
        """Apply the aggregation function and assign the outputs to the class for Monte Carlo simulation"""

        # print('SELF model_reportWindow TABLE IS: {}'.format(self.model_reportWindow.table))

        layer, minthick, maxthick, minres, maxres = aggregateTable_ReportWindow(
            self.model_reportWindow.table)
        self.layer = layer
        self.minthick = minthick
        self.maxthick = maxthick
        self.minres = minres
        self.maxres = maxres

    def computeMonteCarlo(self):
        longtext = self.longitudeLineEdit.text()
        print('LONGTEXT IS {}'.format(longtext))
        lattext = self.latitudeLineEdit.text()
        print('LATTEXT IS {}'.format(lattext))
        datetimetext = self.dateTimeEdit.text()
        print('DATETIMETEXT IS {}'.format(datetimetext))

        """ Launches execution of Monte Carlo Simulation """
        iter_ = 10000  # number of iterations for the Monte Carlo guesses. to be input on GUI

        # INPUT
        arrayType = 'wenner'
        e = 5  # number of layers
        n = 2 * e - 1

        spac = 0.2  # smallest electrode spacing
        m = 20  # number of points where resistivity is calculated

        spac = np.log(spac)
        delx = np.log(10.0) / 6.

        # these lines apparently find the computer precision ep
        ep = 1.0
        ep = ep / 2.0
        fctr = ep + 1.
        while fctr > 1.:
            ep = ep / 2.0
            fctr = ep + 1.

        schlumbergerFilterCoefficients, wennerFilterCoefficients = coefficients

        # I know there must be a better method to assign lists. And probably numpy
        # arrays would be best. But my Python wasn't up to it. If the last letter
        # is an 'l' that means it is a log10 of the value

        # 65 is completely arbitrary - > Nearing retirement?
        # p = [0] * 20
        # r = [0] * 65
        # rl = [0] * 65
        # t = [0] * 50
        # b = [0] * 65
        # asav = [0] * 65
        # asavl = [0] * 65
        # adatl = [0] * 65
        # rdatl = [0] * 65
        # adat = [0] * 65
        # rdat = [0] * 65
        # pkeep = [0] * 65
        # rkeep = [0] * 65
        # rkeepl = [0] * 65
        # pltanswer = [0] * 65
        # pltanswerl = [0] * 65
        # pltanswerkeep = [0] * 65
        # pltanswerkeepl = [0] * 65
        #
        # rl = [0] * 65
        # small = [0] * 65
        # xlarge = [0] * 65
        #
        # x = [0] * 100
        # y = [0] * 100
        # y2 = [0] * 100
        # u = [0] * 5000
        # new_x = [0] * 1000
        # new_y = [0] * 1000
        # ndat = 13
        # hard coded data input - spacing and apparent resistivities measured
        # in the field
        self.aggregateTableForMonteCarlo()
        print('self.layer is {}'.format(self.layer))
        print('self.minthick is {}'.format(self.minthick))
        print('self.maxthick is {}'.format(self.maxthick))
        print('self.minres is {}'.format(self.minres))
        print('self.maxres is {}'.format(self.maxres))

        adat = [0, 3., 4.5, 6., 9., 13.5, 21., 30., 45., 60., 90., 135., 210., 300.]
        print('adat is: {}'.format(adat))
        print('VOLTAGE SPACING from mainwindow (VS) is: {}'.format(self.vs.tolist()))
        print('VOLTAGE SPACING (VS) from mainwindow type is: {}'.format(type(self.vs.tolist())))
        vs_list = [0] + self.vs.tolist() + 40*[0]

        # adat = [0., 0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30.,  70.]
        rdat = [0, 9295., 4475., 2068., 1494., 764., 375., 294., 245., 235., 156., 118., 83., 104.]
        print('rdat is: {}'.format(rdat))
        print('APPARENT RESISTIVITY from mainwindow (AR) is: {}'.format(self.ar.tolist()))
        print('APPARENT RESISTIVITY (AR) from mainwindow type is: {}'.format(type(self.ar.tolist())))
        ar_list = [0] + self.ar.tolist() + 40*[0]
        # rdat = [0., 125., 110., 95., 40., 24., 15., 10.5, 8., 6., 6.5, 11., 25.]

        one30 = 1.e30
        rms = one30
        errmin = 1.e10
        ndat = len(self.vs.tolist())
        # this is where the range in parameters should be input from a GUI
        # I'm hard coding this in for now

        # enter thickness range for each layer and then resistivity range.
        # for 3 layers small[1] and small[2] are low end [MINIMUM] of thickness range
        # small[3], small[4] and small[5] are the low end [MINIMUM] of resistivities

        xlarge = [0] + self.maxthick[:len(self.maxthick)-1] + self.maxres + 40*[0]
        small = [0] + self.minthick[:len(self.minthick)-1] + self.minres + 40*[0]
        print('xlarge is: {}'.format(xlarge))
        print('small is: {}'.format(small))
        print('ndat is: {}'.format(ndat))
        montecarlo_sim(iter_, e, errmin, ndat, vs_list, ar_list, small, xlarge, lattext, longtext, datetimetext)
        # ****SAVE WHATEVER IS IN REPORTWINDOW TABLE TO****
        # ****THE SMALL and XLARGE VARIABLES ABOVE****

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
             'Slect "yes" to exit the program or "no" continue to ' +
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
        nRows = len(self.model_reportWindow.table)
        self.LayersTableView.setModel(model)
        # Set the table to span 4 rows in the spacing columns
        for row in range(0, nRows):
            for col in columns_reportWindow:
                self.LayersTableView.setSpan(row, col, 1, 1)

        self.LayersTableView.resizeColumnsToContents()
        self.LayersTableView.show()
