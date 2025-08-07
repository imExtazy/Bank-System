import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


class AnalyticsEngine:
    @staticmethod
    def plot_transactions(data, save_path=None):
        """Визуализация транзакций"""
        df = pd.DataFrame(data)
        df['period'] = pd.to_datetime(df['period'])

        fig, ax = plt.subplots(figsize=(12, 6))
        df.plot(x='period', y='total', ax=ax, kind='bar')
        ax.set_title('Динамика транзакций')

        if save_path:
            plt.savefig(save_path)
        return fig


def generate_analytics_report(report_type, data):
    """Генерация отчетов разных типов"""
    engine = AnalyticsEngine()

    if report_type == 'transactions':
        return engine.plot_transactions(data['transactions'])

    elif report_type == 'clients':
        df = pd.DataFrame(data['clients'])
        # ... обработка для клиентов ...

    return None