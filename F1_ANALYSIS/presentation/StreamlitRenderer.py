from presentation.ReportRenderer import ReportRenderer
import streamlit as st

class StreamlitRenderer(ReportRenderer):
    def render(self, title: str, data):
        """Renderuje dane w interfejsie Streamlit"""
        st.subheader(title)
        
        if isinstance(data, dict):
            # 1. Sprawdzamy czy to dane degradacji (słownik {kierowca: [lista_stintow]})
            # Pobieramy pierwszą wartość, aby sprawdzić strukturę
            first_val = next(iter(data.values())) if data else None
            
            is_degradation_data = (
                isinstance(first_val, list) 
                and len(first_val) > 0 
                and isinstance(first_val[0], dict)
                and 'stint' in first_val[0] 
                and 'degradation' in first_val[0]
            )

            if is_degradation_data:
                # ---------------------------------------------------------
                # ✅ NOWA OBSŁUGA DEGRADACJI (Wykres + Tabela)
                # ---------------------------------------------------------
                for driver_id, stints_data in data.items():
                    st.markdown(f"### 🏎️ Kierowca #{driver_id}")
                    
                    # 1. Wykres
                    st.caption("Wizualizacja spadku tempa (sekundy na okrążenie)")
                    st.bar_chart(stints_data, x="stint", y="degradation")
                    
                    # 2. Tabelka
                    st.markdown("**Szczegółowe dane:**")
                    
                    # Formatujemy dane, żeby ładnie wyglądały w tabeli
                    formatted_table = [
                        {
                            "Numer Stintu": d["stint"],
                            "Degradacja (s/okr)": f"{d['degradation']:.4f}"
                        }
                        for d in stints_data
                    ]
                    
                    # Używamy st.table dla statycznej, ładnej tabelki 
                    # lub st.dataframe dla interaktywnej
                    st.table(formatted_table)

            # ✅ Obsługa FastestLapStrategy (Twoja stara logika)
            elif 'driver' in data and 'time' in data and 'lap_number' in data:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Kierowca", f"#{data['driver']}")
                with col2:
                    st.metric("Czas", f"{data['time']:.3f}s")
                with col3:
                    st.metric("Okrążenie", data['lap_number'])
            
            # ✅ Obsługa ConsistencyScoreStrategy (Twoja stara logika)
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
                # Jeśli słownik nie pasuje do powyższych, wyświetlamy JSON
                st.json(data)
                
        elif isinstance(data, list):
            st.write(data)
        else:
            st.write(str(data))