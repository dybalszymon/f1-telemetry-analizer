from presentation.ReportRenderer import ReportRenderer


class PlotRenderer(ReportRenderer):
    def render(self, data):
        print(f"--- WYKRES ---\nTworzę wykres na podstawie danych: {data}...")
        