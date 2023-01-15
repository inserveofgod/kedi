from PyQt5.QtWidgets import QMenu

from views.Actions import Actions


class Menus(Actions):
    def __init__(self, controller):
        super(Menus, self).__init__(controller)
        self.controller = controller
        self.win = self.controller.mainWindow

        self.manage = QMenu("Yö&net")
        self.view = QMenu("&Görünüm")
        self.help = QMenu("&Yardım")

        self._actions()
        self.shortcuts()

    def _actions(self):
        manage_actions = [self.manage_add, self.manage_del, self.manage_edit, self.manage_find, self.manage_refresh,
                          self.manage_cat, self.manage_exit]
        view_actions = [self.view_full, self.view_menu, self.view_toolbar, self.view_dark]
        help_actions = [self.help_help, self.help_about]

        for manage_action in manage_actions:
            self.manage.addAction(manage_action)

        for view_action in view_actions:
            self.view.addAction(view_action)

        for help_action in help_actions:
            self.help.addAction(help_action)

    def main(self):
        menubar = self.win.menuBar()
        menubar.addMenu(self.manage)
        menubar.addMenu(self.view)
        menubar.addMenu(self.help)