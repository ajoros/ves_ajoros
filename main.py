import os
import sys

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as Canvas,
    NavigationToolbar2QT as NavigationToolbar)

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.uic import loadUiType

from aggregate import voltage_spacing, mean_voltage, mean_current
import interactivePlot


os.chdir(os.path.join(os.path.dirname(__file__), 'ves'))
UI_MainWindow, QMainWindow = loadUiType('mainwindow.ui')
print(UI_MainWindow)
print(QMainWindow)
# print(dir(UI_MainWindow))
# print(dir(QMainWindow))

# class Main(QMainWindow, UI_MainWindow):

#     def __init__(self, ):
#         super(Main, self).__init__()

#         self.setupUi(self)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = Main()
#     print(dir(main))
#     main.show()
#     sys.exit(app.exec_())

class Main(QMainWindow, UI_MainWindow):

    def __init__(self, xy, width, height, angle=0.):

        # width = 8
        # height = 5
        # dpi = 300

        # self.figure = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = self.figure.add_subplot(111)
        # self.mplwidget = interactivePlot.Plot(
        #     (0, 0), 1, 1, alpha=0.5, color='red')

        # self.setCentralWidget(self.mplwidget)
        # self.plot(self.mplwidget.axes)

        # width = 8
        # height = 5
        # dpi = 300

        # self.Figure = Figure(figsize=(width, height), dpi=dpi)
        # self.mplwidgets = interactivePlot.Plot(
        #     (0, 0), 1, 1, alpha=0.5, color='red')

        # self.setCentralWidget(self.mplwidgets)
        # self.plot(self.mplwidgets.axes)

        super(Main, self).__init__()

        self.setupUi(self)


    def addmpl(self, fig):

        self.canvas = Canvas(fig)
        # self.mplvl.addWidget(self.canvas)
        # self.canvas.setParent(self.mplwindow)
        # print(self.canvas)
        # print(dir(self.canvas))
        # self.canvas.add_subplot(fig)
        self.canvas.draw()
        # self.toolbar = NavigationToolbar(
        #     self.canvas, self.mplwindow, coordinates=True)
        # self.mplvl.addWidget(self.toolbar)


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


if __name__ == '__main__':
    width = 8
    height = 5
    dpi = 300

    figure = Figure(figsize=(width, height), dpi=dpi)
    ax1fig1 = figure.add_subplot(111)
    # fig = plt.subplot(111)
    # figure = interactivePlot.Plot(
    #     fig, (0, 0), 1, 1, alpha=0.5, color='red')
    ax1fig1.plot(voltage_spacing, mean_voltage, '--')
    ax1fig1.plot(voltage_spacing, mean_current, '--')

    app = QApplication(sys.argv)

    main = Main((0, 0.5), 0.25, 0.25)
    main.addmpl(figure)
    main.show()

    sys.exit(app.exec_())
