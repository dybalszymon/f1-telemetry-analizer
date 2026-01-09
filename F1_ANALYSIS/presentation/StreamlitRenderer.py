from presentation.ReportRenderer import ReportRenderer
import streamlit as st


class StreamlitRenderer(ReportRenderer):
    def render(self, title: str, data):
        """Renderuje dane w interfejsie Streamlit"""
        st.subheader(title)
        
        if isinstance(data, dict):
            # ✅ Obsługa FastestLapStrategy
            if 'driver' in data and 'time' in data and 'lap_number' in data:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Kierowca", f"#{data['driver']}")
                with col2:
                    st.metric("Czas", f"{data['time']:.3f}s")
                with col3:
                    st.metric("Okrążenie", data['lap_number'])
            
            # ✅ Obsługa ConsistencyScoreStrategy
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
                # Ogólne wyświetlanie słownika
                st.json(data)
                
        elif isinstance(data, list):
            st.write(data)
        else:
            st.write(str(data))
