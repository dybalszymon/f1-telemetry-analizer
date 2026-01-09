from creation.ReportFactory import ReportFactory
from logic.Strategies import ConsistencyScoreStrategy
from logic.TelemetryComposite import TelemetryComposite
from logic.Strategies import TelemetryComparisonStrategy
from process.GlobalRankingReport import GlobalRankingReport
from process.HeadToHeadReport import HeadToHeadReport
from presentation.CliRenderer import CliRenderer


class RaceReportFactory(ReportFactory):
    def create_ranking_report(self, session_key: int):
        strategy = ConsistencyScoreStrategy()
        return GlobalRankingReport(session_key, strategy)

    def create_comparison_report(self, session_key: int, driver1: int, driver2: int):
        # ✅ Używamy TelemetryComposite zamiast ConsistencyScoreStrategy
        composite = TelemetryComposite()
        composite.add(TelemetryComparisonStrategy(data_type="speed", label="Prędkość", unit="km/h"))
        composite.add(TelemetryComparisonStrategy(data_type="rpm", label="Obroty", unit="RPM"))
        
        renderer = CliRenderer()
        return HeadToHeadReport(session_key, driver1, driver2, composite, renderer)
