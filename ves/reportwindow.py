import os

from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUiType


os.chdir(os.path.join(
    os.path.dirname(__file__),
    'templates'))
UI_ReportWindow, QReportWindow = loadUiType('reportwindow.ui')


class ReportWindow(UI_ReportWindow, QReportWindow):

    def __init__(self):

        super(QReportWindow, self).__init__()

        self.setupUi(self)

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # Set default Earth parameters
        self.rhoALineEdit.setText('  1.00')
        self.rhoBLineEdit.setText(' 10.00')
        self.rhoMLineEdit.setText('100.00')
        self.dALineEdit.setText(' 10.00')

        # Set default lat/long values
        self.longitudeLineEdit.setText('Please enter logitude (E/W)')
        self.latitudeLineEdit.setText('Please enter latitude (N/S)')
