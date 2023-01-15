from PyQt5.Qt import QSize
from PyQt5.QtWidgets import QToolBar, QLineEdit

from views.Actions import Actions


class Toolbar(Actions):
    def __init__(self, controller):
        super(Toolbar, self).__init__(controller)

        self.controller = controller
        self.win = self.controller.mainWindow
        self.findingField = QLineEdit()
        self.toolbar = QToolBar()

        self._actions()

    def _actions(self):
        self.toolbar.addAction(self.manage_add)
        self.toolbar.addAction(self.manage_edit)
        self.toolbar.addAction(self.manage_del)
        self.toolbar.addAction(self.manage_refresh)
        self.toolbar.addAction(self.manage_cat)
        self.toolbar.addWidget(self.findingField)
        self.toolbar.addAction(self.manage_find)

    def main(self):
        self.toolbar.setMovable(False)

        self.findingField.setMaximumWidth(200)
        self.findingField.setPlaceholderText("Aratmak için buraya yazın...")

        self.toolbar.setIconSize(QSize(16, 16))
        self.win.addToolBar(self.toolbar)
