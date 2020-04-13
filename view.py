import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import re

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        self.labels = ['ID', 'DATE', 'VALUE', 'LAST']
        self.sample_data = ['Cell', 'Fish', 'Apple', 'Bananas', 'Mango']
        self.layout = QVBoxLayout(self)

        self.model = QStandardItemModel(5, 4)
        self.set_model()

        self.filter_proxy_model = SortFilterProxyModel()
        self.filter_proxy_model.setColumns(len(self.labels))
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.filter_layout = QHBoxLayout()

        self.combobox = QComboBox()
        self.combobox.currentTextChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.combobox.addItems([''] + self.sample_data)
        self.filter_layout.addWidget(self.combobox)

        self.lineedit = QLineEdit()
        self.lineedit.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.filter_layout.addWidget(self.lineedit)

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setModel(self.filter_proxy_model)
        self.table.clicked.connect(self.click)

        
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.table)
    
    def set_model(self):
        self.model.setHorizontalHeaderLabels(self.labels)
        for row, text in enumerate(self.sample_data):
            self.model.setItem(row, 0, QStandardItem(text))
            self.model.setItem(row, 1, QStandardItem("Sunaina_" + text))
            self.model.setItem(row, 2, QStandardItem("Joshil_" + text))
            self.model.setItem(row, 3, QStandardItem("Test_" + text))

    def click(self):
        indexes = self.table.selectionModel().selectedIndexes()
        data = [index.sibling(index.row(), index.column()).data() for index in indexes]
        print(data)
        return data

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super(SortFilterProxyModel, self).__init__()
        self.role = Qt.DisplayRole
        self.columns = 0

    def setColumns(self, columns):
        self.columns = columns

    def filterAcceptsRow(self, row, parent):
        for index in self._get_indexes(row, parent):
            value = self.sourceModel().data(index, self.role)
            if self.filterRegExp().indexIn(str(value)) >= 0:
                return True
        return False

    def _get_indexes(self, row, parent):
        for col in range(self.columns):
            yield self.sourceModel().index(row, col, parent)

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())