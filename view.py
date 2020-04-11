import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        self.model = QStandardItemModel(5, 3)
        self.model.setHorizontalHeaderLabels(['ID', 'DATE', 'VALUE'])
        for row, text in enumerate(['Cell', 'Fish', 'Apple', 'Ananas', 'Mango']):
            item = QStandardItem(text)
            self.model.setItem(row, 2, item)

        # filter proxy model
        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterKeyColumn(2) # third column

        # line edit for filtering
        self.lineedit = QLineEdit()
        self.lineedit.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.layout.addWidget(self.lineedit)

        # table view
        self.table = QTableView()
        self.table.setModel(self.filter_proxy_model)
        self.layout.addWidget(self.table)


if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())