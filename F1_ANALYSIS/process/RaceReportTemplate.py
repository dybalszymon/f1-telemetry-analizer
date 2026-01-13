from abc import ABC, abstractmethod
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from data.F1DataFacade import F1DataFacade
# from presentation.ReportRenderer import ReportRenderer
# from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
# from data.F1DataFacade import F1DataFacade

from abc import ABC, abstractmethod
from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface


class RaceReportTemplate(ABC):

    def __init__(self, session_key: int, strategy, facade, renderer=None):
        self.session_key = session_key
        self.strategy = strategy
        self.facade = facade
        self.renderer = renderer
        self.raw_data = None

    def generate_report(self):
        self._fetch_data()
        self.display_output()
        # self.process_data()
        #
        #
        # if self.renderer:
        #     self.renderer.render(self.strategy.get_name(), self.result)
        # else:
        #     self.display_output()

    @abstractmethod
    def _fetch_data(self):
        pass

    def process_data(self):
        if self.raw_data:
            self.result = self.strategy.calculate(self.raw_data)

    @abstractmethod
    def display_output(self):
        pass
    