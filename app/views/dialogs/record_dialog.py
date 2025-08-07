from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
import re
from PySide6.QtWidgets import QMessageBox

class RecordDialog(QDialog):
    def __init__(self, table_name, db, record_id=None):
        super().__init__()
        self.table_name = table_name
        self.db = db
        self.record_id = record_id
        self.setWindowTitle("Добавить запись" if not record_id else "Редактировать запись")

        self.fields = []
        self.inputs = []

        self.init_ui()
        self.load_data()

    def init_ui(self):
        query = """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position
        """
        result = self.db.execute_query(query, (self.table_name,))

        if not result:
            return

        layout = QFormLayout()

        for col in result[1:]:  # Skip ID
            self.fields.append(col[0])
            input_field = QLineEdit()
            self.inputs.append(input_field)
            layout.addRow(col[0], input_field)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def load_data(self):
        if not self.record_id:
            return

        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        result = self.db.execute_query(query, (self.record_id,))

        if result and len(result) == 1:
            for i, value in enumerate(result[0][1:]):  # Skip ID
                self.inputs[i].setText(str(value))


    def accept(self):
        """Вызывается при нажатии OK — проверяет данные перед сохранением"""
        values = {}
        for field, input_widget in zip(self.fields, self.inputs):
            values[field] = input_widget.text().strip()

        if self.table_name == "client":
            phone = values.get("phone")
            if phone:
                phone_pattern = r'^[+]?[\d\-()\s]{7,}$'
                if not re.match(phone_pattern, phone):
                    QMessageBox.warning(
                        self,
                        "Ошибка ввода",
                        "Некорректный формат номера телефона.\nПример: +7-950-123-45-67"
                    )
                    return

        elif self.table_name == "agreement":
            date_str = values.get("date")
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'  # YYYY-MM-DD
                if not re.match(date_pattern, date_str):
                    QMessageBox.warning(
                        self,
                        "Ошибка ввода",
                        "Некорректный формат даты.\nИспользуйте формат: YYYY-MM-DD"
                    )
                    return

        elif self.table_name == "account":
            balance = values.get("balance")
            if balance:
                try:
                    float(balance)
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Ошибка ввода",
                        "Поле 'Баланс' должно быть числом"
                    )
                    return

        elif self.table_name == "debtor":
            debt = values.get("debt")
            if debt:
                try:
                    float(debt)
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Ошибка ввода",
                        "Поле 'Задолженность' должно быть числом"
                    )
                    return

        if self.record_id:
            set_clause = ", ".join([f"{field} = %s" for field in self.fields])
            query = f"""
            UPDATE {self.table_name}
            SET {set_clause}
            WHERE id = %s
            """
            params = [input.text() for input in self.inputs] + [self.record_id]
        else:
            columns = ", ".join(self.fields)
            values_placeholders = ", ".join(["%s"] * len(self.fields))
            query = f"""
            INSERT INTO {self.table_name} ({columns})
            VALUES ({values_placeholders})
            """
            params = [input.text() for input in self.inputs]

        if self.db.execute_query(query, params):
            super().accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить данные в базу")