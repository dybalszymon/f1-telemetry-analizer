from F1_ANALYSIS.logic.AnalysisStrategyInterface import AnalysisStrategyInterface


class TelemetryComposite(AnalysisStrategyInterface):
    def __init__(self):
        self.strategies = []

    def add(self, strategy: AnalysisStrategyInterface):
        self.strategies.append(strategy)

    def calculate(self, data: dict) -> list:
        """
        Iteruje po wszystkich dodanych strategiach (Speed, RPM, Throttle)
        i zwraca listę gotową dla MultiPlotRenderer.
        """
        # data to {"driver1": [...], "driver2": [...]}

        full_report_data = []

        for strategy in self.strategies:
            # Każda strategia zwraca jeden słownik wykresu
            plot_data = strategy.calculate(data)
            full_report_data.append(plot_data)

        return full_report_data

    def get_name(self) -> str:
        return "Pełna Telemetria"