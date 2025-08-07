from app.views.table_view import TableView
from PySide6.QtWidgets import QMessageBox


class BranchController:
    def __init__(self, db, bank_id):
        self.view = TableView()
        self.db = db
        self.bank_id = bank_id
        self.view.setWindowTitle(f"Филиалы банка ID: {bank_id}")

        # Настраиваем UI только для филиалов
        self._setup_ui_for_branches()
        self._connect_signals()
        self.load_branches()

    def _setup_ui_for_branches(self):
        """Скрываем ненужные элементы для окна филиалов"""
        self.view.search_input.hide()
        self.view.search_button.hide()
        self.view.add_button.hide()
        self.view.delete_button.hide()
        self.view.edit_button.hide()
        self.view.scrollArea_2.hide()  # Скрываем вторую таблицу

    def _connect_signals(self):
        """Подключаем только кнопку назад"""
        self.view.back_button.clicked.connect(self.view.close)

    # def load_branches(self):
    #     """Загрузка филиалов для выбранного банка"""
    #     query = "SELECT * FROM branch WHERE bank_id = %s"
    #     branches = self.db.execute_query(query, (self.bank_id,))
    #
    #     if branches is not None:
    #         branch_columns = self._get_table_columns("branch")
    #         if branch_columns:
    #             headers = [col[0] for col in branch_columns]
    #             self.view.setup_table(self.view.main_table, headers, branches)
    #
    # def _get_table_columns(self, table_name):
    #     """Получение списка столбцов таблицы"""
    #     query = """
    #     SELECT column_name
    #     FROM information_schema.columns
    #     WHERE table_name = %s
    #     ORDER BY ordinal_position
    #     """
    #     return self.db.execute_query(query, (table_name,))