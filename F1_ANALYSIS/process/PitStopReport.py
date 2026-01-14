# F1_ANALYSIS/process/PitStopReport.py

from process.RaceReportTemplate import RaceReportTemplate
from logic.PitStopStrategy import PitStopStrategy

class PitStopReport(RaceReportTemplate):
    def __init__(self, session_key: int, renderer=None):
        # Wstrzykujemy konkretną strategię
        super().__init__(session_key, PitStopStrategy(), renderer)

    def _fetch_data(self):
        # Pobieramy stinty i kierowców (niezbędne do mapowania nazwisk)
        stints = self.facade.get_stints(self.session_key)
        drivers = self.facade.get_session_drivers(self.session_key)
        
        self.raw_data = {
            'stints': stints,
            'drivers': drivers
        }

    def display_output(self):
        if self.result:
            print(f"Wygenerowano dane dla {len(self.result.get('pit_stop_chart_data', []))} kierowców.")