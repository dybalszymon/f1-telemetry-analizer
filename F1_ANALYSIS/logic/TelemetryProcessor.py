import pandas as pd
import numpy as np


class TelemetryProcessor:
    """
    Statyczna klasa pomocnicza do obliczeń matematycznych na telemetrii.
    """

    @staticmethod
    def calculate_delta(df1: pd.DataFrame, df2: pd.DataFrame, col_name: str = 'speed'):
        """
        Oblicza różnicę (deltę) dla zadanej kolumny.
        Dopasowuje dane drugiego kierowcy do czasu pierwszego kierowcy.
        Zwraca: (time_axis, delta_values)
        """
        # Zabezpieczenie przed pustymi danymi
        if df1.empty or df2.empty:
            return np.array([]), np.array([])

        # Upewniamy się, że mamy czas względny (time_rel)
        if 'time_rel' not in df1.columns:
            df1['time_rel'] = (pd.to_datetime(df1['date']) - pd.to_datetime(df1['date'].iloc[0])).dt.total_seconds()
        if 'time_rel' not in df2.columns:
            df2['time_rel'] = (pd.to_datetime(df2['date']) - pd.to_datetime(df2['date'].iloc[0])).dt.total_seconds()

        # Oś czasu to po prostu czas kierowcy 1
        time_axis = df1['time_rel'].values

        # Pobieramy wartości jako tablice numpy
        s1 = pd.to_numeric(df1[col_name], errors='coerce').values
        s2 = pd.to_numeric(df2[col_name], errors='coerce').values
        t2 = df2['time_rel'].values

        # Interpolacja: dopasowujemy s2 (kierowca 2) do momentów czasu kierowcy 1
        s2_interp = np.interp(time_axis, t2, s2)

        # Delta: + znaczy D1 ma więcej (jest szybszy), - znaczy D2 ma więcej
        delta = s1 - s2_interp

        return time_axis, delta