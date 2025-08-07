from PySide6.QtWidgets import QMessageBox
from app.database import DatabaseManager
from app.views.auth_view import AuthView
from app.controllers.main_controller import MainController


class AuthController:
    def __init__(self):
        self.view = AuthView()
        self.db = DatabaseManager()
        self._connect_signals()

    def _connect_signals(self):
        self.view.login_button.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.view.login_input.text()
        password = self.view.password_input.text()

        if self.db.connect(username, password):
            self.main_controller = MainController(self.db)
            self.main_controller.view.show()
            self.view.hide()
        else:
            self.view.show_error("Неверный логин или пароль")

    def run(self):
        self.view.show()