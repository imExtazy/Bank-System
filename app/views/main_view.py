from PySide6.QtWidgets import QMainWindow
from app.ui_compiled.ui_main_panel import Ui_MainPanel


class MainView(QMainWindow, Ui_MainPanel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("АИС Малый Банк")

        self.bank_button = self.pushButton
        self.branch_button = self.pushButton_2
        self.client_button = self.pushButton_3
        self.customer_button = self.pushButton_4
        self.account_button = self.pushButton_5
        self.agreement_button = self.pushButton_6
        self.loan_button = self.pushButton_7
        self.debtor_button = self.pushButton_8
        self.back_button = self.pushButton_9
        self.exit_button = self.pushButton_10
        self.report_button = self.pushButton_11