#from presentation.ReportRenderer import ReportRenderer

class CliRenderer(ReportRenderer):
    def render(self, data):
        print(f"--- RAPORT CLI ---\nWynik analizy: {data}\n------------------")
