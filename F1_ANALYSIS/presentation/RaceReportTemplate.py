from abc import ABC, abstractmethod

from logic.AnalysisStrategyInterface import AnalysisStrategy
from data.F1DataFacade import F1DataFacade

class RaceReportTemplate(ABC):
    def __init__(self, strategy: AnalysisStrategy, data_facade: F1DataFacade):
        self.data_facade = data_facade
        self.strategy = strategy

    def generate_report(self):
        data = self._fetch_data()
        analyzed_data = self._process_data(data)
        self._display_output(analyzed_data)

    def _fetch_data(self):
        return self.data_facade.get_telemetry_data()
    
    def _process_data(self, data):
        return self.strategy.calculate()
    
    @abstractmethod
    def _display_output(self, analyzed_data):
        pass
