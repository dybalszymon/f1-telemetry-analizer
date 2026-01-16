from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
import pandas as pd


class PitStopStrategy(AnalysisStrategyInterface):
    def get_name(self) -> str:
        return "Analiza Strategii Pit Stopów"

    def calculate(self, data):
        """
        Przetwarza surowe stinty na format wykresu Gantta.
        """
        stints = data.get('stints', [])
        drivers = data.get('drivers', [])

        # Mapa: Numer -> Nazwisko
        driver_map = {d['driver_number']: d['name_acronym'] for d in drivers if 'driver_number' in d}

        compound_colors = {
            "SOFT": "#FF3333", "MEDIUM": "#FFFF33", "HARD": "#FFFFFF",
            "INTERMEDIATE": "#39B54A", "WET": "#00AEEF", "TEST": "#999999"
        }

        chart_data = {}

        for s in stints:
            d_num = s.get('driver_number')
            if d_num not in driver_map: continue

            # --- 🛡️ SEKCJA ZABEZPIECZEŃ (TUTAJ BYŁ BŁĄD) ---
            start = s.get("lap_start")
            end = s.get("lap_end")

            # 1. Jeśli brakuje startu lub końca (None) -> Pomiń
            if start is None or end is None:
                continue

            # 2. Jeśli wartości to NaN (Not a Number) -> Pomiń
            # Używamy pd.isna, bo to najpewniejszy sposób na wykrycie NaN
            if pd.isna(start) or pd.isna(end):
                continue
            # -----------------------------------------------

            driver_name = driver_map[d_num]

            if driver_name not in chart_data:
                chart_data[driver_name] = []

            compound = s.get("compound", "UNKNOWN").upper()

            # Teraz możemy bezpiecznie rzutować na int, bo wiemy, że to liczby
            chart_data[driver_name].append({
                "start": int(start),
                "end": int(end),
                "length": int(end) - int(start),
                "color": compound_colors.get(compound, "#555555"),
                "compound": compound
            })

        return {'pit_stop_chart_data': chart_data}