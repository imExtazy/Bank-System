import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtWidgets import QSizePolicy
from .models import *


class AnalyticsCanvas(FigureCanvasQTAgg):
    """Базовый класс для визуализаций в PySide"""

    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class TransactionVisualizer(AnalyticsCanvas):
    def __init__(self, stats: List[TransactionStats]):
        super().__init__()
        self.plot_transactions(stats)

    def plot_transactions(self, stats):
        periods = [s.period.strftime('%Y-%m') for s in stats]
        amounts = [s.total_amount for s in stats]

        sns.barplot(x=periods, y=amounts, ax=self.ax, palette='Blues_d')
        self.ax.set_title('Динамика транзакций по месяцам')
        self.ax.set_ylabel('Сумма операций')
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.tight_layout()


class ClientSegmentVisualizer(AnalyticsCanvas):
    def __init__(self, segments: List[ClientSegment]):
        super().__init__()
        self.plot_segments(segments)

    def plot_segments(self, segments):
        labels = [s.segment for s in segments]
        sizes = [s.client_count for s in segments]

        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
        self.ax.set_title('Сегментация клиентской базы')
        self.ax.axis('equal')


class CreditRiskVisualizer(AnalyticsCanvas):
    def __init__(self, credits: List[CreditAnalysis]):
        super().__init__()
        self.plot_risk_distribution(credits)

    def plot_risk_distribution(self, credits):
        risks = [c.risk_category for c in credits]
        sns.countplot(x=risks, ax=self.ax, order=['Low', 'Medium', 'High'])
        self.ax.set_title('Распределение кредитных рисков')