import os.path

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QDialog, QPushButton, QFileDialog, QLabel


class AddingDialog(QDialog):
    def __init__(self, controller):
        super(AddingDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model
        self.formLayout = QFormLayout()
        self.files = []

        self.edit_name = QLineEdit()
        self.edit_surname = QLineEdit()
        self.edit_phone = QLineEdit()
        self.file_dialog = QFileDialog()
        self.btn_file = QPushButton()
        self.files_label = QLabel()
        self.btn_submit = QPushButton()

        self.uis = [self.edit_name, self.edit_surname, self.edit_phone]

        self._ui()

    def refactor(self):
        for ui in self.uis:
            ui.setText("")

    def select_file(self):
        files, _ = self.file_dialog.getOpenFileNames(self, "Dosya Seç", os.path.expanduser("~"),
                                                    "Photo Files (*.jpg *.png *.jpeg)")

        self.files.clear()
        self.files = files
        self.files_label.setText(str(len(self.files)))

    def _ui(self):
        self.setWindowTitle(self.model.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        self.files_label.setText("0")

        self.btn_file.setText("Dosya Seç")
        self.btn_file.clicked.connect(self.select_file)

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.add_person)

        self.edit_phone.setPlaceholderText("+00 000.(000).00.00")

        self.formLayout.addRow("İsim : ", self.edit_name)
        self.formLayout.addRow("Soyisim : ", self.edit_surname)
        self.formLayout.addRow("Telefon Numarası : ", self.edit_phone)
        self.formLayout.addRow("Resim Dosyaları : ", self.btn_file)
        self.formLayout.addRow("Seçili Dosyalar : ", self.files_label)
        self.formLayout.addWidget(self.btn_submit)
