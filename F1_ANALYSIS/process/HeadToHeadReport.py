from process.RaceReportTemplate import RaceReportTemplate

from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface

from typing import override


from F1_ANALYSIS.process.RaceReportTemplate import RaceReportTemplate

class HeadToHeadReport(RaceReportTemplate):
    def __init__(self, session_key, driver1, driver2, strategy, renderer):
        super().__init__(session_key, strategy, renderer)
        self.driver1 = driver1
        self.driver2 = driver2

    def fetch_data(self):
        
        self.raw_data = {
            "driver1": {
                "name": str(self.driver1),
                "telemetry": self.facade.get_car_telemetry(self.session_key, self.driver1)
            },
            "driver2": {
                "name": str(self.driver2),
                "telemetry": self.facade.get_car_telemetry(self.session_key, self.driver2)
            }
        }