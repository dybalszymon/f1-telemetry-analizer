import streamlit as st
from creation.QualifyingFactory import QualifyingFactory
from creation.RaceFactory import RaceReportFactory
from data.F1DataFacade import F1DataFacade

st.set_page_config(page_title="F1 Telemetry Analyzer", layout="wide")

# Inicjalizacja
facade = F1DataFacade()
qualifying_factory = QualifyingFactory()
race_factory = RaceReportFactory()

# Tytuł aplikacji
st.title("🏎️ F1 Telemetry Analyzer")

# Sidebar - wybór rodzaju analizy
st.sidebar.header("Wybierz rodzaj analizy")
# ✅ ZAKTUALIZOWANA LISTA OPCJI
analysis_type = st.sidebar.radio(
    "Typ analizy:",
    [
        "Lista wyścigów", 
        "Ranking Kwalifikacji", 
        "Porównanie Telemetrii (H2H)", 
        "Analiza Degradacji Opon"  # <--- NOWA OPCJA
    ]
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
        if st.button("🚀 Generuj Raport", type="primary"):
            with st.spinner("Przetwarzanie danych..."):
                try:
                    report = qualifying_factory.create_ranking_report(int(session_key))
                    report.generate_report()
                    st.success("✅ Raport wygenerowany!")
                except Exception as e:
                    st.error(f"❌ Błąd: {str(e)}")

# --- PORÓWNANIE TELEMETRII ---
elif analysis_type == "Porównanie Telemetrii (H2H)":
    st.header("📊 Porównanie Telemetrii - Head to Head")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        session_key = st.number_input(
            "Session Key:",
            min_value=1,
            value=9632,
            help="Przykład: 9632"
        )
    
    with col2:
        driver1 = st.number_input(
            "Kierowca 1 (numer):",
            min_value=1,
            max_value=99,
            value=1,
            help="Przykład: 1 (Max Verstappen)"
        )
    
    with col3:
        driver2 = st.number_input(
            "Kierowca 2 (numer):",
            min_value=1,
            max_value=99,
            value=16,
            help="Przykład: 16 (Charles Leclerc)"
        )
    
    st.write("")
    
    if st.button("📈 Generuj Porównanie", type="primary"):
        if driver1 == driver2:
            st.warning("⚠️ Wybierz dwóch różnych kierowców!")
        else:
            with st.spinner("Pobieranie i przetwarzanie telemetrii... To może chwilę potrwać."):
                try:
                    report = qualifying_factory.create_comparison_report(
                        int(session_key),
                        int(driver1),
                        int(driver2)
                    )
                    report.generate_report()
                    st.success("✅ Porównanie wygenerowane!")
                except Exception as e:
                    st.error(f"❌ Błąd: {str(e)}")
                    st.exception(e)

# --- ANALIZA DEGRADACJI OPON (NOWY KOD) ---
elif analysis_type == "Analiza Degradacji Opon":
    st.header("📉 Analiza Degradacji Opon")
    st.info("Analiza ta pokazuje, o ile sekund zwalnia kierowca na każdym okrążeniu w ramach jednego stintu (przejazdu).")

    col1, col2 = st.columns(2)
    
    with col1:
        session_key_deg = st.number_input(
            "Session Key (Wyścig):",
            min_value=1,
            value=9165,  # Przykładowy klucz dla wyścigu (nie kwalifikacji)
            help="Upewnij się, że podajesz ID wyścigu (Race), a nie kwalifikacji. Np. 9165 (Bahrain 2024 Race)",
            key="deg_session" # Unikalny klucz dla widgetu
        )
        
    with col2:
        driver_deg = st.number_input(
            "Kierowca (numer):",
            min_value=1,
            max_value=99,
            value=44,
            help="Przykład: 44 (Lewis Hamilton)",
            key="deg_driver"
        )
        
    st.write("")
    
    if st.button("📉 Oblicz Degradację", type="primary"):
        with st.spinner("Analizowanie stintów i czasów okrążeń..."):
            try:
                # Wywołanie odpowiedniej metody z fabryki wyścigowej
                report = race_factory.create_tyre_degradation_report(
                    int(session_key_deg),
                    int(driver_deg)
                )
                
                # Renderowanie wyników (zostanie obsłużone przez StreamlitRenderer)
                report.generate_report()
                
                st.success("✅ Analiza degradacji zakończona!")
            except Exception as e:
                st.error(f"❌ Wystąpił błąd podczas analizy: {str(e)}")
                # Opcjonalnie wyświetl pełny stack trace dla debugowania
                # st.exception(e)

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Jak używać:**
    
    1. **Lista wyścigów** - pobierz dostępne wyścigi i ich Session Keys
    2. **Ranking** - znajdź najszybsze okrążenie w sesji
    3. **H2H** - porównaj telemetrię dwóch kierowców
    4. **Degradacja** - sprawdź zużycie opon w wyścigu
    
    **Popularne Session Keys:**
    - 9158: Bahrain 2024 Qualifying
    - 9165: Bahrain 2024 Race
    """
)