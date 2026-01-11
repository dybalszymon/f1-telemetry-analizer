from process.RaceReportTemplate import RaceReportTemplate
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from presentation.StreamlitRenderer import StreamlitRenderer


class GlobalRankingReport(RaceReportTemplate):
    def __init__(self, session_key: int, strategy: AnalysisStrategyInterface, renderer = StreamlitRenderer()):
        super().__init__(session_key, strategy, renderer)

    def _fetch_data(self):
        """Pobiera dane okrążeń dla całej sesji"""
        print(f"[PROCESS] Pobieranie danych dla sesji {self.session_key}...")
        self.raw_data = self.facade.get_session_laps(self.session_key)
        
        if not self.raw_data:
            print("[!] Brak danych dla tej sesji")
        else:
            print(f"[OK] Pobrano {len(self.raw_data)} okrążeń")