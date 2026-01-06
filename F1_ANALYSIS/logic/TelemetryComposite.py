from AnalysisStrategyInterface import AnalysisStrategy
from strategies import *

class TelemetryComposite(AnalysisStrategy):
    def __init__(self):
        # Lista przechowująca dzieci (inne strategie lub inne kompozyty)
        self.children: List[AnalysisStrategy] = []

    def add(self, strategy: AnalysisStrategy):
        # Tutaj będzie logika dodawania (np. self.children.append(strategy))
        pass

    def calculate(self, data: Any):
        # Tutaj będzie pętla po self.children
        # for child in self.children:
        #     child.calculate(data)
        pass


class StrategyFactory:
    @staticmethod
    def create_base_telemetry():
        composite = TelemetryComposite()
        composite.add(BrakeAnalysis())
        composite.add(ConsistencyScoreStrategy())
        composite.add(UltimateLapStrategy())

        return composite

    @staticmethod
    def create_advanced_telemetry():
        composite = TelemetryComposite()
        composite.add(BrakeAnalysis())
        composite.add(ConsistencyScoreStrategy())
        composite.add(UltimateLapStrategy())
        composite.add(TyreDegradationStrategy())
        composite.add(GearUsageAnalysis())
        composite.add(ThrottleAnalysis())

        return composite
