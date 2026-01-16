from presentation.ReportRenderer import ReportRenderer
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class StreamlitRenderer(ReportRenderer):
    def render(self, data, strategies=None):
        """
        Główna metoda sterująca wyświetlaniem.
        """

        # --- 1. SCENARIUSZ: LISTA (np. Ranking Kwalifikacji) ---
        if isinstance(data, list):
            st.subheader("Wyniki Sesji")
            if not data:
                st.warning("Brak danych.")
                return

            df = pd.DataFrame(data)

            # Tabela z wynikami okrążeń
            if 'lap_duration' in df.columns:
                idx = df.groupby('driver_number')['lap_duration'].idxmin()
                best_laps = df.loc[idx].sort_values('lap_duration').reset_index(drop=True)

                st.dataframe(
                    best_laps[['driver_number', 'driver_name', 'team', 'lap_duration']],
                    use_container_width=True,
                    column_config={
                        "driver_number": "Nr",
                        "driver_name": "Kierowca",
                        "team": "Zespół",
                        "lap_duration": st.column_config.NumberColumn("Czas [s]", format="%.3f")
                    }
                )
            else:
                st.dataframe(df)

        # --- 2. SCENARIUSZ: SŁOWNIK (Wykresy, Analizy) ---
        elif isinstance(data, dict):

            # ✅ PRIORYTET 1: Wykres Strategii (Pit Stopy)
            # Sprawdzamy to NAJPIERW, zanim sprawdzimy 'title'
            if 'pit_stop_chart_data' in data:
                if 'title' in data:
                    st.subheader(data['title'])

                # Tu wywołujemy rysowanie wykresu
                self._render_pit_stop_chart(data['pit_stop_chart_data'])
                return  # <--- WAŻNE: Kończymy, żeby nie wypisać JSONa na dole

            # ✅ PRIORYTET 2: Najszybsze Okrążenie (Fastest Lap)
            if 'driver' in data and 'time' in data and 'lap_number' in data:
                if 'title' in data: st.subheader(data['title'])

                c1, c2, c3 = st.columns(3)
                c1.metric("Kierowca", f"#{data['driver']}")
                c2.metric("Czas", f"{data['time']:.3f}s")
                c3.metric("Okrążenie", data['lap_number'])
                return

            # ✅ PRIORYTET 3: Inne dane z tytułem (Fallback)
            if 'title' in data:
                st.subheader(data['title'])
                st.write("Podgląd surowych danych:")
                st.json(data)
                return

            # Fallback ostateczny
            st.json(data)

        # --- 3. INNE ---
        else:
            st.write(str(data))

    def _render_pit_stop_chart(self, drivers_data):
        """Rysuje wykres Gantta w Matplotlib"""
        if not drivers_data:
            st.warning("Brak danych do wykresu.")
            return

        st.write("Generowanie wykresu strategii...")  # Debug info

        # Styl
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(14, len(drivers_data) * 0.5 + 2))

        y_labels = list(drivers_data.keys())

        # Rysowanie pasków
        for driver_name, stints in drivers_data.items():
            for stint in stints:
                ax.barh(
                    y=driver_name,
                    width=stint['length'],
                    left=stint['start'],
                    color=stint['color'],
                    edgecolor='black',
                    height=0.6
                )

                # Numer okrążenia przy zjeździe
                ax.text(
                    x=stint['end'],
                    y=driver_name,
                    s=f"{int(stint['end'])}",
                    color='white',
                    va='center', ha='left', fontsize=7
                )

        ax.set_xlabel("Okrążenie")
        ax.invert_yaxis()

        # Usuwamy ramki
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Legenda
        legend_patches = [
            mpatches.Patch(color='#FF3333', label='Soft'),
            mpatches.Patch(color='#FFFF33', label='Medium'),  # Poprawiony hex żółtego
            mpatches.Patch(color='#FFFFFF', label='Hard'),
            mpatches.Patch(color='#39B54A', label='Inter'),
            mpatches.Patch(color='#00AEEF', label='Wet')
        ]
        ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, frameon=False)

        # Renderowanie w Streamlit
        st.pyplot(fig)