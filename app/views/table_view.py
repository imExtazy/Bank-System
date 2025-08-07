from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from app.ui_compiled.ui_table_form import Ui_TableForm
from PySide6.QtCore import Signal


class TableView(QMainWindow, Ui_TableForm):
    bank_double_clicked = Signal(str)
    client_double_clicked = Signal(str)
    agreement_double_clicked = Signal(str)
    add_credit_requested = Signal(str)
    def __init__(self, is_admin=False):
        super().__init__()
        self.setupUi(self)


        self.search_input = self.lineEdit
        self.search_button = self.pushButton
        self.add_button = self.pushButton_2
        self.delete_button = self.pushButton_3
        self.edit_button = self.pushButton_4
        self.back_button = self.pushButton_5

        # Новая кнопка "Внести кредит"
        self.add_credit_button = self.pushButton_6  # Предполагаем, что это pushButton_6 в UI
        self.add_credit_button.setText("Внести кредит")
        self.add_credit_button.hide()  # По умолчанию скрыта
        self.add_credit_button.clicked.connect(self._emit_add_credit_request)


        #self.table = QTableWidget()
        #self.scrollArea.setWidget(self.table)
        # Основная таблица (банки)
        self.main_table = QTableWidget()
        self.scrollArea.setWidget(self.main_table)
        # Подключаем двойной клик
        self.main_table.doubleClicked.connect(self._on_double_click)

        # Дополнительная таблица для филиалов
        self.branch_table = QTableWidget()
        self.scrollArea_2.setWidget(self.branch_table)
        self.branch_table.doubleClicked.connect(self._on_agreement_double_click)

        if not is_admin:
            self._set_readonly_mode()

        # Настройка внешнего вида таблиц
        self.setup_tables_style()
        self.table_name = None

    def setup_tables_style(self):
        """Настройка стилей и поведения таблиц"""
        # Для основной таблицы
        self.main_table.setAlternatingRowColors(True)
        self.main_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Для таблицы филиалов
        self.branch_table.setAlternatingRowColors(True)
        self.branch_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Установка минимальных размеров
        self.branch_table.setMinimumWidth(400)
    def setup_table(self,table, headers, data):
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                table.setItem(row_idx, col_idx, item)
        table.resizeColumnsToContents()

    def update_table_data(self, table, headers, data):
        """Обновляет данные таблицы без замены модели"""
        table.clearContents()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()

    def _on_double_click(self, index):
        """Обработчик двойного клика по таблице"""
        if index.isValid():
            item = self.main_table.item(index.row(), 0)
            if item is not None:
                if self.table_name == "bank":
                    bank_id = item.text()
                    self.bank_double_clicked.emit(bank_id)
                elif self.table_name == "client":
                    client_id = item.text()
                    self.client_double_clicked.emit(client_id)

    def _on_agreement_double_click(self, index):
        if index.isValid():
            item = self.branch_table.item(index.row(), 0)
            if item:
                self.agreement_double_clicked.emit(item.text())

    def _set_readonly_mode(self):
        """Скрывает кнопки редактирования для режима чтения"""
        self.add_button.hide()
        self.delete_button.hide()
        self.edit_button.hide()
        self.setWindowTitle(f"{self.windowTitle()} (Режим просмотра)")

    # def add_credit_clicked(self):
    #     selected_row = self.main_table.currentRow()
    #     if selected_row >= 0:
    #         client_id = self.main_table.item(selected_row, 0).text()
    #         self.add_credit_clicked.emit(client_id)


    def _emit_add_credit_request(self):
        """Эмитирует сигнал при нажатии кнопки добавления кредита"""
        selected_row = self.main_table.currentRow()
        if selected_row >= 0:
            client_id = self.main_table.item(selected_row, 0).text()
            self.add_credit_requested.emit(client_id)
