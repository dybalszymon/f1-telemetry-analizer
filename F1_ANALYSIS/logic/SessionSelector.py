import streamlit as st


class SessionSelector:
    """
    Komponent UI oraz Logiki.
    Zadania:
    1. Wyświetlić wybór Roku i Wyścigu.
    2. Automatycznie znaleźć sesję "Qualifying" (pomijając Sprinty).
    3. Pobrać i sformatować listę kierowców.
    """

    def __init__(self, facade):
        self.facade = facade

    def render_selector(self) -> int | None:
        """
        Rysuje widgety wyboru (Rok -> Wyścig) i automatycznie znajduje ID Kwalifikacji.
        Zwraca: session_key (int) lub None (jeśli nie znaleziono).
        """
        st.markdown("### ⚙️ Konfiguracja Sesji")

        # Układ 2 kolumn: Rok i Wyścig (Sesję znajdujemy w tle)
        col1, col2 = st.columns(2)

        # 1. ROK
        with col1:
            year = st.selectbox("1. Rok", [2025, 2024, 2023], index=1)

        # 2. WYŚCIG (Meeting)
        with col2:
            # Używamy wewnętrznej logiki do pobrania tylko Grand Prix
            races = self._get_filtered_races(year)

            if not races:
                st.error("Brak danych o wyścigach dla wybranego roku.")
                return None

            # Mapa: Nazwa Wyścigu -> Meeting Key
            # Sortujemy, żeby mieć porządek
            race_map = {r['meeting_official_name']: r['meeting_key'] for r in races}
            selected_race_name = st.selectbox("2. Wyścig", list(race_map.keys()))
            meeting_key = race_map[selected_race_name]

        # 3. AUTOMATYCZNE SZUKANIE KWALIFIKACJI
        # Nie pytamy użytkownika, sami szukamy sesji "Qualifying"
        with st.spinner("Szukam sesji kwalifikacyjnej..."):
            session_key, session_name = self._find_qualifying_session(meeting_key)

            if session_key:
                st.caption(f"✅ Znaleziono sesję: **{session_name}** (ID: `{session_key}`)")
                return session_key
            else:
                st.warning(f"⚠️ Nie znaleziono sesji kwalifikacyjnej dla {selected_race_name}.")
                return None

    def get_formatted_driver_list(self, session_key: int) -> dict:
        """
        Pobiera kierowców dla danej sesji i formatuje ich do selectboxa.
        Zwraca: słownik {'#55 - Carlos Sainz (Ferrari)': 55, ...}
        """
        drivers_data = self.facade.get_session_drivers(session_key)
        if not drivers_data:
            return {}

        unique_drivers = {}
        for d in drivers_data:
            if d.get('driver_number'):
                unique_drivers[d['driver_number']] = d

        # Sortowanie po numerze (zabezpieczenie przed błędami rzutowania)
        sorted_drivers = sorted(
            unique_drivers.values(),
            key=lambda x: int(x['driver_number']) if str(x['driver_number']).isdigit() else 999
        )

        driver_options = {}
        for d in sorted_drivers:
            team = d.get('team_name', 'N/A')
            label = f"#{d['driver_number']} - {d['full_name']} ({team})"
            driver_options[label] = d['driver_number']

        return driver_options

    def _get_filtered_races(self, year: int) -> list:
        """Metoda prywatna: Pobiera spotkania i filtruje tylko te z 'Grand Prix' w nazwie"""
        all_meetings = self.facade.get_meetings(year)
        if not all_meetings:
            return []
        return [m for m in all_meetings if "GRAND PRIX" in m['meeting_official_name'].upper()]

    def _find_qualifying_session(self, meeting_key: int) -> tuple[int | None, str | None]:
        """Metoda prywatna: Znajduje ID i nazwę sesji kwalifikacyjnej"""
        sessions = self.facade.get_sessions(meeting_key)
        if not sessions:
            return None, None

        # Szukamy sesji, która ma "Qualifying" ale NIE ma "Sprint"
        qual_session = next(
            (s for s in sessions
             if "Qualifying" in s['session_name']
             and "Sprint" not in s['session_name']),
            None
        )

        if qual_session:
            return qual_session['session_key'], qual_session['session_name']

        return None, None

    def render_race_selector(self) -> int | None:
        """
        Rysuje wybór Rok -> Wyścig, ale automatycznie szuka sesji 'Race' (Wyścig główny).
        """
        st.markdown("### ⚙️ Wybór Wyścigu")

        col1, col2 = st.columns(2)

        # 1. ROK
        with col1:
            year = st.selectbox("1. Rok", [2025, 2024, 2023, 2022], index=1, key="race_year")

        # 2. WYŚCIG
        with col2:
            races = self._get_filtered_races(year)
            if not races:
                st.error("Brak danych.")
                return None

            race_map = {r['meeting_official_name']: r['meeting_key'] for r in races}
            selected_race_name = st.selectbox("2. Wyścig", list(race_map.keys()), key="race_name")
            meeting_key = race_map[selected_race_name]

        # 3. SZUKANIE SESJI 'RACE'
        with st.spinner("Szukam sesji wyścigowej..."):
            sessions = self.facade.get_sessions(meeting_key)
            if not sessions:
                return None

            # Szukamy sesji, która nazywa się po prostu "Race"
            race_session = next((s for s in sessions if s['session_name'] == "Race"), None)

            if race_session:
                st.caption(f"✅ Znaleziono: **{race_session['session_name']}** (ID: {race_session['session_key']})")
                return race_session['session_key']
            else:
                st.error(f"❌ Nie znaleziono sesji wyścigowej dla {selected_race_name}.")
                return None