from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from logic.Strategies import *


class TelemetryComposite(AnalysisStrategyInterface):
    def __init__(self):
        self.strategies = []

    def add(self, strategy: AnalysisStrategyInterface):
        self.strategies.append(strategy)

    def calculate(self, data):

        composite_result = {}
        for strategy in self.strategies:
            composite_result[strategy.get_name()] = strategy.calculate(data)
        return composite_result

    def get_name(self):
        return "Złożona Telemetria Porównawcza"

def create_telemetry_comparison(self, session_key, d1, d2):
    composite = TelemetryComposite()
    composite.add(SpeedStrategy())
    composite.add(ThrottleStrategy())
    composite.add(BrakeStrategy())

    return HeadToHeadReport(session_key, d1, d2, composite, PlotRenderer())
# Factory do tworzenia gotowych paczek analiz
class StrategyFactory:
    @staticmethod
    def create_base_telemetry():
        composite = TelemetryComposite()
        # composite.add(BrakeAnalysis())
        # composite.add(ConsistencyScoreStrategy())
        # composite.add(UltimateLapStrategy())

        return composite

    @staticmethod
    def create_advanced_telemetry():
        composite = TelemetryComposite()
        # composite.add(BrakeAnalysis())
        # composite.add(ConsistencyScoreStrategy())
        # composite.add(UltimateLapStrategy())
        # composite.add(TyreDegradationStrategy())
        # composite.add(GearUsageAnalysis())
        # composite.add(ThrottleAnalysis())

        return composite
