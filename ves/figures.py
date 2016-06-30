import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

plt.style.use('bmh')

from PyQt5.QtWidgets import QSizePolicy

from templates.tempData import colors


class InteractiveCanvas(FigureCanvas):
    """An interactive matplotlib figure that allows for the plotting of data
    on a log-log axis with interactive matplotlib.patches.Rectangle drawing

    """

    def __init__(self, xdata, ydata, parent=None,
                 xlabel='x label', ylabel='y label',
                 linestyle='--', marker='o',
                 dpi=150, hold=False, alpha=0.5, colors=None):
        """Initialization method. Executes every time initialization occurs

        Parameters
        ----------
        xdata: `np.array.float64`
            Array of the input data to be plotted on the x-axis
        ydata: np.array.float64
            Array of the input data to be plotted on the y-axis
        parent: None
            Parent object of the class
        xlabel: str
            Label for the x-axis of the plot
        ylabel: str
            Label for the y-axis of the plot
        linestyle: str
            Matplotlib linestyle to be used to draw the line on the graph
        marker: str
            Matplotlib marker type to be used to draw the points on the graph
        dpi: int
            Dots per inch of the desired figure
        hold: bool
            Boolean that desides whether or not the plot should hold on
            the axes during instantiation/drawing
        alpha: float
            Transparency level of the rectangles that are drawn onto the
            figure canvas
        colors: list
            List of matplotlib acceptable color keys to be used in generation
            of the rectangles. Typically matches the table rows

        Notes
        -----
        This class implements the matplotlib Qt5 backend to allow for insertion
        of the resultant figure into a Qt application. The class allows for
        interactive generation of rectangles over a log/log axes plot.

        """
        # Save figure input parameters as class properties
        self.xdata = xdata
        self.ydata = ydata
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.linestyle = linestyle
        self.marker = marker
        self.dpi = dpi
        self.hold = hold
        self.alpha = alpha
        self.colors = colors

        # Initialize empty list to store mpl rectangles and their coordinates
        self.rectCoordinates = []
        self.mplRectangles = []

        # Initialize a figure, axis, and axes
        self.fig = Figure(dpi=self.dpi)
        self.ax = plt.gca()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.margins(0.1)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(self.hold)

        # Initialize a FigureCanvas from the figure
        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.ax.figure.canvas)

        self.initFigure(self.xdata, self.ydata)

        # Allow the FigureCanvas to adjust with Main window using mpl Qt5 API
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Connect the mouse/trackpad to the FigureCanvas
        self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onPress)
        self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onRelease)

        # Super from the class for Qt
        super(InteractiveCanvas, self).__init__(self.fig)

    def initFigure(self, xdata, ydata):
        """Initialize the figure

        Parameters
        ----------
        xdata: `np.array`
            A flat numpy array of x values for the plot
        ydata: `np.array`
            A flat numpy array of y values for the plot

        Notes
        -----
        The plot will not have a tight layout until data has been passed in.
        This is currently the source of the semi-unsightly bug of misaligned
        axes on start up. Plotting the data "fixes" the bug.

        """
        if xdata is None or ydata is None:
            return

        # Currently ydata is longer than xdata with schlumberger, so handle
        #   that if it makes it this far into the program
        if len(xdata) != len(ydata):
            if len(ydata) > len(xdata):
                xdata = xdata[:len(ydata)]
            else:
                ydata = ydata[:len(xdata)]

        # Set up an empty rectangle for drawing and plot the x/y data
        self.rect = Rectangle(
            (0, 0), 0, 0, alpha=self.alpha, color='grey')
        self.addPointsAndLine(xdata, ydata, draw=True)

        # Create an mpl axis and set the labels, add the rectangle
        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()
        self.ax.margins(0.1)

        # Draw extant rectangles if applicable
        if self.mplRectangles:
            self.drawRectangles()

        # Update the figure object/property
        self.fig = plt.gcf()

        self.fig.tight_layout()

    def drawRectangles(self):
        """Adds rectangles to the plot if they are currently stored"""
        # Iterate through the mpl Rectangles to draw them with the proper color
        for i, rectangle in enumerate(self.rectCoordinates):
            color = self.colors[i * 4]
            xy, width, height = rectangle

            rect = Rectangle(
                xy, width, height, alpha=self.alpha, color=color)

            self.ax.add_patch(rect)

    def addPointsAndLine(self, xdata, ydata, color='#348ABD', draw=True):
        """Adds the points and a line to the figure

        Parameters
        ----------
        xdata: `np.array`
            A flat numpy array of x values for the plot
        ydata: `np.array`
            A flat numpy array of y values for the plot
        color: str
            Hex code or other matplotlib accepted color key for the points/line
        draw: bool
            If True, the plot will be drawn. If False, it will not. Mainly a
            product of the test code

        """
        # Currently ydata is longer than xdata with schlumberger, so handle
        #   that if it makes it this far into the program
        if len(xdata) != len(ydata):
            if len(ydata) > len(xdata):
                xdata = xdata[:len(ydata)]
            else:
                ydata = ydata[:len(xdata)]

        # log/log plot of x and y data
        plt.semilogy(
            xdata, ydata, linestyle=self.linestyle,
            marker=self.marker, color=color, label="Observed")
        # plt.margins(x=.5, y=.5)

        # Draw the updates
        if draw:
            self.fig.tight_layout()
            self.ax.figure.canvas.draw()
            self.ax.margins(0.1)
            self.legend = self.ax.legend()
            if self.legend:
                self.ax.legend_ = None
            try:
                self.legend.remove()
                plt.legend()
                # lgd = plt.legend()
                # print('REMOVED OLD and PLOTTED NEW LEGEND')
            except:
                plt.legend()
                # print('PLOTTED NEW LEGEND')

    def onPress(self, event):
        """Handle mouse press events on the matplotlib figure cavas

        Parameters
        ----------
        event: matplotlib.event
            The matplotlib event definition. In this case, a mouse click.

        """
        self.x0 = event.xdata
        self.y0 = event.ydata

    def onRelease(self, event):
        """Handles release of mouse button events on the matplotlib canvas

        Parameters
        ----------
        event: matplotlib.event
            The matplotlib event definition. In this case, a mouse release.

        """
        try:
            self.x1 = event.xdata
            self.y1 = event.ydata

            # Create a rectangle on the plot
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))

            self.ax.figure.canvas.draw()

            # Store and return the rectangle attributes as a tuple
            self.rectxy = (
                self.rect.get_xy(), self.rect._width, self.rect._height)

            return self.rectxy

        except TypeError:
            pass


class ReportCanvas(FigureCanvas):
    """pass"""

    def __init__(self, samplePoints, filteredResistivity,
                 voltageSpacing, apparentResistivity,
                 voltageSpacingExtrapolated, newResistivity,
                 xlabel='Electrode Spacing (m)',
                 ylabel='Apparent Resitivity (ohm-m)',
                 linestyle='--', marker='o',
                 dpi=150, hold=False, colors=colors[0:5:4][::-1]):
        # Note: "colors" list is reversed in previous line.
        plt.clf()

        # Save figure input parameters as class properties
        self.samplePoints = samplePoints
        self.filteredResistivity = filteredResistivity
        self.voltageSpacing = voltageSpacing
        self.apparentResistivity = apparentResistivity
        self.voltageSpacingExtrapolated = voltageSpacingExtrapolated
        self.newResistivity = newResistivity

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.linestyle = linestyle
        self.marker = marker
        self.dpi = dpi
        self.hold = hold
        self.colors = colors
        self.fig = Figure(dpi=dpi)

        # Super from the class for Qt
        super(ReportCanvas, self).__init__(self.fig)

        # Initialize a FigureCanvas from the figure
        FigureCanvas.__init__(self, self.fig)

        # Allow the FigureCanvas to adjust with Main window using mpl Qt5 API
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.setParent(self.ax.figure.canvas)
        self.ax = plt.gca()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.margins(0.1)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(hold)

        self.initFigure()

        # Allow the FigureCanvas to adjust with Main window using mpl Qt5 API
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Super from the class for Qt
        super(ReportCanvas, self).__init__(self.fig)

    def initFigure(self):
        # Plot out the results
        plt.semilogy(self.voltageSpacingExtrapolated,
                     self.filteredResistivity,
                     marker=self.marker,
                     linestyle=self.linestyle,
                     color=self.colors[0],
                     label="Filtered")
        plt.semilogy(self.voltageSpacing, self.apparentResistivity,
                     marker=self.marker,
                     linestyle=self.linestyle,
                     color=self.colors[1],
                     label="Observed")
        plt.legend()

        # Create an mpl axis and set the labels, add the rectangle
        self.ax = plt.gca()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.margins(0.5)

        # self.ax.add_patch(self.rect)
        self.ax.figure.canvas.draw()

        # Update the figure object/property
        self.fig = plt.gcf()

        self.fig.tight_layout()
