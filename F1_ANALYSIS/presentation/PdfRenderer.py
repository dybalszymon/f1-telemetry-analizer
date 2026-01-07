from presentation.ReportRenderer import ReportRenderer

class PdfRenderer(ReportRenderer):
    def render(self, data):
        print(f"--- RAPORT PDF ---\nGeneruję plik PDF z danymi: {data}...")
