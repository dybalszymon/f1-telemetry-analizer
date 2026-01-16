# F1_ANALYSIS/presentation/StreamlitRenderer.py

from presentation.ReportRenderer import ReportRenderer
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class StreamlitRenderer(ReportRenderer):
    def render(self, title: str, data):
        """Renderuje dane w interfejsie Streamlit"""
        st.subheader(title)
        
        if isinstance(data, dict):
            
            # --- NOWA SEKCJA: WYKRES PIT STOPÓW ---
            if 'pit_stop_chart_data' in data:
                self._render_pit_stop_chart(data['pit_stop_chart_data'])
            
            # ✅ Obsługa FastestLapStrategy (istniejąca)
            elif 'driver' in data and 'time' in data and 'lap_number' in data:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Kierowca", f"#{data['driver']}")
                with col2:
                    st.metric("Czas", f"{data['time']:.3f}s")
                with col3:
                    st.metric("Okrążenie", data['lap_number'])
            
            # ✅ Obsługa ConsistencyScoreStrategy (istniejąca)
            elif 'consistency_score' in data:
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
            
            else:
                st.json(data)
                
        elif isinstance(data, list):
            st.write(data)
        else:
            st.write(str(data))

    def _render_pit_stop_chart(self, drivers_data):
        """Prywatna metoda do rysowania wykresu Gantta (styl Pirelli)"""
        if not drivers_data:
            st.warning("Brak danych do wygenerowania wykresu.")
            return

        # Ustawienia stylu wykresu
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Lista kierowców (oś Y)
        y_labels = list(drivers_data.keys())
        
        # Rysowanie pasków
        for driver_name, stints in drivers_data.items():
            for stint in stints:
                # Rysujemy poziomy pasek (stint)
                ax.barh(
                    y=driver_name,
                    width=stint['length'],
                    left=stint['start'],
                    color=stint['color'],
                    edgecolor='black',
                    height=0.4
                )
                
                # Dodajemy numer okrążenia na końcu stintu (zjazd do pitu)
                # Pomijamy ostatni stint (koniec wyścigu)
                # (Prosta heurystyka: jeśli stint kończy się np. > 50 okrążeniu to pewnie koniec)
                # Lepiej: po prostu wypiszmy, tekst będzie mały
                ax.text(
                    x=stint['end'],
                    y=driver_name,
                    s=f"{int(stint['end'])}",
                    color='white',
                    va='center',
                    ha='left',
                    fontsize=8,
                    fontweight='bold'
                )

        # Formatowanie osi
        ax.set_xlabel("Okrążenie")
        ax.invert_yaxis() # Odwracamy, żeby pierwszy kierowca był na górze
        
        # Usunięcie ramek dla czystszego wyglądu
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Legenda opon
        legend_patches = [
            mpatches.Patch(color='#FF3333', label='Soft'),
            mpatches.Patch(color='#FFF200', label='Medium'),
            mpatches.Patch(color='#FFFFFF', label='Hard'),
            mpatches.Patch(color='#39B54A', label='Inter'),
            mpatches.Patch(color='#00AEEF', label='Wet')
        ]
        ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False)
        
        st.pyplot(fig)