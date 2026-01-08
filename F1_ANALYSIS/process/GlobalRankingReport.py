import streamlit as st
from process.RaceReportTemplate import RaceReportTemplate
from data.F1DataFacade import F1DataFacade
from logic.AnalysisStrategyInterface import AnalysisStrategyInterface
from presentation.ReportRenderer import ReportRenderer
from typing_extensions import override


# Tworzymy konkretną implementację renderera, bo bazowy ReportRenderer jest abstrakcyjny
class StreamlitRenderer(ReportRenderer):
    def render(self, data):
        if data is not None:
            st.dataframe(data)  # Wyświetla dane w ładnej tabeli Streamlit
        else:
            st.error("Renderer otrzymał puste dane!")


class GlobalRankingReport(RaceReportTemplate):
    def __init__(self, session_key: int, strategy: AnalysisStrategyInterface):
        # Inicjalizujemy fasadę i nasz nowy, działający renderer
        self.session_key = session_key
        self.data_facade = F1DataFacade()
        # Używamy konkretnej klasy zamiast abstrakcyjnej
        self.my_renderer = StreamlitRenderer()

        # Przekazujemy do klasy bazowej
        super().__init__(strategy, self.data_facade, self.my_renderer)

    @override
    def _fetch_data(self):
        # Pobieramy dane przez fasadę
        self.raw_data = self.data_facade.get_session_laps(self.session_key)

    @override
    def display_output(self):
        st.header(f"Ranking dla Sesji: {self.session_key}")
        # Strategia przetwarza surowe dane
        processed_data = self.strategy.execute(self.raw_data)
        # Nasz konkretny renderer wyświetla wynik
        self.my_renderer.render(processed_data)