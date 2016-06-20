import sys

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QTableView

# from templates.tempData import (
#     columnCount, columns, colors, headers, rowCount, tableData)

from templates.tempData import (
    columns_reportWindow, headers_reportWindow, columnCount_reportWindow,
    rowCount_reportWindow, tableData_reportWindow)


class PalettedTableModel_reportWindow(QAbstractTableModel):
    """Class object representing the QtTable model upon which
    the GUI is built. Must interact with a QtTableView object

    """

    def __init__(self, table=[[]], headers=[], colors=[], parent=None):
        """Initialization method for the PalettedTableModel. This portion
        of the code will execute every time a PalettedTableModel object
        is instantiated

        Parameters
        ----------
        Args:
            table: list
                A nested table containing the data abstracted in the
                QAbstractTableModel. Indexed as [row][column]
            headers: list
                A list containing hex color codes (or some other matplotlib
                accepted value) to define the row colors
            parent: None
                The object from which the instantiated object inherits

        Notes
        -----
        All attributes on this model were required to be set as public
        attributes (in the Python world, i.e. no leading _ to the name).
        This allows for access to the table data and color values regardless
        of whether or not the object is instantiated in __main__.

        """
        # Default parent to self
        if parent is None:
            parent = self

        # For Qt
        super(PalettedTableModel_reportWindow, self).__init__()

        QAbstractTableModel.__init__(self, parent)

        # Set up the table, table headers, and colors properties
        self.table = table
        self.headers = headers
        # self.colors = colors


    def rowCount(self, parent):
        """Define the row count of the table

        Parameters
        ----------
        Args:
            parent: None
            The object from which this method considers the parent (I think you
            inherit from your parents)

        Returns
        -------
        rowCount: int
            An integer representing the number of rows currently in the table

        """
        return len(self.table)


    def columnCount(self, parent):
        """Define the row count of the table

        Parameters
        ----------
        Args:
            parent: None
            The object from which this method considers the parent (I think you
            inherit from your parents)

        Returns
        -------
        columnCount: int
            An integer representing the number of columns currently
            in the table

        """
        return len(self.table[0])


    def flags(self, index):
        """Sets the Qt flags

        Parameters
        ----------
            index: `Qt:::QModelIndex`
                http://doc.qt.io/qt-5/qmodelindex.html
                A Qt object describing where in the table the current cell is

        Returns
        -------
        Qt objects

        """
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def update(self, table):
        """Define the method which updates the table with new data

        Parameters
        ----------
            table: list
                A nested table containing the data abstracted in the
                QAbstractTableModel. Indexed as [row][column]

        Returns
        -------
            None
                Simply updates a table

        """
        self.table = table


    def data(self, index, role):
        """Define the alignment and actions of the table on edit,
        hover, display

        Parameters
        ----------
            index: `Qt:::QModelIndex`
                http://doc.qt.io/qt-5/qmodelindex.html
                A Qt object describing where in the table the current cell is
            role: `Qt::ItemDataRole`
                http://doc.qt.io/qt-5/qt.html#ItemDataRole-enum
                Tells the view what type of data to get from the table model

        Returns
        -------
            variable:
                The returns are definied by the role. Most values are integers

        """
        # Get the Qt rtable row and column
        row = index.row()
        column = index.column()

        # For each cell, define an action for Qt roles
        #  http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ItemDataRole-enum
        if role == Qt.EditRole:

            return self.table[row][column]

        if role == Qt.ToolTipRole:

            return 'Cell value: {}'.format(
                self.table[row][column])

        if role == Qt.DisplayRole:

            return self.table[row][column]

        if role == Qt.TextAlignmentRole:

            return Qt.AlignHCenter | Qt.AlignVCenter


    def setData(self, index, value, role=Qt.EditRole):
        """This method sets the data to the appropriate value when appprops

        Parameters
        ----------
        index: `Qt:::QModelIndex`
            http://doc.qt.io/qt-5/qmodelindex.html
            A Qt object describing where in the table the current cell is
        value: str
            The update or new value for the cell in question, mark?
        role: `Qt::EditRole`
            The role for which Qt is to use in updating or setting the data

        Returns
        -------
        bool: True or False, depending on needs

        """
        if role == Qt.EditRole:

            row = index.row()
            column = index.column()

            if isinstance(value, str):

                self.table[row][column] = value
                self.dataChanged.emit(index, index)

                return True

        return False


    def stripCommas(self):

        for row in range(len(self.table)):

            for column in  range(len(self.table[0])):

                value = self.table[row][column]
                print(self.table)
                self.table[row][column] = value.replace('.', ',')
                print(self.table)
                del value


    def headerData(self, section, orientation, role):
        """Sets the headers for both the rows and columns of the tableView

        Parameters
        ----------
        section: int
            The section number which the header should belong to. Sections
            refer to every 4th row in this particular case
        orientation: `Qt::Orientation`
            Refers to the Horizontal or Vertical orientation of the table.
            Vertical is a row header, horizontal is a column header
        role: `Qt::EditRole`
            The role for which Qt is to use in updating or setting the data

        Returns
        -------
        pixmap: `Qt::QPixmap`
            The DisplayRole or DecorationRole for Qt. Will also return a
            QPixmap if it's the money$ shot.

        """
        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:
                return self.headers[section]

        if role == Qt.DecorationRole:

            if orientation == Qt.Horizontal:
                return self.headers[section]

            # if orientation == Qt.Vertical:
            #
            #     # Use QPixmap objects to create colored boxes in row headers
            #     value = self.colors[section]
            #     pixmap = QPixmap(25, 25)
            #     pixmap.fill(QColor(value))
            #
            #     return pixmap


    def insertRows(self, position, rows, parent=QModelIndex()):
        """Insert a new row in the table

        Parameters
        ----------
        position: int
            The row number of the table
        rows: int
            The number of rows to add to the table (4 in this particular case,
            as we're only requiring four measurements)
        parent: QModelIndex
            The parent object of the method

        Returns
        ------
        None

        """
        self.beginInsertRows(parent, position, position + rows - 1)

        # Default to empty cells
        for i in range(rows):

            defaultValues = [
                '' for i in range(self.columnCount(None))]

            self.table.insert(position, defaultValues)

        self.endInsertRows()


    def removeRows(self, position, rows, parent=QModelIndex()):
        """Remove rows from the table

        Parameters
        ----------
        position: int
            The starting row from which the table deletion is to initialize
        rows: int
            The number of rows to be deleted from the mesa. Once again, four
            rows at a time
        parent: QModelIndex
            The QModelIndex parent that defines the parent of this fine method

        Returns
        ------
        None

        """
        nRows = len(self.table) - rows

        self.beginRemoveRows(parent, position, position + rows - 1)

        self.table = self.table[:nRows]

        self.endRemoveRows()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion") #Changed the style to prevent "PyQt5: Gtk-CRITICAL error"
    model = PalettedTableModel(tableData_reportWindow, headers_reportWindow)

    tableView = QTableView()
    tableView.setModel(model)

    tableView.show()
    print('headers: {}'.format(headers_reportWindow))
    print('rowcount: {}'.format(rowCount_reportWindow))
    # for row in range(0, rowCount_reportWindow, 4):
    for row in range(0, rowCount_reportWindow):
        for col in columns_reportWindow:
            # tableView.setSpan(row, col, 4, 1)
            tableView.setSpan(row, col, 1, 1)
    input()
    model.insertRows(rowCount_reportWindow, 4)

    sys.exit(app.exec_())
