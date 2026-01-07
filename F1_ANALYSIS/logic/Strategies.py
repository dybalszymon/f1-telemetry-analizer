#from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from typing import List, Any

from datetime import datetime
from F1_ANALYSIS.logic.AnalysisStrategyInterface import AnalysisStrategyInterface


class FastestLapStrategy(AnalysisStrategyInterface):
    def calculate(self, data: list):
        if not data:
            return None

        # Filtrujemy dane
        valid_laps = [lap for lap in data if lap.get('lap_duration') is not None]

        if not valid_laps:
            return None

        # Szukamy minimum
        best_lap = min(valid_laps, key=lambda x: x['lap_duration'])

        return {
            "driver": best_lap.get("driver_number"),
            "time": best_lap.get("lap_duration"),
            "lap_number": best_lap.get("lap_number")
        }

    def get_name(self) -> str:
        return "Analiza Najszybszego Okrążenia"


# --- STRATEGIA 2: TELEMETRIA (Wykresy) ---
class TelemetryComparisonStrategy(AnalysisStrategyInterface):
    def __init__(self, data_type: str = "speed", label: str = "Prędkość", unit: str = "km/h"):
        self.data_type = data_type
        self.label = label
        self.unit = unit

    def calculate(self, raw_data: dict) -> dict:
        processed_plot = {
            "label": self.label,
            "unit": self.unit,
            "drivers": {}
        }

        for driver_key, driver_info in raw_data.items():
            # driver_info to np. {"name": "1", "telemetry": [...]}
            telemetry_list = driver_info['telemetry']
            driver_name = driver_info['name']

            if not telemetry_list:
                continue

            x_axis, y_axis = self._calculate_axis(telemetry_list)

            processed_plot["drivers"][driver_name] = {
                "x": x_axis,
                "y": y_axis
            }

        return processed_plot

    def _calculate_axis(self, telemetry_list):
        """Zamiana Czasu na Dystans."""
        x_dist = []
        y_val = []

        current_distance = 0
        previous_time = None

        # Sortujemy po dacie
        sorted_data = sorted(telemetry_list, key=lambda x: x['date'])

        for point in sorted_data:
            current_time = datetime.fromisoformat(point['date'])
            speed_kmh = point['speed']

            # Pobieramy wartość dla osi Y (np. speed, rpm, throttle)
            val = point.get(self.data_type, 0)
            y_val.append(val)

            # Obliczanie dystansu (oś X)
            if previous_time is None:
                x_dist.append(0)
            else:
                delta_seconds = (current_time - previous_time).total_seconds()
                speed_ms = speed_kmh / 3.6
                distance_segment = speed_ms * delta_seconds
                current_distance += distance_segment
                x_dist.append(current_distance)

            previous_time = current_time

        return x_dist, y_val

    def get_name(self) -> str:
        return f"Analiza: {self.label}"


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