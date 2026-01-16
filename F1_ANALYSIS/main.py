import streamlit as st

from F1_ANALYSIS.logic.SessionSelector import SessionSelector
from creation.QualifyingFactory import QualifyingFactory
from creation.RaceFactory import RaceReportFactory
from data.F1DataFacade import F1DataFacade
from process.PitStopReport import PitStopReport
from presentation.StreamlitRenderer import StreamlitRenderer

st.set_page_config(page_title="F1 Telemetry Analyzer", layout="wide")

facade = F1DataFacade()
qualifying_factory = QualifyingFactory()
race_factory = RaceReportFactory()
selector = SessionSelector(facade)
streamlit_renderer = StreamlitRenderer()

st.title("🏎️ F1 Telemetry Analyzer")

st.sidebar.header("Wybierz rodzaj analizy")
analysis_type = st.sidebar.radio(
    "Typ analizy:",
    [
        "Lista wyścigów", 
        "Ranking Kwalifikacji", 
        "Porównanie Telemetrii Kwalifikacje (H2H)",
        "Strategia Pit Stopów"
    ]
)

if analysis_type == "Lista wyścigów":
    st.header("📅 Dostępne wyścigi 2024")
    
    if st.button("Pobierz listę wyścigów"):
        with st.spinner("Pobieranie danych..."):
            races = facade.get_meetings(2024)
            
            if races:
                st.success(f"Znaleziono {len(races)} wyścigów")
                
                race_data = []
                for r in races:
                    race_data.append({
                        "Meeting Key": r['meeting_key'],
                        "Nazwa": r['meeting_official_name'],
                        "Lokalizacja": r.get('location', 'N/A'),
                        "Data": r.get('date_start', 'N/A')[:10] if r.get('date_start') else 'N/A'
                    })
                
                st.dataframe(race_data, use_container_width=True)
            else:
                st.error("Nie udało się pobrać danych")

elif analysis_type == "Ranking Kwalifikacji":
    st.header("🏁 Ranking Kwalifikacji - Najszybsze Okrążenie")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        session_key = st.number_input(
            "Podaj Session Key:",
            min_value=1,
            value=9158,
            help="Przykład: 9158 (Bahrajn 2024 Qualifying)"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🚀 Generuj Raport", type="primary"):
            with st.spinner("Przetwarzanie danych..."):
                try:
                    report = qualifying_factory.create_ranking_report(int(session_key))
                    report.generate_report()
                    st.success("✅ Raport wygenerowany!")
                except Exception as e:
                    st.error(f"❌ Błąd: {str(e)}")

elif analysis_type == "Porównanie Telemetrii Kwalifikacje (H2H)":
    st.header("📊 Porównanie Telemetrii")

    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("1. Rok", [2024, 2023])

    races = selector.get_filtered_races(year)

    if not races:
        st.error("Nie udało się pobrać listy wyścigów.")
    else:
        race_map = {r['meeting_official_name']: r['meeting_key'] for r in races}
        with col2:
            race_name = st.selectbox("2. Wyścig", list(race_map.keys()))
            meeting_key = race_map[race_name]

        st.info(f"Wybrano: {race_name}")

        with st.spinner("Szukanie sesji kwalifikacyjnej..."):
            session_key, session_name = selector.get_qualifying_session_id(meeting_key)

        if not session_key:
            st.error("❌ Dla tego wyścigu nie znaleziono sesji 'Qualifying'.")
        else:
            st.success(f"✅ Znaleziono sesję: **{session_name}** (ID: `{session_key}`)")

            driver_options = selector.get_formatted_driver_list(session_key)

            if not driver_options:
                st.warning("Brak danych o kierowcach.")
            else:
                st.subheader("Wybór Kierowców")
                d_col1, d_col2 = st.columns(2)
                driver_labels = list(driver_options.keys())

                with d_col1:
                    l1 = st.selectbox("Kierowca 1", driver_labels, index=0)
                with d_col2:
                    l2 = st.selectbox("Kierowca 2", driver_labels, index=1 if len(driver_labels) > 1 else 0)

                if st.button("📈 Generuj Wykres", type="primary"):
                    d1_num = driver_options[l1]
                    d2_num = driver_options[l2]

                    if d1_num == d2_num:
                        st.warning("Wybierz różnych kierowców.")
                    else:
                        with st.spinner("Analiza w toku..."):
                            try:
                                report = qualifying_factory.create_comparison_report(session_key, d1_num, d2_num)
                                report.generate_report()
                                st.success("Gotowe!")
                            except Exception as e:
                                st.error(f"Błąd: {e}")

elif analysis_type == "Strategia Pit Stopów":
    st.header("🛠️ Analiza Strategii Pit Stopów (Pirelli Style)")
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("1. Rok", [2024, 2023], key="pit_year")

    races = selector.get_filtered_races(year)

    if not races:
        st.error("Błąd pobierania listy wyścigów.")
    else:
        race_map = {r['meeting_official_name']: r['meeting_key'] for r in races}
        with col2:
            race_name = st.selectbox("2. Wyścig", list(race_map.keys()), key="pit_race")
            meeting_key = race_map[race_name]
            
        if st.button("🔍 Znajdź sesję wyścigową i generuj"):
            with st.spinner("Szukanie sesji wyścigowej..."):
                sessions = facade.get_sessions(meeting_key)
                race_session = next((s for s in sessions if "Race" in s['session_name']), None)
                
            if race_session:
                session_key = race_session['session_key']
                st.success(f"Znaleziono sesję: {race_session['session_name']} (ID: {session_key})")
                
                with st.spinner("Pobieranie danych o oponach i generowanie wykresu..."):
                    try:
                        report = PitStopReport(session_key, renderer=streamlit_renderer)
                        report.generate_report()
                    except Exception as e:
                        st.error(f"Wystąpił błąd podczas generowania raportu: {e}")
                        st.exception(e)
            else:
                st.error("Nie znaleziono sesji wyścigowej dla tego wydarzenia.")

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Jak używać:**
    
    1. **Lista wyścigów** - pobierz dostępne wyścigi
    2. **Ranking** - analiza najszybszych okrążeń
    3. **H2H** - porównanie kierowców
    4. **Pit Stopy** - wizualizacja strategii opon
    """
)