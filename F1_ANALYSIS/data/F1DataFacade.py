
class F1DataFacade:
    def __init__(self, data_source):
        self.data_source = data_source

    def get_lap_times(self):
        return self.data_source.fetch_lap_times()

    def get_telemetry_data(self):
        return self.data_source.fetch_telemetry_data()

    def get_session_data(self):
        pass

    def get_weather_data(self):
        pass