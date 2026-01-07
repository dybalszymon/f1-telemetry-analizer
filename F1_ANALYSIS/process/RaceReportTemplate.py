from abc import ABC, abstractmethod

from presentation.ReportRenderer import ReportRenderer
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from data.F1DataFacade import F1DataFacade

class RaceReportTemplate(ABC):
    def __init__(self, session_key: int, strategy: AnalysisStrategyInterface):
        self.session_key = session_key
        self.strategy = strategy
        self.facade = F1DataFacade()
        self.raw_data = None
        self.result = None

    def generate_report(self):
        self.fetch_data()
        if self.raw_data:
            self.process_data()
            self.display_output()
        else:
            print("Data download error")

    @abstractmethod #every report chose what to download from facadee
    def _fetch_data(self):
        pass
    
    def _process_data(self, data):
        self.result = self.strategy.calculate(self.raw_data)

    @abstractmethod
    def display_output(self):
        pass
    