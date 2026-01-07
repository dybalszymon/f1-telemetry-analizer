from abc import ABC, abstractmethod

from creation.ReportFactory import *

from F1_ANALYSIS.presentation.ReportRenderer import ReportRenderer
from F1_ANALYSIS.process.HeadToHeadReport import HeadToHeadReport
from F1_ANALYSIS.logic.Strategies import HeadToHeadStrategy
from F1_ANALYSIS.presentation.PlotRenderer import PlotRenderer


class QualifyingReportFactory(ReportFactory):
    def create_ranking_report(self) -> RaceReportTemplate:
        return RaceReportTemplate()

    def create_comparison_report(self, session_key: int, driver1: int, driver2: int):

        strategy = HeadToHeadStrategy()


        renderer = PlotRenderer()

        return HeadToHeadReport(session_key, driver1, driver2, strategy, renderer)