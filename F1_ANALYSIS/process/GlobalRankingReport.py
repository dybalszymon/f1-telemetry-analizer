from process.RaceReportTemplate import RaceReportTemplate
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from presentation.StreamlitRenderer import StreamlitRenderer


class GlobalRankingReport(RaceReportTemplate):
    def __init__(self, session_key: int, strategy: AnalysisStrategyInterface):
        renderer = StreamlitRenderer()
        # ✅ Nie tworzymy facade - klasa bazowa to robi
        super().__init__(session_key, strategy, renderer)

    def _fetch_data(self):
        """Pobiera dane okrążeń dla całej sesji"""
        print(f"[PROCESS] Pobieranie danych dla sesji {self.session_key}...")
        self.raw_data = self.facade.get_session_laps(self.session_key)
        
        if not self.raw_data:
            print("[!] Brak danych dla tej sesji")
        else:
            print(f"[OK] Pobrano {len(self.raw_data)} okrążeń")

    def display_output(self):
        """Fallback gdyby renderer nie był dostępny"""
        if self.result:
            print(f"\n--- RANKING: {self.strategy.get_name()} ---")
            print(f"Kierowca #{self.result['driver']}")
            print(f"Czas: {self.result['time']}s")
            print(f"Okrążenie: {self.result['lap_number']}")
            print("----------------------------------------\n")
