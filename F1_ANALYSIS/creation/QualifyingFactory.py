from abc import ABC, abstractmethod

from ReportFactory import *

class QualifyingReportFactory(ReportFactory):
    def create_ranking_report(self) -> RankingReport:
        return QualifyingRankingReport()

    def create_comparison_report(self) -> ComparisonReport:
        return QualifyingComparisonReport()
