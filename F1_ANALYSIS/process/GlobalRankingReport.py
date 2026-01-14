import pandas as pd
from process.RaceReportTemplate import RaceReportTemplate
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from presentation.StreamlitRenderer import StreamlitRenderer


class GlobalRankingReport(RaceReportTemplate):
    def __init__(self, session_key, strategy, facade, renderer):
        super().__init__(session_key, strategy, facade, renderer)

    def _fetch_data(self):
        """Pobiera dane okrążeń dla całej sesji"""
        print(f"[PROCESS] Pobieranie danych dla sesji {self.session_key}...")
        laps = self.facade.get_session_laps(self.session_key)

        clean_data = []
        if laps and isinstance(laps, list):
            for l in laps:
                if isinstance(l, dict) and l.get('lap_duration'):
                    clean_data.append({
                        'driver_number': l.get('driver_number'),
                        'team': l.get('team'),
                        'lap_duration': l.get('lap_duration')
                    })
        self.raw_data = clean_data

    def display_output(self):
        if self.renderer:
            self.renderer.render(self.raw_data)
        else:
            print("[REPORT] Brak renderera.")
    # def display_output(self):
    #     """Fallback gdyby renderer nie był dostępny"""
    #     if self.result:
    #         print(f"\n--- RANKING: {self.strategy.get_name()} ---")
    #         print(f"Kierowca #{self.result['driver']}")
    #         print(f"Czas: {self.result['time']}s")
    #         print(f"Okrążenie: {self.result['lap_number']}")
    #         print("----------------------------------------\n")
