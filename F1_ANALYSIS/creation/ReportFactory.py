from abc import ABC, abstractmethod

from process.RaceReportTemplate import RaceReportTemplate

class ReportFactory(ABC):
    @abstractmethod
    def create_ranking_report(self) -> RaceReportTemplate:
        pass

    @abstractmethod
    def create_comparison_report(self) -> RaceReportTemplate:
        pass