from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from typing import List, Any


class FastestLapStrategy(AnalysisStrategyInterface):#finding fastest lap in race
    def calculate(self, data: list):
        if not data:
            return None

        valid_laps = [lap for lap in data if lap.get('lap_duration') is not None]

        if not valid_laps:
            return None

        best_lap = min(valid_laps, key=lambda x: x['lap_duration'])

        return {
            "driver": best_lap.get("driver_number"),
            "time": best_lap.get("lap_duration"),
            "lap_number": best_lap.get("lap_number")
        }

    def get_name(self) -> str:
        return "Analiza Najszybszego Okrążenia"

class HeadToHeadStrategy(AnalysisStrategyInterface):
    def calculate(self, data: list):

        results = {}
        for driver, laps in data.items():
            valid_laps = [l for l in laps if l.get('lap_duration') is not None]
            if valid_laps:
                best = min(valid_laps, key=lambda x: x['lap_duration'])
                results[driver] = {
                    "time": best.get("lap_duration"),
                    "lap_number": best.get("lap_number")
                }
        return results

    def get_name(self) -> str:
        return "Head-to-Head Comparison"

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