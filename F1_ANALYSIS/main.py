import streamlit as st

from F1_ANALYSIS.logic.SessionSelector import SessionSelector
from creation.QualifyingFactory import QualifyingFactory
from creation.RaceFactory import RaceReportFactory
from data.F1DataFacade import F1DataFacade

st.set_page_config(page_title="F1 Telemetry Analyzer", layout="wide")

# Inicjalizacja
facade = F1DataFacade()
qualifying_factory = QualifyingFactory()
race_factory = RaceReportFactory()
selector = SessionSelector(facade)

# Tytuł aplikacji
st.title("🏎️ F1 Telemetry Analyzer")

# Sidebar - wybór rodzaju analizy
st.sidebar.header("Wybierz rodzaj analizy")
analysis_type = st.sidebar.radio(
    "Typ analizy:",
    ["Lista wyścigów", "Ranking Kwalifikacji", "Porównanie Telemetrii Kwalifikacje (H2H)"]
)

# --- LISTA WYŚCIGÓW ---
if analysis_type == "Lista wyścigów":
    st.header("📅 Dostępne wyścigi 2024")

    if st.button("Pobierz listę wyścigów"):
        with st.spinner("Pobieranie danych..."):
            races = facade.get_meetings(2024)

            if races:
                st.success(f"Znaleziono {len(races)} wyścigów")

                # Wyświetl w tabeli
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

# --- RANKING KWALIFIKACJI ---
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
        generate_clicked = st.button("🚀 Generuj Raport", type="primary")

    if generate_clicked:
        with st.spinner("Przetwarzanie danych..."):
            try:
                # 1. Tworzymy raport
                report = qualifying_factory.create_ranking_report(int(session_key))

                # 2. Generujemy go (teraz wykorzysta pełną szerokość strony)
                report.generate_report()

                st.success("✅ Raport wygenerowany!")

            except Exception as e:
                st.error(f"❌ Błąd: {str(e)}")

# --- PORÓWNANIE TELEMETRII ---
elif analysis_type == "Porównanie Telemetrii Kwalifikacje (H2H)":
    st.header("📊 Porównanie Telemetrii")

    # A. Wybór Roku
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("1. Rok", [2025, 2024, 2023])

    # B. Wybór Wyścigu (Używamy Selector do pobrania czystej listy)
    races = selector.get_filtered_races(year)

    if not races:
        st.error("Nie udało się pobrać listy wyścigów.")
    else:
        race_map = {r['meeting_official_name']: r['meeting_key'] for r in races}
        with col2:
            race_name = st.selectbox("2. Wyścig", list(race_map.keys()))
            meeting_key = race_map[race_name]

        st.info(f"Wybrano: {race_name}")

        # C. Szukanie Kwalifikacji (Logic delegate to Selector)
        with st.spinner("Szukanie sesji kwalifikacyjnej..."):
            session_key, session_name = selector.get_qualifying_session_id(meeting_key)

        if not session_key:
            st.error("Dla tego wyścigu nie znaleziono sesji 'Qualifying'.")
        else:
            st.success(f"Znaleziono sesję: **{session_name}** (ID: `{session_key}`)")

            # D. Pobieranie Kierowców (Logic delegate to Selector)
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

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Jak używać:**
    
    1. **Lista wyścigów** - pobierz dostępne wyścigi i ich Session Keys
    2. **Ranking** - znajdź najszybsze okrążenie w sesji
    3. **H2H** - porównaj telemetrię dwóch kierowców
    
    
    """
)
