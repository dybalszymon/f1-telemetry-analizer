import requests
from urllib.parse import urljoin

class F1DataFacade:
    BASE_URL = "https://api.openf1.org/v1/"
    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint : str, params : dict = None   ):
        url = urljoin(self.BASE_URL, endpoint);

        try:
            response = self.session.get(url, params=params, timeout=100)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: blad polaczenia z API: {e}")
            return[]

    def get_lap_times(self):

        return self.data_source.fetch_lap_times()


    def get_telemetry_data(self):
        return self.data_source.fetch_telemetry_data()

    def get_session_data(self):
        pass

    def get_weather_data(self):
        pass