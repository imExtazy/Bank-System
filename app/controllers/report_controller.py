# app/controllers/report_controller.py
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QMessageBox,
                               QFileDialog, QSpacerItem, QSizePolicy, QWidget)
from app.views.table_view import TableView
import pandas as pd


class ReportController:
    def __init__(self, db):
        self.db = db
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        """Настройка интерфейса отчетов"""
        # Инициализация с учетом прав администратора
        current_user = self.db.connection.get_dsn_parameters().get('user')
        self.view = TableView(is_admin=current_user == 'nikolay')
        self.view.setWindowTitle("Отчет по клиентам")

        # Автоматическое скрытие кнопок через TableView
        self.view.table_name = "client_info_v"  # Активируем режим отчета

        # Настройка кнопки "Назад"
        self.view.back_button.setText("Закрыть")
        self.view.back_button.clicked.connect(self.view.close)

        # Создаем панель инструментов отчета
        self._create_report_toolbar()

    def _create_report_toolbar(self):
        """Создает панель инструментов для отчетов"""
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # Кнопка экспорта
        self.export_btn = QPushButton("📊 Экспорт в Excel")
        self.export_btn.setStyleSheet("""
            QPushButton {
                padding: 5px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.export_btn.clicked.connect(self.export_to_excel)
        toolbar_layout.addWidget(self.export_btn)

        # Кнопка печати
        self.print_btn = QPushButton("🖨 Печать")
        self.print_btn.setStyleSheet("padding: 5px;")
        self.print_btn.clicked.connect(self._print_report)
        toolbar_layout.addWidget(self.print_btn)

        # Гибкое пространство
        toolbar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Добавляем панель в интерфейс
        if hasattr(self.view, 'gridLayout'):
            self.view.gridLayout.addWidget(toolbar, 0, 0, 1, 2)
        else:
            self.view.horizontalLayout.insertWidget(0, toolbar)

    def load_data(self):
        """Загрузка данных с обработкой ошибок"""
        try:
            data = self.db.execute_query("""
                SELECT 
                    full_name as "ФИО",
                    passport as "Паспорт", 
                    phone as "Телефон",
                    CASE WHEN sign THEN 'Да' ELSE 'Нет' END as "Подпись",
                    balance as "Баланс",
                    CASE WHEN debt IS NOT NULL THEN 'Есть' ELSE 'Нет' END as "Долг"
                FROM client_info_v
            """)

            if data:
                self.view.setup_table(
                    self.view.main_table,
                    ["ФИО", "Паспорт", "Телефон", "Подпись", "Баланс", "Долг"],
                    data
                )
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def export_to_excel(self):
        """Улучшенный экспорт с проверкой данных"""
        try:
            data = self.db.execute_query("SELECT * FROM client_info_v")
            if not data:
                raise ValueError("Нет данных для экспорта")

            df = pd.DataFrame(data, columns=[
                "ФИО", "Паспорт", "Телефон",
                "Наличие подписи", "Баланс", "Задолженность"
            ])

            file_path = self._get_save_path()
            if file_path:
                df.to_excel(file_path, index=False, engine='openpyxl')
                self._show_success_message(file_path)

        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Ошибка экспорта",
                f"Произошла ошибка:\n{str(e)}"
            )

    def _get_save_path(self):
        """Диалог сохранения файла"""
        return QFileDialog.getSaveFileName(
            self.view,
            "Сохранить отчет",
            "клиенты_отчет.xlsx",
            "Excel Files (*.xlsx)"
        )[0]  # Возвращаем только путь

    def _show_success_message(self, path):
        """Показывает сообщение об успешном экспорте"""
        QMessageBox.information(
            self.view,
            "Экспорт завершен",
            f"Отчет успешно сохранен:\n{path}",
            QMessageBox.Ok
        )

    def _print_report(self):
        """Заглушка для будущей реализации печати"""
        QMessageBox.information(
            self.view,
            "Печать отчета",
            "Функция печати находится в разработке",
            QMessageBox.Ok
        )