import os
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType


os.chdir(os.path.join(os.getcwd(), 'ves'))
UI_MainWindow, QMainWindow = loadUiType('mainwindow.ui')

class Main(QMainWindow, UI_MainWindow):

    def __init__(self, ):

        super(Main, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())
