from RaceReportTemplate import RaceReportTemplate

from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategy

from typing import Override


class HeadToHeadReport(RaceReportTemplate):

    def __init__(self, strategy : AnalysisStrategy, data_facade: F1DataFacade):
        super().__init__(strategy, data_facade)

    def _display_output(self, analyzed_data):
        pass

    @Override
    def _fetch_data(self):
        return super()._fetch_data()
