from abc import ABC, abstractmethod
# from logic.Strategies import TyreDegradationStrategy, ConsistencyScoreStrategy
# from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
#
# from presentation.CliRenderer import CliRenderer
# from presentation.PdfRenderer import PdfRenderer
# from presentation.PlotRenderer import PlotRenderer
# from presentation.ReportRenderer import ReportRenderer
#
# from process.GlobalRankingReport import GlobalRankingReport
# from process.HeadToHeadReport import HeadToHeadReport
# from data.F1DataFacade import F1DataFacade
# from creation.ReportFactory import *

from F1_ANALYSIS.creation.ReportFactory import ReportFactory


class RaceReportFactory(ReportFactory):
    #TODO np lista czasów w kwalifikacjach
    def create_ranking_report(self, renderer: ReportRenderer) -> RaceReportTemplate:

        strategy = ConsistencyScoreStrategy()
        facade = F1DataFacade()

        return GlobalRankingReport(strategy, facade, renderer)

    def create_comparison_report(self, driver1: str, driver2: str, renderer: ReportRenderer) -> RaceReportTemplate:
        """
        Tworzy raport porównawczy.
        Fabryka decyduje o STRATEGII (ConsistencyScoreStrategy).
        Użytkownik decyduje o RENDERERZE (przekazanym w argumencie).
        """
        # 1. Fabryka wybiera logikę biznesową (Strategię)
        strategy = ConsistencyScoreStrategy()

        # 2. Tworzymy fasadę
        facade = F1DataFacade()

        # 3. Składamy wszystko w całość
        # Renderer jest tylko przekazywany dalej ("pass-through")
        return HeadToHeadReport(strategy, facade, renderer, driver1, driver2)