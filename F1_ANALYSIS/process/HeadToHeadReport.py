from process.RaceReportTemplate import RaceReportTemplate

from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface

from typing import override


class HeadToHeadReport(RaceReportTemplate):

    def __init__(self, strategy : AnalysisStrategyInterface, data_facade: F1DataFacade, driver1 : str, driver2: str):
        super().__init__(strategy, data_facade)
        self.driver1 = driver1
        self.driver2 = driver2

    @override
    def _fetch_data(self):
        pass
