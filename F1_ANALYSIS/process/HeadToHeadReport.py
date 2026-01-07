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

        # 1. Pobieramy listę okrążeń
        laps_d1 = self.facade.get_session_laps(self.session_key, self.driver1)
        laps_d2 = self.facade.get_session_laps(self.session_key, self.driver2)

        def get_best_lap_telemetry(laps, driver_num):
            # --- KROK 1: Znalezienie najlepszego kółka ---
            valid_laps = [l for l in laps if l.get('lap_duration') and l.get('date_start')]

            if not valid_laps:
                print(f" [!] Błąd: Brak poprawnych okrążeń dla kierowcy {driver_num}")
                return []

            best_lap = min(valid_laps, key=lambda x: x['lap_duration'])
            print(f" -> Kierowca #{driver_num}: Best Lap = {best_lap['lap_duration']}s")

            # Obliczamy ramy czasowe (tylko dla Pythona, nie dla API)
            t_start = best_lap['date_start']
            dt_start = datetime.fromisoformat(t_start)
            dt_end = dt_start + timedelta(seconds=best_lap['lap_duration'])

            # Dodajemy marginesy (buffer)
            dt_start_buffered = dt_start - timedelta(seconds=2)
            dt_end_buffered = dt_end + timedelta(seconds=2)

            print(
                f"    [LOGIC] Pobieram CAŁĄ telemetrię i wytnę fragment: {dt_start_buffered.time()} -> {dt_end_buffered.time()}")

            # --- KROK 2: Opcja Nuklearna - Pobieramy WSZYSTKO ---
            # Nie podajemy dat do API. Dzięki temu unikamy błędu 500.
            # To zapytanie jest bezpieczne.
            full_telemetry = self.facade.get_car_telemetry(self.session_key, driver_num)

            if not full_telemetry:
                print(f"    [API] Pusta odpowiedź dla kierowcy {driver_num}")
                return []

            print(f"    [API] Pobranno {len(full_telemetry)} punktów. Filtrowanie lokalne...")

            # --- KROK 3: Filtrowanie w Pythonie (skalpel) ---
            filtered_data = []

            # Musimy uważać na strefy czasowe przy porównywaniu
            # Data z API przychodzi jako string ISO
            for point in full_telemetry:
                try:
                    # Parsujemy datę punktu
                    point_time_str = point['date']
                    # Usuwamy 'Z' lub offset jeśli jest, żeby porównać "surowe" czasy
                    # OpenF1 zwykle zwraca np. 2023-09-15T10:08:48.194000
                    # Najbezpieczniej użyć fromisoformat
                    point_dt = datetime.fromisoformat(point_time_str)

                    # Jeśli point_dt ma strefę, a nasze ramy nie (lub odwrotnie), Python rzuci błąd.
                    # Ujednolicamy: usuwamy info o strefie (tzinfo=None)
                    point_dt = point_dt.replace(tzinfo=None)
                    range_start = dt_start_buffered.replace(tzinfo=None)
                    range_end = dt_end_buffered.replace(tzinfo=None)

                    if range_start <= point_dt <= range_end:
                        filtered_data.append(point)
                except ValueError:
                    continue  # Pomijamy błędne daty

            print(f"    [PYTHON] Po wycięciu okrążenia zostało: {len(filtered_data)} punktów")
            return filtered_data

        # Wykonujemy logikę dla obu kierowców
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