#from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from typing import List, Any

from datetime import datetime
from F1_ANALYSIS.logic.AnalysisStrategyInterface import AnalysisStrategyInterface


class TelemetryComparisonStrategy(AnalysisStrategyInterface):
    def __init__(self, data_type: str = "speed", label: str = "Prędkość", unit: str = "km/h"):
        """
        data_type: klucz w JSON z API (np. 'speed', 'rpm', 'throttle', 'n_gear')
        label: nazwa na wykresie
        unit: jednostka
        """
        self.data_type = data_type
        self.label = label
        self.unit = unit

    def calculate(self, raw_data: dict) -> dict:
        """
        Przyjmuje słownik: {'driver1': [punkty...], 'driver2': [punkty...]}
        Zwraca format pod PlotRenderer.
        """
        processed_plot = {
            "label": self.label,
            "unit": self.unit,
            "drivers": {}
        }

        for driver_key, laps_data in raw_data.items():
            # laps_data może być listą słowników (z fasady)
            # Musimy obliczyć oś X (dystans) i wyciągnąć oś Y (wartość)
            x_axis, y_axis = self._calculate_axis(laps_data)

            # Dodajemy do wyniku, np. klucz "VER" (lub driver1)
            # Zakładamy, że driver_key to np. "driver1", więc w prawdziwym kodzie
            # warto by przekazywać też numer kierowcy, ale dla uproszczenia:
            processed_plot["drivers"][driver_key] = {
                "x": x_axis,
                "y": y_axis
            }

        return processed_plot

    def _calculate_axis(self, telemetry_list):

        x_dist = []
        y_val = []

        current_distance = 0
        previous_time = None


        sorted_data = sorted(telemetry_list, key=lambda x: x['date'])

        for point in sorted_data:

            current_time = datetime.fromisoformat(point['date'])
            speed_kmh = point['speed']


            y_val.append(point.get(self.data_type, 0))


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