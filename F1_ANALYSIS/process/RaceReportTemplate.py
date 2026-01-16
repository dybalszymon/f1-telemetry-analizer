from abc import ABC, abstractmethod

class RaceReportTemplate(ABC):
    def __init__(self, session_key: int, strategy, facade, renderer=None):
        self.session_key = session_key
        self.strategy = strategy
        self.facade = facade  # ✅ To jest kluczowe! Musimy to zapisać
        self.renderer = renderer
        self.raw_data = None
        self.result = None

    def generate_report(self):
        """Metoda Szablonowa - definiuje algorytm"""
        self._fetch_data()
        self._analyze_data()
        self.display_output()

    @abstractmethod
    def _fetch_data(self):
        pass

    def _analyze_data(self):
        if self.strategy and self.raw_data:
            print(f"[TEMPLATE] Uruchamiam strategię: {self.strategy.__class__.__name__}")
            self.result = self.strategy.calculate(self.raw_data)
        else:
            self.result = self.raw_data

    @abstractmethod
    def display_output(self):
        pass