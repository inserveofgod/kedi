from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction


class Actions:
    def __init__(self, controller):
        self.controller = controller
        self.model = self.controller.model

        self.manage_add = QAction(self.model.add_icon, "Ekle")
        self.manage_del = QAction(self.model.del_icon, "Sil")
        self.manage_edit = QAction(self.model.edit_icon, "Düzenle")
        self.manage_refresh = QAction(self.model.refresh_icon, "Yenile")
        self.manage_cat = QAction(self.model.icon, "Kedi")
        self.manage_find = QAction(self.model.find_icon, "Bul")
        self.manage_exit = QAction(self.model.exit_icon, "Çık")

        self.view_full = QAction(self.model.full_icon, "Tam Ekran")
        self.view_menu = QAction(self.model.menu_icon, "Menü Göster/Gizle")
        self.view_toolbar = QAction(self.model.toolbar_icon, "Araç Çubuğu Göster/Gizle")
        self.view_dark = QAction(self.model.dark_icon, "Gece görünümü")

        self.help_help = QAction(self.model.help_icon, "Yardım")
        self.help_about = QAction(self.model.about_icon, "Hakkında")

        self.disable()
        self._checks()
        self._triggers()

    def disable(self):
        self.manage_del.setEnabled(False)
        self.manage_edit.setEnabled(False)
        self.manage_find.setEnabled(False)

    def enable(self):
        self.manage_del.setEnabled(True)
        self.manage_edit.setEnabled(True)
        self.manage_find.setEnabled(True)

    def shortcuts(self):
        self.manage_add.setShortcut(QKeySequence("Ctrl+N"))
        self.manage_del.setShortcut(QKeySequence("Del"))
        self.manage_edit.setShortcut(QKeySequence("Ctrl+E"))
        self.manage_find.setShortcut(QKeySequence("Return"))
        self.manage_refresh.setShortcut(QKeySequence("Ctrl+R"))
        self.manage_cat.setShortcut(QKeySequence("Ctrl+K"))
        self.manage_exit.setShortcut(QKeySequence("Alt+F4"))

        self.view_full.setShortcut(QKeySequence("F11"))
        self.view_menu.setShortcut(QKeySequence("Ctrl+Shift+M"))
        self.view_toolbar.setShortcut(QKeySequence("Ctrl+Shift+T"))
        self.view_dark.setShortcut(QKeySequence("Ctrl+Shift+D"))

        self.help_help.setShortcut(QKeySequence("Ctrl+H"))
        self.help_about.setShortcut(QKeySequence("Ctrl+Shift+O"))

    def _checks(self):
        self.view_full.setCheckable(True)
        self.view_full.setChecked(False)

        self.view_menu.setCheckable(True)
        self.view_menu.setChecked(True)

        self.view_toolbar.setCheckable(True)
        self.view_toolbar.setChecked(True)

        self.view_dark.setCheckable(True)
        self.view_dark.setChecked(False)

    def _triggers(self):
        self.manage_add.triggered.connect(self.controller.action_manage_add)
        self.manage_del.triggered.connect(self.controller.action_manage_del)
        self.manage_edit.triggered.connect(self.controller.action_manage_edit)
        self.manage_refresh.triggered.connect(self.controller.reload_tables)
        self.manage_cat.triggered.connect(self.controller.action_run_cat)
        self.manage_find.triggered.connect(self.controller.action_manage_find)
        self.manage_exit.triggered.connect(self.controller.action_manage_exit)

        self.view_full.triggered.connect(self.controller.action_view_full)
        self.view_menu.triggered.connect(self.controller.action_view_menu)
        self.view_toolbar.triggered.connect(self.controller.action_view_toolbar)
        self.view_dark.triggered.connect(self.controller.action_view_dark)

        self.help_help.triggered.connect(self.controller.action_help_help)
        self.help_about.triggered.connect(self.controller.action_help_about)
