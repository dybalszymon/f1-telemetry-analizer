from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from typing import List, Any

class BrakeAnalysis(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        pass

class ConsistencyScoreStrategy(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        pass

class UltimateLapStrategy(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        pass

class TyreDegradationStrategy(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        pass

class GearUsageAnalysis(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        pass

class ThrottleAnalysis(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        pass

# --- 3. Kompozyt (Kontener na strategie) ---

class TelemetryComposite(AnalysisStrategyInterface):
    def __init__(self):
        # Lista przechowująca dzieci (inne strategie lub inne kompozyty)
        self.children: List[AnalysisStrategyInterface] = []

    def add(self, strategy: AnalysisStrategyInterface):
        # Tutaj będzie logika dodawania (np. self.children.append(strategy))
        pass

    def calculate(self, data: Any):
        # Tutaj będzie pętla po self.children
        # for child in self.children:
        #     child.calculate(data)
        pass