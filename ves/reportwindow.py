import os
import sys

from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)
import numpy as np
np.seterr(over='ignore')

from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUiType


os.chdir(os.path.join(os.path.dirname(__file__), 'templates'))
UI_ReportWindow, QReportWindow = loadUiType('reportwindow.ui')


class ReportWindow(UI_ReportWindow, QReportWindow):

    def __init__(self, canvas):

        super(QReportWindow, self).__init__()

        self.setupUi(self)

        # Center the window by default
        screenCenter = QApplication.desktop().screen().rect().center()
        windowCenter = self.rect().center()
        self.move(screenCenter - windowCenter)
        # Set the icon
        self.setWindowIcon(QIcon('hand_drill.png'))

        self.canvas = canvas

        rectCoordinates = canvas.rectCoordinates

        self.rectCoordinates = rectCoordinates
        self.nLayers = len(rectCoordinates)

        if self.nLayers == 0:
            self.emptyRectangles(QApplication.quit)

        if self.nLayers > 0:
            self.layersFromRectangles()

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # Set default Earth parameters
        self.rhoALineEdit.setText('  1.00')
        self.rhoBLineEdit.setText(' 10.00')
        self.rhoMLineEdit.setText('100.00')
        self.dALineEdit.setText(' 10.00')

        # Set default lat/long values
        self.longitudeLineEdit.setText('Please enter logitude (E/W)')
        self.latitudeLineEdit.setText('Please enter latitude (N/S)')

        self.resultsTextBox.append('This is a test:\n  {}'.format('drill'))

        # Add a plot and matplotlib toolbar to the report window
        self.mplvl.addWidget(self.canvas)
        self.mplvl.addWidget(NavigationToolbar(
            self.canvas, self.canvas, coordinates=True))


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
