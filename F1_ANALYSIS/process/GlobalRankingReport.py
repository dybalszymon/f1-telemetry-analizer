import pandas as pd
from process.RaceReportTemplate import RaceReportTemplate
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from presentation.StreamlitRenderer import StreamlitRenderer


class GlobalRankingReport(RaceReportTemplate):
    def __init__(self, session_key, strategy, facade, renderer):
        super().__init__(session_key, strategy, facade, renderer)

    def _fetch_data(self):
        print(f"[PROCESS] Pobieranie danych dla sesji {self.session_key}...")

        # 1. Pobieramy okrążenia ORAZ listę kierowców
        laps = self.facade.get_session_laps(self.session_key)
        drivers = self.facade.get_session_drivers(self.session_key)

        # 2. Tworzymy mapę kierowców dla szybkiego wyszukiwania
        # { numer_kierowcy: {dane_kierowcy} }
        drivers_map = {}
        if drivers and isinstance(drivers, list):
            for d in drivers:
                d_num = d.get('driver_number')
                if d_num:
                    drivers_map[d_num] = d

        # 3. Łączymy dane (Okrążenia + Nazwiska + Zespoły)
        clean_data = []
        if laps and isinstance(laps, list):
            for l in laps:
                # Interesują nas tylko okrążenia z czasem
                if isinstance(l, dict) and l.get('lap_duration'):
                    driver_num = l.get('driver_number')

                    # Pobieramy dane kierowcy z naszej mapy (jeśli istnieją)
                    driver_info = drivers_map.get(driver_num, {})

                    # Składamy imię i nazwisko (lub używamy akronimu np. VER)
                    full_name = driver_info.get('full_name', f"Kierowca #{driver_num}")
                    name_acronym = driver_info.get('name_acronym', str(driver_num))
                    team_name = driver_info.get('team_name', 'Nieznany')

                    # Czasem API zwraca kolor zespołu
                    team_color = driver_info.get('team_colour', '000000')

                    clean_data.append({
                        'driver_number': driver_num,
                        'driver_name': full_name,
                        'acronym': name_acronym,
                        'team': team_name,
                        'lap_duration': l.get('lap_duration'),
                        'team_color': team_color
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
