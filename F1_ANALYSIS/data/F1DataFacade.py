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

    def get_session_laps_time(self, session_key: int, driver_number: int = None):
        # last parameter none -> all drivers
        params = {'session_key': session_key}

        if(driver_number):
            params['driver_number'] = driver_number

        return self._get("laps", params)

    def get_car_telemetry(self, session_key: int, driver_number: int):
        """
        func get all data({
        "date": "2024-03-02T15:00:00.456Z",
        "session_key": 9158,
        "driver_number": 1,
        "speed": 315,
        "rpm": 11800,
        "gear": 7,
        "n_gear": false,
        "throttle": 100,
        "brake": 0,
        "drs": 12
        }) from driver, in tests, check if it is too much
        """
        params = {'session_key': session_key,
                  'driver_number': driver_number}
        return self._get("telemetry", params);

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