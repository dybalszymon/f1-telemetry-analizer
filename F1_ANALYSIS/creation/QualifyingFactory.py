from creation.ReportFactory import ReportFactory
from process.GlobalRankingReport import GlobalRankingReport
from process.HeadToHeadReport import HeadToHeadReport
from logic.Strategies import FastestLapStrategy, TelemetryComparisonStrategy
from logic.TelemetryComposite import TelemetryComposite
from presentation.PlotRenderer import UniversalTelemetryRenderer

from data.F1DataFacade import F1DataFacade

from F1_ANALYSIS.presentation.StreamlitRenderer import StreamlitRenderer


class QualifyingFactory(ReportFactory):
    def create_ranking_report(self, session_key: int):
        strategy = FastestLapStrategy()
        facade = F1DataFacade()
        renderer = StreamlitRenderer()
        return GlobalRankingReport(session_key, strategy, facade, renderer)

    def create_comparison_report(self, session_key: int, driver1: int, driver2: int):
        composite = TelemetryComposite()
        #composite.add(TelemetryComparisonStrategy(data_type="track_map", label="Mapa Prędkości (Delta)", unit=""))
        composite.add(TelemetryComparisonStrategy(data_type="speed", label="Prędkość", unit="km/h"))
        composite.add(TelemetryComparisonStrategy(data_type="speed_delta", label="Delta Prędkości", unit="km/h"))
        composite.add(TelemetryComparisonStrategy(data_type="rpm", label="Obroty Silnika", unit="RPM"))
        composite.add(TelemetryComparisonStrategy(data_type="throttle", label="Gaz", unit="%"))
        composite.add(TelemetryComparisonStrategy(data_type="brake", label="Hamulec", unit="0/1"))
        composite.add(TelemetryComparisonStrategy(data_type="n_gear", label="Bieg", unit="#", plot_style="step"))
        composite.add(TelemetryComparisonStrategy(data_type="drs", label="DRS", unit="Signal", plot_style="step"))
        renderer = UniversalTelemetryRenderer()
        facade = F1DataFacade()
        return HeadToHeadReport(session_key, driver1, driver2, composite, facade, renderer)

    
