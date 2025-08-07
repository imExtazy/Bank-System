import pandas as pd
from fpdf import FPDF
from pathlib import Path
from .models import *


class ReportGenerator:
    @staticmethod
    def create_transaction_report(stats: List[TransactionStats], output_path: str):
        """PDF отчет по транзакциям"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Заголовок
        pdf.cell(200, 10, txt="Аналитический отчет по транзакциям", ln=1, align='C')

        # Таблица данных
        df = pd.DataFrame([s.__dict__ for s in stats])
        pdf.multi_cell(0, 10, txt=df.to_string(index=False))

        # Сохранение
        pdf.output(output_path)

    @staticmethod
    def create_client_segment_report(segments: List[ClientSegment]):
        """HTML отчет по сегментации клиентов"""
        df = pd.DataFrame([s.__dict__ for s in segments])
        html = f"""
        <html>
            <body>
                <h2>Сегментация клиентов</h2>
                {df.to_html(index=False)}
            </body>
        </html>
        """
        return html

    @staticmethod
    def save_credit_analysis(results: List[CreditAnalysis], db_connection):
        """Сохранение кредитного анализа в БД"""
        df = pd.DataFrame([r.__dict__ for r in results])
        df.to_sql('credit_scores', db_connection, if_exists='replace')