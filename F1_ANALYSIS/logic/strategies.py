from AnalysisStrategyInterface import AnalysisStrategy
from typing import List, Any

class BrakeAnalysis(AnalysisStrategy):
    def calculate(self, data: Any):
        pass

class ConsistencyScoreStrategy(AnalysisStrategy):
    def calculate(self, data: Any):
        pass

class UltimateLapStrategy(AnalysisStrategy):
    def calculate(self, data: Any):
        pass

class TyreDegradationStrategy(AnalysisStrategy):
    def calculate(self, data: Any):
        pass

class GearUsageAnalysis(AnalysisStrategy):
    def calculate(self, data: Any):
        pass

class ThrottleAnalysis(AnalysisStrategy):
    def calculate(self, data: Any):
        pass

# --- 3. Kompozyt (Kontener na strategie) ---

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