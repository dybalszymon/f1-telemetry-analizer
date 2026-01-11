from abc import ABC, abstractmethod
from process.RaceReportTemplate import RaceReportTemplate

class ReportFactory(ABC):
    @abstractmethod
    def create_ranking_report(self, session_key: int) -> RaceReportTemplate:
        pass

    @abstractmethod
    def create_comparison_report(self, session_key: int, driver1: int, driver2: int) -> RaceReportTemplate:
        pass
    
    @abstractmethod
    def create_tyre_degradation_report(self, session_key: int, driver_number: int) -> RaceReportTemplate:
        pass