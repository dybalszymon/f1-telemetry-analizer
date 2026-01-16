import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
from presentation.ReportRenderer import ReportRenderer


class UniversalTelemetryRenderer(ReportRenderer):
    def render(self, data: dict, strategies: list):
        """
        Uniwersalny renderer.
        :param data: Słownik z danymi telemetrii (driver1, driver2)
        :param strategies: Lista obiektów strategii (np. TelemetryComparisonStrategy)
        """
        d1 = data['driver1']
        d2 = data['driver2']

        # Konwersja na DataFrame (dla bezpieczeństwa)
        df1 = pd.DataFrame(d1['telemetry']) if isinstance(d1.get('telemetry'), list) else pd.DataFrame()
        df2 = pd.DataFrame(d2['telemetry']) if isinstance(d2.get('telemetry'), list) else pd.DataFrame()

        if df1.empty or df2.empty:
            st.error("Brak danych telemetrii do wyrysowania.")
            return

        # Przygotowanie osi czasu (Time Relative)
        if 'date' in df1.columns:
            try:
                t0 = pd.to_datetime(df1['date'].iloc[0], format='mixed')
                df1['time_rel'] = (pd.to_datetime(df1['date'], format='mixed') - t0).dt.total_seconds()
            except Exception as e:
                print(f" [RENDERER WARNING] Problem z datami kierowcy 1: {e}")

        if 'date' in df2.columns:
            try:
                t0 = pd.to_datetime(df2['date'].iloc[0], format='mixed')
                df2['time_rel'] = (pd.to_datetime(df2['date'], format='mixed') - t0).dt.total_seconds()
            except Exception as e:
                print(f" [RENDERER WARNING] Problem z datami kierowcy 2: {e}")
        # DYNAMICZNA KONFIGURACJA
        num_plots = len(strategies)

        # Tworzymy wykresy
        fig, axes = plt.subplots(num_plots, 1, figsize=(14, 3.5 * num_plots), sharex=False)
        if num_plots == 1: axes = [axes]

        c1, c2 = '#1f77b4', '#ff7f0e'  # Niebieski / Pomarańczowy
        name1, name2 = f"#{d1['name']}", f"#{d2['name']}"

        # PĘTLA PO KONFIGURACJI Z FABRYKI
        for i, strategy in enumerate(strategies):
            ax = axes[i]
            col_name = strategy.data_type  # Tutaj używamy atrybutu .data_type (OBIEKT), a nie ['data_type'] (SŁOWNIK)

            # --- 1. SPECJALNY PRZYPADEK: DELTA PRĘDKOŚCI ---
            if col_name == "speed_delta":
                # Pobieramy gotowe obliczenia z Logic Layer
                if 'analysis' in data and 'speed_delta' in data['analysis']:
                    delta_info = data['analysis']['speed_delta']
                    t_axis = delta_info['time']
                    val = delta_info['value']

                    ax.plot(t_axis, val, color='black', linewidth=1)
                    ax.fill_between(t_axis, val, 0, where=(val > 0), color=c1, alpha=0.3, label=f"{name1} szybszy")
                    ax.fill_between(t_axis, val, 0, where=(val < 0), color=c2, alpha=0.3, label=f"{name2} szybszy")
                else:
                    ax.text(0.5, 0.5, "Brak danych delty", ha='center')

                ax.set_ylabel("Delta [km/h]")
                ax.grid(True, alpha=0.5)
                if i == 0: ax.legend(loc="upper right")
                continue

            # --- 2. SPECJALNY PRZYPADEK: MAPA TORU ---
            if col_name == "track_map":
                # ✅ ZABEZPIECZENIE: Czy mamy współrzędne?
                has_coords_1 = 'x' in df1.columns and 'y' in df1.columns

                if not has_coords_1:
                    ax.text(0.5, 0.5, "Brak danych GPS (x, y) w telemetrii", ha='center', fontsize=12, color='red')
                    ax.set_title("Mapa Toru (Dane niedostępne)")
                    ax.axis('off')
                    continue

                # Rysowanie mapy
                if 'analysis' in data and 'speed_delta' in data['analysis']:
                    delta_vals = data['analysis']['speed_delta']['value']
                    # Musimy uważać na długości wektorów
                    if len(delta_vals) == len(df1):
                        scatter = ax.scatter(df1['x'], df1['y'], c=delta_vals, cmap='RdYlGn', s=5, vmin=-20, vmax=20)
                        ax.set_title(f"Mapa Delty: Zielony={name1}, Czerwony={name2}", fontsize=10)
                    else:
                        ax.plot(df1['x'], df1['y'], color=c1)
                        ax.set_title("Mapa Toru (Brak dopasowania delty)")
                else:
                    ax.plot(df1['x'], df1['y'], label=name1, color=c1)
                    if 'x' in df2.columns and 'y' in df2.columns:
                        ax.plot(df2['x'], df2['y'], label=name2, color=c2)

                ax.set_facecolor('black')
                ax.axis('off')
                ax.set_aspect('equal')
                continue

            # --- 3. STANDARDOWE WYKRESY (Speed, RPM, Gear...) ---
            # Konwersja na liczby
            if col_name in df1.columns: df1[col_name] = pd.to_numeric(df1[col_name], errors='coerce')
            if col_name in df2.columns: df2[col_name] = pd.to_numeric(df2[col_name], errors='coerce')

            # Rysowanie (Step vs Line)
            # Sprawdzamy atrybut .plot_style (OBIEKT), a nie ['plot_style']
            style = getattr(strategy, 'plot_style', 'line')

            if style == 'step':
                ax.step(df1['time_rel'], df1[col_name], where='post', color=c1, label=name1 if i == 0 else "")
                ax.step(df2['time_rel'], df2[col_name], where='post', color=c2, label=name2 if i == 0 else "")
            else:
                ax.plot(df1['time_rel'], df1[col_name], color=c1, label=name1 if i == 0 else "")
                ax.plot(df2['time_rel'], df2[col_name], color=c2, label=name2 if i == 0 else "")

            ax.set_ylabel(f"{strategy.label} [{strategy.unit}]")
            ax.grid(True, alpha=0.6)

            if i == 0:
                ax.legend(loc="upper right")

        axes[-1].set_xlabel("Czas okrążenia [s]")
        plt.tight_layout()

        self._display(fig)

    def _display(self, fig):
        try:
            if st.runtime.exists():
                st.pyplot(fig)
            else:
                plt.show()
        except ImportError:
            plt.show()