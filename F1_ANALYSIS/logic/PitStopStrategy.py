from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
import pandas as pd

class PitStopStrategy(AnalysisStrategyInterface):
    def get_name(self) -> str:
        return "Analiza Strategii Pit Stopów"

    def calculate(self, data: dict):
        """
        data oczekuje słownika: {'stints': [...], 'drivers': [...]}
        """
        stints_data = data.get('stints', [])
        drivers_data = data.get('drivers', [])

        if not stints_data or not drivers_data:
            return {"error": "Brak danych o stintach lub kierowcach"}

        driver_map = {d['driver_number']: d['name_acronym'] for d in drivers_data}
        
        compound_colors = {
            'SOFT': '#FF3333',
            'MEDIUM': '#FFF200',
            'HARD': '#FFFFFF',
            'INTERMEDIATE': '#39B54A',
            'WET': '#00AEEF',
            'TEST': '#808080'
        }

        processed_drivers = {}

        df = pd.DataFrame(stints_data)
        
        driver_numbers = df['driver_number'].unique()

        for driver_num in driver_numbers:
            driver_stints = df[df['driver_number'] == driver_num].sort_values('lap_start')
            driver_acronym = driver_map.get(driver_num, f"#{driver_num}")
            
            stints_list = []
            for _, stint in driver_stints.iterrows():
                compound = str(stint['compound']).upper() if stint['compound'] else 'UNKNOWN'
                
                stints_list.append({
                    'start': stint['lap_start'],
                    'end': stint['lap_end'],
                    'length': stint['lap_end'] - stint['lap_start'],
                    'compound': compound,
                    'color': compound_colors.get(compound, '#808080')
                })
            
            processed_drivers[driver_acronym] = stints_list

        return {
            'pit_stop_chart_data': processed_drivers,
            'title': "Strategia Opon i Pit Stopów"
        }