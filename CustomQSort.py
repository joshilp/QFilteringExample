class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, data, parent=None):
        super(SortFilterProxyModel, self).__init__(parent)
        self.role = Qt.DisplayRole
        self.minDate = QDate()
        self.maxDate = QDate()
        self.__data = data

    def setFilterMinimumDate(self, date):
        self.minDate = date
        self.invalidateFilter()

    def filterMinimumDate(self):
        return self.minDate

    def setFilterMaximumDate(self, date):
        self.maxDate = date
        self.invalidateFilter()

    def filterMaximumDate(self):
        return self.maxDate

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
        index1 = self.sourceModel().index(sourceRow, 1, sourceParent)
        index2 = self.sourceModel().index(sourceRow, 2, sourceParent)
        value = self.sourceModel().data(index0, self.role) 
        for ix in (index0, index1, index2):
            value = self.sourceModel().data(ix, self.role)
            if self.filterRegExp().indexIn(str(value)) >= 0:
                return True
        return False

    def lessThan(self, left, right):
        leftData = self.sourceModel().data(left, self.role)
        rightData = self.sourceModel().data(right, self.role)

        if not isinstance(leftData, QDate):
            emailPattern = QRegExp("([\\w\\.]*@[\\w\\.]*)")

            if left.column() == 1 and emailPattern.indexIn(leftData) != -1:
                leftData = emailPattern.cap(1)

            if right.column() == 1 and emailPattern.indexIn(rightData) != -1:
                rightData = emailPattern.cap(1)

        return leftData < rightData

    def dateInRange(self, date):
        if isinstance(date, QDateTime):
            date = date.date()

        return ((not self.minDate.isValid() or date >= self.minDate)
                and (not self.maxDate.isValid() or date <= self.maxDate))