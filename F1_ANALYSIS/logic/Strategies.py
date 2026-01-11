from typing import Any
from datetime import datetime
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface

from collections import defaultdict

class FastestLapStrategy(AnalysisStrategyInterface):
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

        sorted_data = sorted(telemetry_list, key=lambda x: x['date'])

        for point in sorted_data:
            current_time = datetime.fromisoformat(point['date'])
            speed_kmh = point['speed']

            val = point.get(self.data_type, 0)
            y_val.append(val)

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


class ConsistencyScoreStrategy(AnalysisStrategyInterface):
    def calculate(self, data: list):
        """
        Analizuje spójność czasów okrążeń.
        Niższe odchylenie standardowe = większa konsystencja
        """
        if not data:
            return None
            
        valid_laps = [lap for lap in data if lap.get('lap_duration') is not None]
        
        if len(valid_laps) < 2:
            return None
        
        times = [lap['lap_duration'] for lap in valid_laps]
        avg_time = sum(times) / len(times)
        variance = sum((t - avg_time) ** 2 for t in times) / len(times)
        std_dev = variance ** 0.5
        
        driver = valid_laps[0].get('driver_number')
        
        return {
            "driver": driver,
            "avg_time": avg_time,
            "std_dev": std_dev,
            "consistency_score": 100 / (1 + std_dev),
            "laps_count": len(valid_laps)
        }
    
    def get_name(self) -> str:
        return "Analiza Konsystencji"


# Puste strategie do przyszłej implementacji
class BrakeAnalysis(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        return {"info": "Analiza hamowania - do zaimplementowania"}
    
    def get_name(self) -> str:
        return "Analiza Hamowania"


class UltimateLapStrategy(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        return {"info": "Ultimate Lap - do zaimplementowania"}
    
    def get_name(self) -> str:
        return "Ultimate Lap"


class TyreDegradationStrategy(AnalysisStrategyInterface):

    def calculate(self, data: Any):

        # fitlrujemy dane po driver_number, nastepnie sortujemy wzgledem okrazenia
        drivers_map = {}

        for record in data:
            driver_number = record.get("driver_number")
            if driver_number not in drivers_map:
                drivers_map[driver_number] = []
            drivers_map[driver_number].append(record)

        degradation_data = defaultdict(list)

        for driver_number, laps in drivers_map.items():
            laps.sort(key=lambda x: x.get("lap_number", 0))

            stint = 1
            left = 0
            for i in range(len(laps)):
                if laps[i]["is_pit_out_lap"] or i == len(laps) - 1:
                    end_time = 0
                    start_time = laps[left + 1]["lap_duration"]
                    
                    if i == len(laps) - 1 and not laps[i]["is_pit_out_lap"]:
                        end_time = laps[i]["lap_duration"] 
                    else:
                        end_time = laps[i - 2]["lap_duration"]

                    if end_time is not None and start_time is not None:        
                        diff = end_time - start_time                
                        degradation_data[driver_number].append({"stint": stint, "degradation": diff})
                        
                        stint += 1
                    
                    left = i
        
        return degradation_data
    
    def get_name(self) -> str:
        return "Analiza Degradacji Opon"


class GearUsageAnalysis(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        return {"info": "Użycie biegów - do zaimplementowania"}
    
    def get_name(self) -> str:
        return "Analiza Użycia Biegów"


class ThrottleAnalysis(AnalysisStrategyInterface):
    def calculate(self, data: Any):
        return {"info": "Analiza gazu - do zaimplementowania"}
    
    def get_name(self) -> str:
        return "Analiza Gazu"
