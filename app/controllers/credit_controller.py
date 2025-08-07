# # app/controllers/credit_controller.py
# from PySide6.QtWidgets import QTableWidgetItem
# from PySide6.QtCore import Qt
# from PySide6.QtWidgets import QWidget, QVBoxLayout
# from PySide6.QtWidgets import QLabel
# from app.views.table_view import TableView
#
#
# class CreditController:
#     def __init__(self, db, client_id):
#         self.db = db
#         self.client_id = client_id
#         self.view = TableView(is_admin=True)  # Всегда в режиме админа для этого окна
#         self.view.setWindowTitle(f"Кредиты клиента ID: {client_id}")
#         self._setup_ui()
#         self.load_data()
#
#     def _setup_ui(self):
#         """Настраиваем интерфейс окна кредитов"""
#         # Скрываем ненужные элементы
#         self.view.search_input.hide()
#         self.view.search_button.hide()
#         self.view.add_button.hide()
#         self.view.delete_button.hide()
#         self.view.edit_button.hide()
#         self.view.back_button.hide()
#         self.view.add_credit_button.hide()
#
#         # Создаем заголовки для таблиц
#         loan_label = QLabel("Кредиты")
#         loan_label.setAlignment(Qt.AlignCenter)
#         loan_label.setStyleSheet("font-weight: bold; font-size: 14px;")
#
#         debt_label = QLabel("Долги")
#         debt_label.setAlignment(Qt.AlignCenter)
#         debt_label.setStyleSheet("font-weight: bold; font-size: 14px;")
#
#         # Создаем контейнеры с заголовками
#         loan_container = QWidget()
#         loan_layout = QVBoxLayout()
#         loan_layout.addWidget(QLabel("Кредиты", alignment=Qt.AlignCenter))
#         loan_layout.addWidget(self.view.main_table)
#         loan_container.setLayout(loan_layout)
#
#         debt_container = QWidget()
#         debt_layout = QVBoxLayout()
#         debt_layout.addWidget(QLabel("Долги", alignment=Qt.AlignCenter))
#         debt_layout.addWidget(self.view.branch_table)
#         debt_container.setLayout(debt_layout)
#
#         # Устанавливаем новые контейнеры в scrollArea
#         self.view.scrollArea.setWidget(loan_container)
#         self.view.scrollArea_2.setWidget(debt_container)
#
#         # Настройка таблиц
#         self.view.main_table.setHorizontalHeaderLabels(["ID", "Сумма", "Ставка", "Срок", "Дата выдачи"])
#         self.view.branch_table.setHorizontalHeaderLabels(["ID", "ID Клиента", "ID Кредита", "Сумма долга", "Дата"])
#     def load_data(self):
#         """Загружает данные о кредитах и долгах"""
#         # Загрузка кредитов
#         loan_query = "SELECT id, amount, interest_rate, period, created_at FROM loan WHERE client_id = %s"
#         loans = self.db.execute_query(loan_query, (self.client_id,))
#
#         if loans:
#             self.view.setup_table(self.view.main_table, ["ID", "Сумма", "Ставка", "Срок", "Дата выдачи"], loans)
#
#         # Загрузка долгов
#         debtor_query = """
#         SELECT d.id, d.client_id, d.loan_id, d.debt, d.created_at
#         FROM debtor d
#         WHERE d.client_id = %s
#         """
#         debts = self.db.execute_query(debtor_query, (self.client_id,))
#
#         if debts:
#             self.view.setup_table(self.view.branch_table, ["ID", "ID Клиента", "ID Кредита", "Сумма долга", "Дата"],
#                                   debts)