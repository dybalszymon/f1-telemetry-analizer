import time
from datetime import datetime, timedelta
from F1_ANALYSIS.process.RaceReportTemplate import RaceReportTemplate


class HeadToHeadReport(RaceReportTemplate):
    def __init__(self, session_key, driver1, driver2, strategy, renderer):
        # Przekazujemy renderer do klasy nadrzędnej
        super().__init__(session_key, strategy, renderer)
        self.driver1 = driver1
        self.driver2 = driver2

    def _fetch_data(self):
        print(f"[PROCESS] Szukanie najszybszych okrążeń dla #{self.driver1} i #{self.driver2}...")

        laps_d1 = self.facade.get_session_laps(self.session_key, self.driver1)
        laps_d2 = self.facade.get_session_laps(self.session_key, self.driver2)

        def get_best_lap_telemetry(laps, driver_num):
            valid_laps = [l for l in laps if l.get('lap_duration') and l.get('date_start')]

            if not valid_laps:
                print(f" [!] Błąd: Brak poprawnych okrążeń dla kierowcy {driver_num}")
                return []

            best_lap = min(valid_laps, key=lambda x: x['lap_duration'])
            print(f" -> Kierowca #{driver_num}: Best Lap = {best_lap['lap_duration']}s")

            t_start = best_lap['date_start']
            dt_start = datetime.fromisoformat(t_start)

            # Margines czasowy
            dt_start_buffered = dt_start - timedelta(seconds=1)
            dt_end_buffered = dt_start + timedelta(seconds=best_lap['lap_duration'] + 1)

            # --- FIX: MILISEKUNDY (3 miejsca po przecinku) ---
            # Formatujemy do pełnych mikrosekund, a potem ucinamy ostatnie 3 znaki.
            # Wynik: 2023-09-15T10:08:48.194 (zamiast .194000)
            t_start_str = dt_start_buffered.strftime("%Y-%m-%dT%H:%M:%S")
            t_end_str = dt_end_buffered.strftime("%Y-%m-%dT%H:%M:%S")

            print(f"    [DEBUG] Pytanie API o zakres: {t_start_str} -> {t_end_str}")

            time.sleep(2.0)  # Zwiększamy czas oczekiwania dla bezpieczeństwa

            try:
                data = self.facade.get_car_telemetry(self.session_key, driver_num, date_start=t_start_str,
                                                     date_end=t_end_str)
                print(f"    [API] Pobranych punktów telemetrii: {len(data)}")
                return data
            except Exception as e:
                # Wypiszemy dokładny URL błędu, żeby zobaczyć co poszło nie tak
                print(f"    [!!!] Błąd API: {e}")
                return []

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

    def display_output(self):
        # W tym raporcie wyświetlaniem zajmuje się renderer w generate_report,
        # ale metoda musi być zdefiniowana, bo wymaga tego klasa abstrakcyjna.
        pass