# database.py
import psycopg2
from psycopg2 import OperationalError, DatabaseError


class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self, user, password, dbname="postgres", host="localhost", port="5432"):
        """Подключение к базе данных"""
        try:
            self.connection = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                dbname=dbname
            )
            return True
        except OperationalError as e:
            print(f"Database connection error: {e}")
            return False

    def execute_query(self, query, params=None):
        """Выполнение SQL запроса"""
        if not self.connection:
            raise RuntimeError("Database connection is not established")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                self.connection.commit()
                return True
        except DatabaseError as e:
            print(f"Query execution error: {e}")
            self.connection.rollback()
            return False

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()

    def get_current_user(self):
        """Возвращает текущего пользователя БД"""
        if not self.connection:
            return None
        return self.connection.get_dsn_parameters().get('user')