from F1_ANALYSIS.creation.ReportFactory import ReportFactory
from F1_ANALYSIS.process.GlobalRankingReport import GlobalRankingReport
from F1_ANALYSIS.process.HeadToHeadReport import HeadToHeadReport
from F1_ANALYSIS.logic.Strategies import FastestLapStrategy, TelemetryComparisonStrategy
from F1_ANALYSIS.logic.TelemetryComposite import TelemetryComposite
from F1_ANALYSIS.presentation.PlotRenderer import PlotRenderer

class QualifyingFactory(ReportFactory):
    #TODO np lista najlepszych czasów zawodników w kwalach
    def create_ranking_report(self, session_key: int):
        strategy = FastestLapStrategy()
        return GlobalRankingReport(session_key, strategy)

    def create_comparison_report(self, session_key: int, driver1: int, driver2: int):
        pass


    def create_telemetry_comparison(self, session_key: int, driver1: int, driver2: int):
        """
        Tworzy raport porównawczy z 4 wykresami na jednym ekranie.
        """

        composite = TelemetryComposite()


        composite.add(TelemetryComparisonStrategy(data_type="speed", label="Prędkość", unit="km/h"))
        composite.add(TelemetryComparisonStrategy(data_type="rpm", label="Obroty Silnika", unit="RPM"))
        composite.add(TelemetryComparisonStrategy(data_type="throttle", label="Gaz", unit="%"))
        composite.add(TelemetryComparisonStrategy(data_type="brake", label="Hamulec", unit="0/1"))


        renderer = PlotRenderer()


        return HeadToHeadReport(session_key, driver1, driver2, composite, renderer)