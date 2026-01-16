from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from logic.TelemetryProcessor import TelemetryProcessor
import pandas as pd


class TelemetryComposite(AnalysisStrategyInterface):
    def __init__(self):
        self.strategies = []

    def add(self, strategy: AnalysisStrategyInterface):
        self.strategies.append(strategy)

    @property
    def has_delta_strategy(self):
        """Sprawdza, czy którakolwiek strategia wymaga obliczania delty"""
        return any(s.data_type in ['speed_delta', 'track_map'] for s in self.strategies)

    def calculate(self, data: dict) -> dict:
        """
        Główna metoda przetwarzająca.
        Przyjmuje surowe dane, wykonuje obliczenia (jeśli potrzebne) i zwraca wzbogacone dane.
        """
        # 1. Jeśli nie ma potrzeby liczenia delty, zwracamy dane bez zmian
        if not self.has_delta_strategy:
            return data

        # 2. Jeśli potrzebna jest delta, używamy Processora
        d1 = data['driver1']
        d2 = data['driver2']

        # Konwertujemy na DataFrame, żeby Processor mógł działać
        df1 = pd.DataFrame(d1['telemetry'])
        df2 = pd.DataFrame(d2['telemetry'])

        # Wywołujemy TelemetryProcessor (nasze narzędzie matematyczne)
        time_axis, speed_delta = TelemetryProcessor.calculate_delta(df1, df2, 'speed')

        # 3. Wzbogacamy dane o wyniki analizy
        if 'analysis' not in data:
            data['analysis'] = {}

        data['analysis']['speed_delta'] = {
            'time': time_axis,
            'value': speed_delta
        }

        return data

    def get_name(self) -> str:
        return "Analiza Telemetrii"