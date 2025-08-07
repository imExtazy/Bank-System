# app/controllers/client_details_window.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from app.views.table_view import TableView


class ClientDetailsWindow:
    def __init__(self, db, client_id):
        self.db = db
        self.view = TableView()
        self.view.table_name = "client_details"  # Устанавливаем имя таблицы
        self.view.setWindowTitle(f"Детальная информация о клиенте ID: {client_id}")
        self._setup_ui()
        self.load_data(client_id)

        self.view.back_button.clicked.connect(self.view.close)

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.view.search_input.hide()
        self.view.search_button.hide()
        self.view.add_button.hide()
        self.view.delete_button.hide()
        self.view.edit_button.hide()
        self.view.scrollArea_2.hide()
        self.view.back_button.show()

        self.view.main_table.setColumnCount(4)
        self.view.main_table.setRowCount(1)
        self.view.main_table.setHorizontalHeaderLabels(["Сумма кредита", "Период", "Ставка", "Дата выдачи"])

    def load_data(self, client_id):
        query = """
            SELECT d.debt, l.period, l.interest_rate, l.created_at
            FROM debtor d
            JOIN loan l ON d.loan_id = l.id
            WHERE d.client_id = %s
        """
        result = self.db.execute_query(query, (client_id,))
        if result and len(result) > 0:
            row = result[0]
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.view.main_table.setItem(0, col_idx, item)