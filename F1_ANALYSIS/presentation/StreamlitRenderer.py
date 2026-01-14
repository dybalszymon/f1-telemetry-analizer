from presentation.ReportRenderer import ReportRenderer
import streamlit as st
import pandas as pd


class StreamlitRenderer(ReportRenderer):
    def render(self, data, strategies=None):
        """
        Uniwersalny renderer Streamlit.
        Obsługuje zarówno listy (Rankingi) jak i słowniki (Pojedyncze analizy).
        """

        # --- SCENARIUSZ 1: LISTA (Ranking Kwalifikacji) ---
        if isinstance(data, list):
            st.subheader("Wyniki Sesji")

            if not data:
                st.warning("Brak danych do wyświetlenia.")
                return

            # Tworzymy tabelę
            df = pd.DataFrame(data)

            # Jeśli to dane z kwalifikacji (mają czas okrążenia)
            if 'lap_duration' in df.columns:
                # Logika: Najlepszy czas dla każdego kierowcy
                # Grupujemy po numerze, bierzemy indeks minimum czasu
                idx = df.groupby('driver_number')['lap_duration'].idxmin()
                best_laps = df.loc[idx].sort_values('lap_duration').reset_index(drop=True)

                # Wyświetlamy jako ładną tabelę
                st.dataframe(
                    best_laps[['driver_number', 'team', 'lap_duration']],
                    use_container_width=True,
                    column_config={
                        "driver_number": "Nr",
                        "team": "Zespół",
                        "lap_duration": st.column_config.NumberColumn("Czas [s]", format="%.3f")
                    }
                )
            else:
                # Fallback dla innych list
                st.dataframe(df)

        # --- SCENARIUSZ 2: SŁOWNIK (Twoja stara logika) ---
        elif isinstance(data, dict):
            # Jeśli ktoś podał tytuł w danych (opcjonalnie)
            if 'title' in data:
                st.subheader(data['title'])

            # ✅ Obsługa FastestLapStrategy
            if 'driver' in data and 'time' in data and 'lap_number' in data:
                st.subheader("Najszybsze Okrążenie")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Kierowca", f"#{data['driver']}")
                with col2:
                    st.metric("Czas", f"{data['time']:.3f}s")
                with col3:
                    st.metric("Okrążenie", data['lap_number'])

            # ✅ Obsługa ConsistencyScoreStrategy
            elif 'consistency_score' in data:
                st.subheader("Analiza Równości Jazdy")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Kierowca", f"#{data['driver']}")
                with col2:
                    st.metric("Średni czas", f"{data['avg_time']:.3f}s")
                with col3:
                    st.metric("Odchylenie", f"{data['std_dev']:.3f}s")
                with col4:
                    st.metric("Wynik", f"{data['consistency_score']:.1f}")

                st.info(f"Przeanalizowano {data['laps_count']} okrążeń")

            # ✅ Obsługa surowych danych H2H (jeśli trafią tutaj zamiast do UniversalTelemetryRenderer)
            elif 'driver1' in data and 'driver2' in data:
                st.write("Dane porównawcze (użyj UniversalTelemetryRenderer dla wykresów).")
                st.json(data)

            else:
                st.json(data)

        else:
            st.write(str(data))