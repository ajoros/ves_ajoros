import sys

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap #QTableView
from PyQt5.QtWidgets import (QApplication, QTableView, QListView)

from tempData import columnCount, colors, headers, rowCount, tableData


class PaletteTableModel(QAbstractTableModel):

    def __init__(self, table=[[]], headers=[], colors=[], parent=None):

        QAbstractTableModel.__init__(self, parent)
        # super(self, colors).__init__(parent)

        self.__table = table
        self.__headers = headers
        self.__colors = colors


    def rowCount(self, parent):

        return len(self.__table)


    def columnCount(self, parent):

        return len(self.__table[0])


    def flags(self, index):

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def update(self, table):

        self.__table = table


    def data(self, index, role):
        """Store and control data for the Table model

        Args:
            self (class??): an instance of PaletteTableModel
            index (`::class::Qt.TableInex`??)
            role (qt class): role

        Returns:
            str: QtName

        """
        row = index.row()
        column = index.column() - 1

        # if column == 0:
        #     pass

        if role == Qt.EditRole:

            # if column == 0:
            #     return self.__colors[row][column]
            # else:
            return self.__table[row][column]

        if role == Qt.ToolTipRole:

            return 'Cell contents: {}'.format(
                self.__table[row][column])

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__table[row][column]

            return value

        # if role == Qt.DecorationRole:
        #     row = index.row()
        #     column = index.column()
        #     # if column == 0:
        #     #     # value = self.__colors[row][column]
        #     #     value = self.__colors[row][1]

        #     #     pixmap = QPixmap(26, 26)
        #     #     pixmap.fill(value)

        #     #     icon = QIcon(pixmap)

        #     #     return icon
        #     return ''


    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.EditRole:
            row = index.row()
            column = index.column()

            if isinstance(value, str):
                self.__table[row][column] = value
                self.dataChanged.emit(index, index)
                return True
            # color = QColor(value)

            # if color.isValid():
            #     if column == 0:
            #         self.__colors[row][column] = value
            #         self.dataChanged.emit(index, index)
            #         return True
            #     else:
            #         self.__colors[row][column] = color
            #         self.dataChanged.emit(index, index)
            #         return True
        return False


    def headerData(self, section, orientation, role):


        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:
                return self.__headers[section]

        if role == Qt.DecorationRole:

            if orientation == Qt.Horizontal:
                return self.__headers[section]

            if orientation == Qt.Vertical:

                # validSections = range(2, rowCount, 4)

                # try:
                    # index = colors.index(section)
                    # print(index)
                    # if column == 0:
                        # value = self.__colors[row][column]
                value = self.__colors[section]
                pixmap = QPixmap(25, 25)
                pixmap.fill(QColor(value))

                return pixmap
                # except:
                #     pixmap = QPixmap(26, 50)
                #     pixmap.fill(QColor(value))

                #     # icon = QIcon(pixmap)
                #     return pixmap
                # except:
                #     pixmap = QPixmap(0, 0)
                #     return pixmap

        # else:
        #     return QAbstractTableModel.headerData(
        #         self, section, orientation, role)


    def insertRows(self, position, rows, parent=QModelIndex()):

        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            defaultValues = [
                '' for i in range(self.columnCount(None))]

            self.__colors.insert(position, defaultValues)

        self.endInsertRows()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # import matplotlib.pyplot as plt
    # plt.style.use('bmh')
    # x = range(10)
    # y = range(11, 21)
    # for i in range(len(colors[::4])):
    #     z = [z + i for z in y]
    #     plt.plot(x, z, color=colors[::4][i])
    #     plt.plot(x, z[::-1], color=colors[::4][::-1][i])
    #     del z
    # plt.show()

    model = PaletteTableModel(tableData, headers, colors)

    tableView = QTableView()
    tableView.setModel(model)
    # print(dir(tableView))
    tableView.show()
    for row in range(0, rowCount - 1, 4):
        tableView.setSpan(row, 0, 4, 1)
        tableView.setSpan(row, 1, 4, 1)
        tableView.setSpan(row, 2, 4, 1)
        tableView.setSpan(row, 3, 4, 1)

    sys.exit(app.exec_())
