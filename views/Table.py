from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeView, QAbstractItemView


class Table(QTreeView):
    def __init__(self, controller):
        super(Table, self).__init__()

        self.controller = controller
        self.titles = self.controller.model.table_titles
        self.tableModel = QStandardItemModel(0, len(self.titles))

    def main(self):
        for i in range(len(self.titles)):
            self.tableModel.setHeaderData(i, Qt.Horizontal, self.titles[i])

        self.setModel(self.tableModel)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.selectionModel().selectionChanged.connect(self.controller.selected)
