# app/controllers/agreement_controller.py
from app.views.table_view import TableView
from PySide6.QtWidgets import QMessageBox
from app.views.dialogs.record_dialog import RecordDialog

class AgreementController:
    def __init__(self, db, agreement_id):
        self.view = TableView()
        self.db = db
        self.agreement_id = agreement_id
        self.view.setWindowTitle(f"Договор ID: {agreement_id}")
        self._setup_ui()
        self._connect_signals()
        self.load_agreement_info()

    def _setup_ui(self):
        self.view.search_input.hide()
        self.view.search_button.hide()
        self.view.scrollArea_2.hide()
        self.view.add_button.setText("Редактировать")
        self.view.delete_button.hide()
        self.view.add_button.hide()

    def _connect_signals(self):
        self.view.back_button.clicked.connect(self.view.close)
        self.view.edit_button.clicked.connect(lambda: self.edit_agreement(self.agreement_id))

    def load_agreement_info(self):
        query = """
            SELECT id,date,sign FROM agreement WHERE id = %s
        """
        result = self.db.execute_query(query, (self.agreement_id,))
        if result:
            headers = ["ID", "Дата", "Подпись"]
            self.view.setup_table(self.view.main_table, headers, result)

    def edit_agreement(self, agreement_id):
        from app.views.dialogs.record_dialog import RecordDialog
        dialog = RecordDialog("agreement", self.db, agreement_id)
        if dialog.exec():
            self.load_agreement_info()