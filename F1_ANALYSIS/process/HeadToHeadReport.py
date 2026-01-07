# from process.RaceReportTemplate import RaceReportTemplate
#
# from data.F1DataFacade import F1DataFacade
# from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from datetime import datetime, timedelta
from typing import override


from F1_ANALYSIS.process.RaceReportTemplate import RaceReportTemplate

class HeadToHeadReport(RaceReportTemplate):
    def __init__(self, session_key, driver1, driver2, strategy, renderer):
        super().__init__(session_key, strategy, renderer)
        self.driver1 = driver1
        self.driver2 = driver2

    from datetime import datetime, timedelta

    def fetch_data(self):
        print(f"[PROCESS] Szukanie najszybszych okrążeń dla #{self.driver1} i #{self.driver2}...")

        # 1. Pobieramy lekką listę okrążeń dla obu kierowców
        laps_d1 = self.facade.get_session_laps(self.session_key, self.driver1)
        laps_d2 = self.facade.get_session_laps(self.session_key, self.driver2)

        # 2. Pomocnicza funkcja do znalezienia "Best Lap" i pobrania telemetrii
        def get_best_lap_telemetry(laps, driver_num):
            # Filtrujemy tylko ważne okrążenia (bez zjazdów do boksu, bez błędów)
            valid_laps = [l for l in laps if l.get('lap_duration') and l.get('date_start')]

            if not valid_laps:
                print(f"Ostrzeżenie: Brak poprawnych okrążeń dla kierowcy {driver_num}")
                return []

            # Znajdujemy rekordowe kółko
            best_lap = min(valid_laps, key=lambda x: x['lap_duration'])
            print(
                f" -> Kierowca #{driver_num}: Best Lap = {best_lap['lap_duration']}s (Okrążenie {best_lap['lap_number']})")

            # 3. Wyliczamy czas START i KONIEC tego okrążenia
            # OpenF1 daje 'date_start'. Musimy obliczyć koniec dodając czas trwania.
            t_start = best_lap['date_start']

            # Konwersja stringa na obiekt czasu, dodanie sekund i powrót do stringa
            # Format API: 2023-03-04T15:00:00.000000
            dt_start = datetime.fromisoformat(t_start)
            dt_end = dt_start + timedelta(seconds=best_lap['lap_duration'])
            t_end = dt_end.isoformat()

            # 4. Pobieramy telemetrię TYLKO dla tego wycinka
            return self.facade.get_car_telemetry(self.session_key, driver_num, date_start=t_start, date_end=t_end)

        # Wykonujemy to dla obu
        self.raw_data = {
            "driver1": {
                "name": str(self.driver1),
                "telemetry": get_best_lap_telemetry(laps_d1, self.driver1)
            },
            "driver2": {
                "name": str(self.driver2),
                "telemetry": get_best_lap_telemetry(laps_d2, self.driver2)
            }
        }