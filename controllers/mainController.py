from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QMessageBox

from model.model import Model
from views.AddingDialog import AddingDialog
from views.MainWindow import MainWindow
from views.Menus import Menus
from views.Table import Table
from views.Toolbar import Toolbar


# todo : test program one more
# todo : append stylesheets in order to make program darken or lighten


class MainController:
    def __init__(self):
        # model
        self.model = Model()

        # views
        self.mainWindow = MainWindow(self)
        self.menus = Menus(self)
        self.toolBar = Toolbar(self)
        self.table = Table(self)

        self.addingDialog = AddingDialog(self)

    # starters

    def main(self):
        self.mainWindow.main()
        self.menus.main()
        self.toolBar.main()
        self.table.main()

        self.mainWindow.setCentralWidget(self.table)

    # table loaders

    def remove_data(self):
        self.table.tableModel.setRowCount(0)

    def append_data(self, data: tuple):
        table_model = self.table.model()
        table_model.insertRow(0)

        for i in range(len(data)):
            table_model.setData(table_model.index(0, i), data[i])

    def reload_tables(self):
        cursor = self.model.conn.cursor()
        cursor.execute(self.model.main_sql)
        data = cursor.fetchall()

        self.remove_data()

        # load data into tables
        for datum in data:
            self.append_data(datum)

    # sql listeners

    def add_person(self):
        row_id = self.model.selected_id
        dialog = self.addingDialog
        name, surname, phone = [ui.text() for ui in dialog.uis]

        if row_id is None:
            sql = "INSERT INTO people(id, name, surname, phone) VALUES(?, ?, ?, ?)"
            self.mainWindow.statusBar().showMessage("Veri eklendi")

        else:
            sql = "UPDATE people " \
                  "SET id = ?, name = ?, surname = ?, phone = ? " \
                  f"WHERE id = {row_id}"
            self.mainWindow.statusBar().showMessage("Veri düzenlendi")

        row = (row_id, name, surname, phone)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        dialog.close()
        self.reload_tables()

        # save into datasets

        # fill the blanks with '-'
        calling = self.model.format_calling(name, surname)
        self.model.add_datasets(calling, dialog.files)

        # train the uploaded images

        self.model.prepare_train()
        self.model.train_images()
        self.model.save_trained_names()

    # table listeners

    def selected(self):
        table_model = self.table.model()
        indexes = self.table.selectedIndexes()

        if indexes:
            self.model.selected_row = indexes[0].row()
            self.model.selected_id = table_model.data(table_model.index(self.model.selected_row, 0))

            self.menus.enable()
            self.toolBar.enable()

    # listeners

    def action_run_cat(self) -> None:
        if not self.model.cat_running:
            print("[+] Cat is running...")

            # get trained images and names and run the face detector
            self.model.trained_images()
            self.model.trained_names()
            self.model.run_face_detector()
            self.model.cat_running = True

    def action_manage_add(self) -> None:
        self.model.deselect()
        self.menus.disable()
        self.toolBar.disable()

        dialog = self.addingDialog
        dialog.refactor()
        dialog.show()

    def action_manage_edit(self) -> None:
        if self.model.is_selected():
            dialog = self.addingDialog
            sql = f"SELECT name, surname, phone FROM people WHERE id={self.model.selected_id};"

            cursor = self.model.conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()

            for i in range(len(data)):
                dialog.uis[i].setText(data[i])

            dialog.btn_submit.setText("Düzenle")
            dialog.show()

    def action_manage_del(self) -> None:
        if self.model.is_selected():
            confirm = QMessageBox.question(self.mainWindow, self.mainWindow.windowTitle(),
                                           "Bu satırı silmek istediğinize emin misiniz?\n"
                                           f"id={self.model.selected_id}")

            if confirm == QMessageBox.Yes:
                sql = f"DELETE FROM people WHERE id={self.model.selected_id}"
                cursor = self.model.conn.cursor()

                try:
                    cursor.execute(sql)
                    self.model.conn.commit()

                except Exception as exc:
                    QMessageBox.critical(self.mainWindow, self.mainWindow.windowTitle(), "Veri silinemedi!\n"
                                                                                         f"Hata : {str(exc)}")
                    self.mainWindow.statusBar().showMessage("Veri silinemedi")

                else:
                    self.model.deselect()
                    self.menus.disable()
                    self.toolBar.disable()
                    self.reload_tables()
                    self.mainWindow.statusBar().showMessage("Veri silindi")

    def action_manage_find(self) -> None:
        searched_text = self.toolBar.findingField.text()
        found = False

        if searched_text != '':
            rows = self.table.tableModel.rowCount()
            cols = self.table.tableModel.columnCount()

            for row in range(rows):
                for col in range(cols):
                    index = self.table.model().index(row, col)
                    item = self.table.tableModel.data(index)

                    if searched_text in str(item):
                        self.table.selectionModel().clearSelection()
                        self.table.selectionModel().select(index, QItemSelectionModel.Rows | QItemSelectionModel.Select)
                        found = True
                        break

            if not found:
                QMessageBox.warning(self.mainWindow, self.model.title, "Listede böyle bir bilgi yok!")

    def action_manage_exit(self) -> bool:
        ask = QMessageBox.question(self.mainWindow, self.model.title, "Uygulamadan çıkmak istediğinize emin misiniz?",
                                   QMessageBox.Yes | QMessageBox.No)
        return True if ask == QMessageBox.Yes else False

    def action_view_full(self) -> None:
        if self.mainWindow.isFullScreen():
            self.mainWindow.showNormal()

        else:
            self.mainWindow.showFullScreen()

    def action_view_menu(self) -> None:
        menubar = self.mainWindow.menuBar()
        menubar.setVisible(False if menubar.isVisible() else True)

    def action_view_toolbar(self) -> None:
        toolbar = self.toolBar.toolbar
        toolbar.setVisible(False if toolbar.isVisible() else True)

    def action_view_dark(self) -> None:
        if self.model.config.get('dark'):
            self.model.update("dark", False)

        else:
            self.model.update("dark", True)

        stylesheets = self.model.read_stylesheets()

        if stylesheets is not None:
            print(stylesheets)

    def action_help_help(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Program hakkında yardım için\ninserveofgod@gmail.com adresine mail gönderebilirsiniz",
                                QMessageBox.Ok)

    def action_help_about(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Bu program Python programalama dili ile PyQt5\n"
                                "kütüphanesi kullanılarak yapılmıştır.",
                                QMessageBox.Ok)
