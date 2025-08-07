from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.ui_compiled.ui_auth_form import Ui_AuthForm


class AuthView(QMainWindow, Ui_AuthForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Авторизация")

        self.login_input = self.lineEdit
        self.password_input = self.lineEdit_2
        self.login_button = self.pushButton

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)