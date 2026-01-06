from process.RaceReportTemplate import RaceReportTemplate

from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface

from presentation.ReportRenderer import ReportRenderer

from typing import override

class GlobalRankingReport(RaceReportTemplate):

    def __init__(self, strategy : AnalysisStrategyInterface, data_facade: F1DataFacade, renderer: ReportRenderer):
        super().__init__(strategy, data_facade, renderer)

    @override
    def _fetch_data(self):
        pass