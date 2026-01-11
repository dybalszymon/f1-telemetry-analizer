from abc import ABC, abstractmethod
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from data.F1DataFacade import F1DataFacade

from abc import ABC, abstractmethod
from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface

from presentation.StreamlitRenderer import StreamlitRenderer

from process.RaceReportTemplate import RaceReportTemplate

class TyreDegradationRaceReport(RaceReportTemplate):
    def __init__(self, session_key: int, driver_number: int ,strategy: AnalysisStrategyInterface, renderer = StreamlitRenderer()):
        super().__init__(session_key, strategy, renderer)
        self.driver_number = driver_number
    
    def _fetch_data(self):
        self.raw_data = self.facade.get_laps_race(self.session_key, self.driver_number)

    def get_name(self):
        return "Race Tyre Degradation Report"