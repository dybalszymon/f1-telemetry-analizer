from process.RaceReportTemplate import RaceReportTemplate
from logic.PitStopStrategy import PitStopStrategy


class PitStopReport(RaceReportTemplate):
    def __init__(self, session_key: int, strategy, facade, renderer=None):
        # Przekazujemy wszystko do rodzica
        super().__init__(session_key, strategy, facade, renderer)

    def _fetch_data(self):
        print(f"[PROCESS] Pobieranie danych stintów...")
        # Pobieramy surowe dane
        stints = self.facade.get_stints(self.session_key)
        drivers = self.facade.get_session_drivers(self.session_key)

        # Zapisujemy do raw_data (Strategia to potem przeliczy)
        self.raw_data = {
            'stints': stints,
            'drivers': drivers
        }

    def display_output(self):
        if self.renderer and self.result:
            # self.result to już wynik działania Strategy.calculate()
            self.renderer.render(self.result)