from PyQt5 import QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super(MainWindow, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        # calculate center of the screen

        self.screen_width = self.screen().geometry().width()
        self.screen_height = self.screen().geometry().height()
        self.default_width = self.screen_width // 2
        self.default_height = self.screen_height // 2

    def main(self):
        self.statusBar().showMessage("Yüz Tespit uygulamasına hoşgeldiniz.")
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setWindowTitle(self.model.title)
        self.setGeometry((self.screen_width - self.default_width) // 2, (self.screen_height - self.default_height) // 2,
                         self.default_width, self.default_height)
        self.setWindowIcon(self.model.icon)
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.controller.action_manage_exit():
            a0.accept()
            return None

        a0.ignore()
