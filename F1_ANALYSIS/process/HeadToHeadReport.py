from datetime import datetime, timedelta
from process.RaceReportTemplate import RaceReportTemplate

from F1_ANALYSIS.logic.TelemetryComposite import TelemetryComposite


class HeadToHeadReport(RaceReportTemplate):
    def __init__(self, session_key, driver1, driver2, strategy, facade, renderer):
        super().__init__(session_key, strategy, facade, renderer)
        self.driver1 = driver1
        self.driver2 = driver2

    def _fetch_data(self):

        print(f"[PROCESS] Pobieranie telemetrii dla #{self.driver1} i #{self.driver2}...")

        # Pobierz okrążenia
        laps_d1 = self.facade.get_session_laps(self.session_key, self.driver1)
        laps_d2 = self.facade.get_session_laps(self.session_key, self.driver2)

        # Znajdź najlepsze okrążenie i pobierz jego telemetrię
        telemetry_d1 = self._get_best_lap_telemetry(laps_d1, self.driver1)
        telemetry_d2 = self._get_best_lap_telemetry(laps_d2, self.driver2)


        self.raw_data = {
            "driver1": {
                "name": str(self.driver1),
                "telemetry": telemetry_d1
            },
            "driver2": {
                "name": str(self.driver2),
                "telemetry": telemetry_d2
            }
        }
        if self.raw_data:
            print("[PROCESS] Uruchamiam obliczenia (Delta, Mapa)...")
            self.raw_data = self.strategy.calculate(self.raw_data)

    def _get_best_lap_telemetry(self, laps, driver_num):
        """Helper do pobrania telemetrii najszybszego okrążenia"""
        valid_laps = [l for l in laps if l.get('lap_duration') and l.get('date_start')]

        if not valid_laps:
            print(f" [!] Brak poprawnych okrążeń dla kierowcy {driver_num}")
            return []


        best_lap = min(valid_laps, key=lambda x: x['lap_duration'])
        print(f" -> Kierowca #{driver_num}: Best Lap = {best_lap['lap_duration']}s")

        # Oblicz ramy czasowe
        t_start = datetime.fromisoformat(best_lap['date_start'])
        t_end = t_start + timedelta(seconds=best_lap['lap_duration'])

        # Dodaj buffer
        t_start_buffered = t_start - timedelta(seconds=2)
        t_end_buffered = t_end + timedelta(seconds=2)

        # Pobierz całą telemetrię
        full_telemetry = self.facade.get_car_telemetry(self.session_key, driver_num)

        if not full_telemetry or not isinstance(full_telemetry, list):
            print(f" [!] Błąd lub brak telemetrii dla #{driver_num} (Otrzymano: {type(full_telemetry)})")
            return []

        # if not full_telemetry:
        #     return []

        # Filtruj lokalnie
        filtered = []
        for point in full_telemetry:
            try:
                point_dt = datetime.fromisoformat(point['date']).replace(tzinfo=None)
                if t_start_buffered.replace(tzinfo=None) <= point_dt <= t_end_buffered.replace(tzinfo=None):
                    filtered.append(point)
            except ValueError:
                continue

        print(f"    [FILTERED] {len(filtered)} punktów dla kierowcy {driver_num}")
        return filtered

    def display_output(self):
        if self.renderer:
            strategies_list = []

            if hasattr(self.strategy, 'strategies'):
                # To jest Kompozyt (pudełko) -> wyciągamy zawartość
                strategies_list = self.strategy.strategies
            else:
                # To jest pojedyncza strategia -> pakujemy w listę
                strategies_list = [self.strategy]

            # Przekazujemy listę prostych strategii do renderera
            self.renderer.render(self.raw_data, strategies_list)
        else:
            print("[REPORT] Brak renderera.")
        pass
