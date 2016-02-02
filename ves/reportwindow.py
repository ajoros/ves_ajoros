import os
import sys

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUiType


os.chdir(os.path.join(os.path.dirname(__file__), 'templates'))
UI_ReportWindow, QReportWindow = loadUiType('reportwindow.ui')


class ReportWindow(UI_ReportWindow, QReportWindow):

    def __init__(self, rectCoordinates=[]):

        super(QReportWindow, self).__init__()

        self.setupUi(self)

        self.rectCoordinates = rectCoordinates

        if len(rectCoordinates) == 0:
            self.emptyRectangles(QApplication.quit)

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


    def emptyRectangles(self, event):

        msgBox = QMessageBox(self)
        reply = msgBox.question(
            self, 'Warning',
            ('There were no rectangles drawn to define layers. Would ' +
             'you like to exit the program or continue to adjust the ' +
             'Earth parameters and mark location?'),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            sys.exit()
        else:
            pass
