import sys
from PySide6.QtWidgets import QApplication
from app.controllers.auth_controller import AuthController


def main():
    app = QApplication(sys.argv)

    controller = AuthController()
    controller.run()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()