from PySide6.QtWidgets import QMessageBox

from app.controllers import main_controller
from app.views.table_view import TableView
from app.views.dialogs.record_dialog import RecordDialog

COLUMN_ALIASES = {
    "id": "ID",
    "full_name": "ФИО",
    "passport": "Паспорт",
    "phone": "Телефон",
    "name": "Название",
    "address": "Адрес",
    "date": "Дата",
    "sign": "Подпись",
    "post": "Должность",
    "debt": "Задолженность",
    "period": "Срок",
    "interest_rate": "Ставка",
    "created_at": "Создано",
    "bank_id": "ID Банка",
    "birthday": "Дата рождения"
}
class TableController:
    def __init__(self, db, table_name,column, main_controller=None):
        current_user = db.connection.get_dsn_parameters().get('user')
        is_admin = current_user == 'nikolay'

        self.view = TableView(is_admin=is_admin)
        self.db = db
        self.table_name = table_name
        self.view.table_name = table_name
        self.view.setWindowTitle(f"Таблица: {table_name}")
        self.column = column
        self.main_controller = main_controller

        self._connect_signals()
        self.load_data()
        self.search_data()
        if table_name == "bank":
            self.view.main_table.itemSelectionChanged.connect(self.load_branches)
        elif table_name == "client":
            self.view.main_table.itemSelectionChanged.connect(self.load_client_details)
            self.view.client_double_clicked.connect(self.open_client_details_window)
            self.view.add_credit_button.show()
            self.view.add_credit_requested.connect(self.open_debtor_table)
            #self.view.add_credit_requested.clicked.connect(self.open_debtor_table)
            #self.view.add_credit_clicked.connect(self.open_credit_window)
        elif table_name == "customer":
            self.view.main_table.itemSelectionChanged.connect(self.load_customer_details)
            self.view.agreement_double_clicked.connect(self.open_agreement_window)
        elif table_name == "client_info_v":
            self.view.add_button.hide()
            self.view.edit_button.hide()
            self.view.delete_button.hide()
            self.view.scrollArea_2.hide()
            self.view.branch_table.hide()
        else:
            self.view.scrollArea_2.hide()
            self.view.branch_table.hide()


    def _connect_signals(self):
        self.view.search_button.clicked.connect(self.search_data)
        self.view.add_button.clicked.connect(self.add_record)
        self.view.delete_button.clicked.connect(self.delete_record)
        self.view.edit_button.clicked.connect(self.edit_record)
        self.view.back_button.clicked.connect(self.back_to_menu)

    def open_debtor_table(self):
        if self.main_controller:
            self.main_controller.open_table("debtor", "id")
        else:
            QMessageBox.warning(self.view, "Ошибка", "Не удалось открыть таблицу должников")

    def _check_admin_access(self):
        """Проверяет права администратора"""
        current_user = self.db.connection.get_dsn_parameters().get('user')
        if current_user != 'nikolay':
            QMessageBox.warning(self.view, "Ошибка", "Недостаточно прав для выполнения операции")
            return False
        return True

    def load_data(self):
        query = f"SELECT * FROM {self.table_name} LIMIT 100"
        result = self.db.execute_query(query)

        if result is not None:  # Проверяем, что результат не None
            # query_columns = """
            # SELECT column_name
            # FROM information_schema.columns
            # WHERE table_name = %s
            # ORDER BY ordinal_position
            # """
            # columns = self.db.execute_query(query_columns, (self.table_name,))
            columns = self._get_table_columns()
            if columns:
                if self.table_name == 'bank':
                    headers = ['ID','Название','Адрес']
                    self.view.update_table_data(self.view.main_table, headers, result)
                    if self.view.main_table.rowCount() > 0:
                        self.view.main_table.setCurrentCell(0, 0)
                else:
                    headers = self._get_table_columns()
                    self.view.update_table_data(self.view.main_table,headers, result)
                    if self.view.main_table.rowCount() > 0:
                        self.view.main_table.setCurrentCell(0, 0)

    def _get_table_columns(self, table_name=None):
        """Получение списка столбцов таблицы"""
        table = table_name if table_name else self.table_name
        query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = %s 
        ORDER BY ordinal_position
        """
        # return self.db.execute_query(query, (table,))
        columns = self.db.execute_query(query, (table,))
        if not columns:
            return []

        if table_name == 'branch':
            print(columns)
        return [COLUMN_ALIASES.get(col[0], col[0]) for col in columns]

    def load_branches(self):
        """Загрузка филиалов для выбранного банка"""
        if self.table_name != "bank":
            return
        selected = self.view.main_table.currentRow()
        if selected >= 0:
            bank_id = self.view.main_table.item(selected, 0).text()

            query = "SELECT name,address FROM branch WHERE bank_id = %s"
            branches = self.db.execute_query(query, (bank_id,))

            if branches is not None:
                headers = ['Название', 'Адрес']
                self.view.update_table_data(self.view.branch_table, headers, branches)

    def load_client_details(self):
        """Загрузка детальной информации о клиенте"""
        selected = self.view.main_table.currentRow()
        if selected >= 0:
            client_id = self.view.main_table.item(selected, 0).text()
            #self.view.add_credit_clicked.emit(client_id)
            full_name = self.view.main_table.item(selected, 1).text()

            query = """
                SELECT
                    ag.id AS "№ Договора", 
                    CASE WHEN ag.sign THEN 'Присутствует' ELSE 'Отсутствует' END AS "Наличие подписи",
                    COALESCE(ac.balance, 0) AS "Баланс",
                    CASE WHEN d.debt IS NOT NULL THEN 'Имеется' ELSE 'Нет' END AS "Задолженность"
                FROM client c
                LEFT JOIN agreement ag ON c.id = ag.client_id
                LEFT JOIN account ac ON ag.id = ac.agreement_id
                LEFT JOIN debtor d ON c.id = d.client_id
                WHERE c.full_name = %s
            """
            details = self.db.execute_query(query, (full_name,))

            if details is not None and len(details) > 0:
                headers = ["№ Договора","Наличие подписи", "Баланс", "Задолженность"]

                self.view.update_table_data(self.view.branch_table, headers, details)

                self.view.branch_table.resizeColumnsToContents()

    def load_customer_details(self):
        """Загрузка детальной информации о клиенте через agreement"""
        if self.table_name != "customer":
            return

        selected = self.view.main_table.currentRow()
        if selected >= 0:
            customer_id = self.view.main_table.item(selected, 0).text()

            query = """
                SELECT 
                    a.id AS agreement_id,
                    c.full_name,
                    a.date
                FROM agreement a
                JOIN client c ON a.client_id = c.id
                WHERE a.customer_id = %s
            """
            result = self.db.execute_query(query, (customer_id,))

            if result and len(result) > 0:
                headers = ["№ договора", "ФИО клиента", "Дата договора"]
                self.view.update_table_data(self.view.branch_table, headers, result)
                self.view.branch_table.resizeColumnsToContents()
            else:
                # Очистите таблицу, если данных нет
                self.view.update_table_data(self.view.branch_table, [], [])

    def open_branch_window(self, bank_id):
        """Открывает новое окно с филиалами банка"""
        from app.controllers.branch_controller import BranchController
        self.branch_controller = BranchController(self.db, bank_id)
        self.branch_controller.view.show()

    def search_data(self):
        search_text = self.view.search_input.text()
        if not search_text:
            self.load_data()
            return

        query = """
        SELECT * FROM {}
        WHERE {} ILIKE %s
        """.format(self.table_name,self.column)

        # result = self.db.execute_query(query, (search_text,))
        result = self.db.execute_query(query, (f"%{search_text}%",))
        if result is not None:  # Проверяем, что результат не None
            query_columns = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s 
            ORDER BY ordinal_position
            """
            columns = self.db.execute_query(query_columns, (self.table_name,))
            if columns:
                headers = [col[0] for col in columns]
                self.view.update_table_data(self.view.main_table,headers, result)
                # Выбираем первую строку после поиска
                if self.view.main_table.rowCount() > 0:
                    self.view.main_table.setCurrentCell(0, 0)


    def add_record(self):
        dialog = RecordDialog(self.table_name, self.db)
        if dialog.exec():
            self.load_data()

    def delete_record(self):
        selected = self.view.main_table.currentRow()
        if selected >= 0:
            id_item = self.view.main_table.item(selected, 0)
            if id_item:
                query = f"DELETE FROM {self.table_name} WHERE id = %s"
                if self.db.execute_query(query, (id_item.text(),)):
                    self.load_data()

    def edit_record(self):
        selected = self.view.main_table.currentRow()
        if selected >= 0:
            id_item = self.view.main_table.item(selected, 0)
            if id_item:
                dialog = RecordDialog(self.table_name, self.db, id_item.text())
                if dialog.exec():
                    self.load_data()

    def back_to_menu(self):
        """Возврат в главное меню"""
        # Закрываем текущее окно
        self.view.close()

        # Создаем и показываем главное меню
        from app.controllers.main_controller import MainController
        self.main_controller = MainController(self.db)
        self.main_controller.view.show()

    def open_client_details_window(self, client_id):
        from app.controllers.client_controller import ClientDetailsWindow
        self.details_window = ClientDetailsWindow(self.db, client_id)
        self.details_window.view.show()

    def open_agreement_window(self, agreement_id):
        """Открывает форму договора"""
        from app.controllers.agreement_controller import AgreementController
        self.agreement_controller = AgreementController(self.db, agreement_id)
        self.agreement_controller.view.show()

    def open_credit_window(self, client_id):
        """
        Открывает диалог добавления кредита/должника
        """
        from app.views.dialogs.record_dialog import RecordDialog

        # Создаем новую запись в debtor
        insert_query = """
            INSERT INTO debtor (client_id, debt) VALUES (%s, 0) RETURNING id
        """
        result = self.db.execute_query(insert_query, (client_id,))
        if not result:
            QMessageBox.critical(self.view, "Ошибка", "Не удалось создать должника")
            return

        debtor_id = result[0][0]

        # Теперь открываем договор (agreement) или кредит (loan)
        dialog = RecordDialog("loan", self.db)

        # Предзаполнение поля client_id в диалоге (если ваш RecordDialog это поддерживает)
        dialog.set_field_value("debtor_id", debtor_id)

        if dialog.exec():
            QMessageBox.information(self.view, "Успех", "Кредит успешно добавлен")