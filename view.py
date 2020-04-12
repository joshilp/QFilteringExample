import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import re

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        self.model = QStandardItemModel(5, 4)
        labels = ['ID', 'DATE', 'VALUE', 'LAST']
        self.model.setHorizontalHeaderLabels(labels)
        for row, text in enumerate(['Cell', 'Fish', 'Apple', 'Bananas', 'Mango']):
            self.model.setItem(row, 0, QStandardItem(text))
            self.model.setItem(row, 1, QStandardItem("Sunaina_" + text))
            self.model.setItem(row, 2, QStandardItem("Joshil_" + text))
            self.model.setItem(row, 3, QStandardItem("Test_" + text))

        # self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model = SortFilterProxyModel()
        self.filter_proxy_model.setColumns(len(labels))
        
        self.filter_proxy_model.setSourceModel(self.model)
        # self.filter_proxy_model.setFilterKeyColumn(2) # third column

        self.lineedit = QLineEdit()
        self.lineedit.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.layout.addWidget(self.lineedit)

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setModel(self.filter_proxy_model)
        self.layout.addWidget(self.table)

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super(SortFilterProxyModel, self).__init__()
        self.role = Qt.DisplayRole

    def setColumns(self, columns):
        self.columns = columns

    def filterAcceptsRow(self, row, parent):
        for index in self._get_indexes(row, parent):
            value = self.sourceModel().data(index, self.role)
            print(self.filterRegExp())
            if self.filterRegExp().indexIn(str(value)) >= 0:
                return True
        return False

    def _get_indexes(self, row, parent):
        for col in range(self.columns):
            yield self.sourceModel().index(row, col, parent)

    # def _get_indexes2(self, row, parent):
    #     index0 = self.sourceModel().index(row, 0, parent)
    #     index1 = self.sourceModel().index(row, 1, parent)
    #     index2 = self.sourceModel().index(row, 2, parent)
    #     index3 = self.sourceModel().index(row, 3, parent)
    #     return [index0, index1, index2, index3]

if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())