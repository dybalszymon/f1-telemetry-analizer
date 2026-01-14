
class SessionSelector:
    """
    Klasa odpowiedzialna za logikę biznesową wyboru sesji.
    Filtruje wyścigi, znajduje odpowiednie sesje i przygotowuje listy kierowców.
    """

    def __init__(self, facade):
        self.facade = facade

    def get_filtered_races(self, year: int) -> list:

        all_meetings = self.facade.get_meetings(year)
        if not all_meetings:
            return []

        #  Tylko wydarzenia mające "Grand Prix" w nazwie
        return [m for m in all_meetings if "GRAND PRIX" in m['meeting_official_name']]

    def get_qualifying_session_id(self, meeting_key: int) -> tuple[int, str]:
        """
        Szuka klucza sesji kwalifikacyjnej dla danego weekendu (nie kwalifikacje do sprintu).
        Zwraca (session_key, session_name) lub (None, None).
        """
        sessions = self.facade.get_sessions(meeting_key)
        if not sessions:
            return None, None

        qual_session = next((s for s in sessions if "Qualifying" in s['session_name'] and "Sprint" not in s['session_name']), None)

        if qual_session:
            return qual_session['session_key'], qual_session['session_name']
        return None, None

    def get_formatted_driver_list(self, session_key: int) -> dict:

        drivers_data = self.facade.get_session_drivers(session_key)
        if not drivers_data:
            return {}


        unique_drivers = {}
        for d in drivers_data:
            if d['driver_number'] not in unique_drivers:
                unique_drivers[d['driver_number']] = d

        sorted_drivers = sorted(unique_drivers.values(), key=lambda x: x['driver_number'])


        driver_options = {}
        for d in sorted_drivers:
            label = f"#{d['driver_number']} - {d['full_name']} ({d.get('team_name', 'N/A')})"
            driver_options[label] = d['driver_number']

        return driver_options