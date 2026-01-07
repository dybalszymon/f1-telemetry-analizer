from abc import ABC, abstractmethod

from creation.ReportFactory import *

class QualifyingReportFactory(ReportFactory):
    def create_ranking_report(self) -> RaceReportTemplate:
        return RaceReportTemplate()

    def create_comparison_report(self) -> RaceReportTemplate:
        return RaceReportTemplate()
