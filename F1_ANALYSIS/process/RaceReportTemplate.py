from abc import ABC, abstractmethod

from presentation.ReportRenderer import ReportRenderer
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from data.F1DataFacade import F1DataFacade

class RaceReportTemplate(ABC):
    def __init__(self, strategy: AnalysisStrategyInterface, data_facade: F1DataFacade, renderer: ReportRenderer):
        self.data_facade = data_facade
        self.strategy = strategy
        self.renderer = renderer

    def generate_report(self):
        data = self._fetch_data()
        analyzed_data = self._process_data(data)
        self.renderer.render(analyzed_data)

    def _fetch_data(self):
        return self.data_facade.get_telemetry_data()
    
    def _process_data(self, data):
        return self.strategy.calculate()
    