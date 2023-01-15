import sys

from PyQt5.QtWidgets import QApplication

from controllers.mainController import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainController = MainController()
    mainController.main()
    mainController.reload_tables()

    app.exec()
