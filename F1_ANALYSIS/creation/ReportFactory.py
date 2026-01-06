from abc import ABC, abstractmethod

class RankingReport(ABC):
    @abstractmethod
    def generate():
        pass

class ComparisonReport(ABC):
    @abstractmethod
    def generate():
        pass

class ReportFactory(ABC):
    @abstractmethod
    def create_ranking_report(self) -> RankingReport:
        pass

    @abstractmethod
    def create_comparison_report(self) -> ComparisonReport:
        pass