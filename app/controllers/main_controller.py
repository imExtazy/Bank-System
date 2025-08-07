from app.database import DatabaseManager
from app.controllers.table_controller import TableController


class MainController:
    def __init__(self, db):
        from app.views.main_view import MainView
        self.view = MainView()
        self.db = db
        self._connect_signals()

    def _connect_signals(self):
        self.view.bank_button.clicked.connect(lambda: self.open_table("bank","name"))
        self.view.branch_button.clicked.connect(lambda: self.open_table("branch","name"))
        self.view.client_button.clicked.connect(lambda: self.open_table("client","full_name"))
        self.view.customer_button.clicked.connect(lambda: self.open_table("customer","full_name"))
        self.view.account_button.clicked.connect(lambda: self.open_table("account","id"))
        self.view.agreement_button.clicked.connect(lambda: self.open_table("agreement","id"))
        self.view.loan_button.clicked.connect(lambda: self.open_table("loan", "id"))
        self.view.debtor_button.clicked.connect(lambda: self.open_table("debtor", "id"))
        self.view.report_button.clicked.connect(lambda: self.open_table("client_info_v", "ФИО"))

        self.view.back_button.clicked.connect(self.back_to_auth)
        self.view.exit_button.clicked.connect(self.view.close)

    def open_table(self, table_name,column):
        self.table_controller = TableController(self.db, table_name,column, self)
        self.table_controller.view.show()
        self.view.hide()

    def back_to_auth(self):
        from app.controllers.auth_controller import AuthController  # Ленивый импорт
        self.auth_controller = AuthController()
        self.auth_controller.run()
        self.view.close()

    def generate_report(self):
        from app.controllers.report_controller import ReportController
        self.report_controller = ReportController(self.db)
        self.report_controller.view.show()