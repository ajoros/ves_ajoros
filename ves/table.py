import sys

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QTableView

from templates.tempData import (
    columnCount, columns, colors, headers, rowCount, tableData)


class PalettedTableModel(QAbstractTableModel):

    def __init__(self, table=[[]], headers=[], colors=[], parent=None):

        if parent is None:
            parent = self

        super(PalettedTableModel, self).__init__()

        QAbstractTableModel.__init__(self, parent)

        self.table = table
        self.headers = headers
        self.colors = colors



    def rowCount(self, parent):

        return len(self.table)


    def columnCount(self, parent):

        return len(self.table[0])


    def flags(self, index):

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def update(self, table):

        self.table = table


    def data(self, index, role):
        """Store and control data for the Table model

        Args:
            self (class??): an instance of PalettedTableModel
            index (`::class::Qt.TableInex`??)
            role (qt class): role

        Returns:
            str: QtName

        """
        row = index.row()
        column = index.column()

        if role == Qt.EditRole:

            return self.table[row][column]

        if role == Qt.ToolTipRole:

            return 'Cell contents: {}'.format(
                self.table[row][column])

        if role == Qt.DisplayRole:

            row = index.row()
            column = index.column()
            value = self.table[row][column]

            return value


    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.EditRole:
            row = index.row()
            column = index.column()

            if isinstance(value, str):
                self.table[row][column] = value
                self.dataChanged.emit(index, index)
                return True

        return False


    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:
                return self.headers[section]

        if role == Qt.DecorationRole:

            if orientation == Qt.Horizontal:
                return self.headers[section]

            if orientation == Qt.Vertical:

                value = self.colors[section]
                pixmap = QPixmap(25, 25)
                pixmap.fill(QColor(value))

                return pixmap


    def insertRows(self, position, rows, parent=QModelIndex()):

        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            defaultValues = [
                '' for i in range(self.columnCount(None))]

            self.table.insert(position, defaultValues)

        self.endInsertRows()


    def removeRows(self, position, rows, parent=QModelIndex()):

        nRows = len(self.table) - rows

        self.beginRemoveRows(parent, position, position + rows - 1)

        self.table = self.table[:nRows]

        self.endRemoveRows()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = PalettedTableModel(tableData, headers, colors)

    tableView = QTableView()
    tableView.setModel(model)

    tableView.show()

    for row in range(0, rowCount, 4):
        for col in columns:
            tableView.setSpan(row, col, 4, 1)
    input()
    model.insertRows(rowCount, 4)

    sys.exit(app.exec_())
