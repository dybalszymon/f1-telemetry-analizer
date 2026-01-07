from abc import ABC, abstractmethod

from F1_ANALYSIS.creation.ReportFactory import ReportFactory
from F1_ANALYSIS.process.HeadToHeadReport import HeadToHeadReport
from F1_ANALYSIS.logic.TelemetryComposite import TelemetryComposite
from F1_ANALYSIS.logic.Strategies import TelemetryComparisonStrategy
from F1_ANALYSIS.presentation.PlotRenderer import PlotRenderer


class QualifyingReportFactory(ReportFactory):
    # def create_ranking_report(self) -> RaceReportTemplate:
    #     return RaceReportTemplate()

    def create_telemetry_comparison(self, session_key: int, driver1: int, driver2: int):
        """
        Tworzy raport porównawczy z 4 wykresami na jednym ekranie.
        Używa wzorca Composite do połączenia różnych strategii.
        """
        # 1. Tworzymy Kompozyt (Pusty worek na strategie)
        composite = TelemetryComposite()

        # 2. Wrzucamy do niego konkretne strategie (klocki)
        # Każda linijka to jeden wykres na finalnym obrazku!
        composite.add(TelemetryComparisonStrategy(data_type="speed", label="Prędkość", unit="km/h"))
        composite.add(TelemetryComparisonStrategy(data_type="rpm", label="Obroty Silnika", unit="RPM"))
        composite.add(TelemetryComparisonStrategy(data_type="throttle", label="Gaz", unit="%"))
        composite.add(TelemetryComparisonStrategy(data_type="brake", label="Hamulec", unit="0/1"))

        # 3. Wybieramy Renderer (Ten nowy, obsługujący listy)
        renderer = PlotRenderer()

        # 4. Zwracamy gotowy, skonfigurowany obiekt raportu
        return HeadToHeadReport(session_key, driver1, driver2, composite, renderer)


class QualifyingFactory:
    pass