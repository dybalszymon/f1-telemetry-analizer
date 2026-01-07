from urllib.parse import urljoin

import requests


class F1DataFacade:
    BASE_URL = "https://api.openf1.org/v1/"

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None):
        """
        Uniwersalna metoda do wysyłania zapytań GET.
        Automatycznie obsługuje kodowanie parametrów URL.
        """
        url = urljoin(self.BASE_URL, endpoint)
        try:

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error: błąd HTTP: {e}")
            # Dla celów debugowania wypiszmy pełny URL
            print(f"       URL: {e.response.url}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error: błąd połączenia: {e}")
            return []

    def get_meetings(self, year: int):
        return self._get("meetings", {'year': year})

    def get_session_laps(self, session_key: int, driver_number: int = None):
        params = {'session_key': session_key}
        if driver_number:
            params['driver_number'] = driver_number
        return self._get("laps", params)

    def get_car_telemetry(self, session_key: int, driver_number: int, date_start: str = None, date_end: str = None):


        params = {
            'session_key': session_key,
            'driver_number': driver_number,
        }

        # Używamy operatorów OpenF1. Biblioteka requests zakoduje je poprawnie.
        if date_start:
            params['date>='] = date_start
        if date_end:
            params['date<'] = date_end

        return self._get("car_data", params)

    def get_drivers(self, session_key: int):
        return self._get("drivers", {'session_key': session_key})

    def get_weather(self, session_key: int):
        return self._get("weather", {'session_key': session_key})

    def get_races(self, year: int):
        #return list of races IDs from choosen year
        params = {'year': year}
        return self._get("races", params);


    def get_lap_times(self):
        return self.data_source.fetch_lap_times()


    def get_telemetry_data(self):
        return self.data_source.fetch_telemetry_data()

    def get_session_data(self):
        pass

    def get_weather_data(self):
        pass