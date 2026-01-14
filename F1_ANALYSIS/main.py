import streamlit as st
from F1_ANALYSIS.logic.SessionSelector import SessionSelector
from creation.QualifyingFactory import QualifyingFactory
# from creation.RaceFactory import RaceReportFactory # Jeśli używasz
from data.F1DataFacade import F1DataFacade

st.set_page_config(page_title="F1 Telemetry Analyzer", layout="wide")

# --- INICJALIZACJA (Wstrzykiwanie Zależności) ---
facade = F1DataFacade()
qualifying_factory = QualifyingFactory()
# race_factory = RaceReportFactory()
selector = SessionSelector(facade)

st.title("🏎️ F1 Telemetry Analyzer")

# --- SIDEBAR (Nawigacja) ---
st.sidebar.header("Wybierz rodzaj analizy")
analysis_type = st.sidebar.radio(
    "Typ analizy:",
    ["Ranking Kwalifikacji", "Porównanie Telemetrii (H2H)", "Lista wyścigów"]
)

st.sidebar.markdown("---")
st.sidebar.info("Aplikacja automatycznie wybiera sesję kwalifikacyjną dla wskazanego Grand Prix.")

# ==========================================
# 1. RANKING KWALIFIKACJI
# ==========================================
if analysis_type == "Ranking Kwalifikacji":
    st.header("🏁 Ranking Kwalifikacji")

    # KROK 1: Wybór sesji (Logika delegowana do Selectora)
    # Selector sam rysuje widgety i zwraca ID znalezionej sesji
    session_key = selector.render_selector()

    st.divider()

    # KROK 2: Generowanie Raportu
    if session_key:
        if st.button("🚀 Generuj Ranking", type="primary"):
            with st.spinner(f"Pobieranie danych dla sesji {session_key}..."):
                try:
                    # Fabryka tworzy raport
                    report = qualifying_factory.create_ranking_report(session_key)
                    # Uruchamiamy proces (Template Method)
                    report.generate_report()
                    st.success("✅ Raport wygenerowany!")
                except Exception as e:
                    st.error(f"❌ Błąd: {e}")

# ==========================================
# 2. PORÓWNANIE TELEMETRII (H2H)
# ==========================================
elif analysis_type == "Porównanie Telemetrii (H2H)":
    st.header("📊 Porównanie Kierowców (H2H)")

    # KROK 1: Wybór sesji (Ten sam komponent co wyżej - DRY!)
    session_key = selector.render_selector()

    if session_key:
        st.subheader("Wybór Kierowców")

        # KROK 2: Pobranie listy kierowców (Selector wie jak to zrobić)
        driver_options = selector.get_formatted_driver_list(session_key)

        if not driver_options:
            st.warning("Brak danych o kierowcach dla tej sesji.")
        else:
            # UI wyboru kierowców
            d_col1, d_col2 = st.columns(2)
            driver_labels = list(driver_options.keys())

            with d_col1:
                l1 = st.selectbox("Kierowca 1", driver_labels, index=0)
            with d_col2:
                # Domyślny wybór drugiego kierowcy (jeśli możliwe)
                default_idx = 1 if len(driver_labels) > 1 else 0
                l2 = st.selectbox("Kierowca 2", driver_labels, index=default_idx)

            st.divider()

            # KROK 3: Generowanie Raportu
            if st.button("📈 Porównaj Telemetrię", type="primary"):
                d1_num = driver_options[l1]
                d2_num = driver_options[l2]

                if d1_num == d2_num:
                    st.warning("⚠️ Wybierz dwóch różnych kierowców.")
                else:
                    with st.spinner("Pobieranie i przetwarzanie telemetrii..."):
                        try:
                            # Fabryka składa skomplikowany raport H2H
                            report = qualifying_factory.create_comparison_report(session_key, d1_num, d2_num)
                            report.generate_report()
                            st.success("✅ Analiza zakończona!")
                        except Exception as e:
                            st.error(f"❌ Błąd: {e}")

# ==========================================
# 3. LISTA WYŚCIGÓW (DEBUG / INFO)
# ==========================================
elif analysis_type == "Lista wyścigów":
    st.header("📅 Baza danych wyścigów")

    # Prosty widok tabelaryczny
    year = st.selectbox("Wybierz rok", [2025, 2024, 2023])

    if st.button("Pobierz listę"):
        with st.spinner("Pobieranie..."):
            races = facade.get_meetings(year)
            if races:
                st.dataframe(races, use_container_width=True)
            else:
                st.error("Brak danych.")