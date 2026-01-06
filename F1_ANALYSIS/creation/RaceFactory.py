from abc import ABC, abstractmethod

from ReportFactory import *

class RaceRankingReport(RankingReport):
    def generate(self):
        pass

class RaceComparisonReport(ComparisonReport):
    def generate(self):
        pass

class RaceReportFactory(ReportFactory):
    def create_ranking_report(self) -> RankingReport:
        return RaceRankingReport()

    def create_comparison_report(self) -> ComparisonReport:
        return RaceComparisonReport()
    