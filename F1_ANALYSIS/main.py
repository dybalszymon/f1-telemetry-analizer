from enum import Enum
from creation.RaceFactory import RaceReportFactory
from creation.QualifyingFactory import QualifyingReportFactory

from presentation.CliRenderer import CliRenderer
from presentation.PdfRenderer import PdfRenderer
from presentation.PlotRenderer import PlotRenderer

import typer

app = typer.Typer()


class ReportFormat(str, Enum):
    CLI = "cli"
    PDF = "pdf"
    PLOT = "plot"

def get_renderer(fmt: ReportFormat):
    if fmt == ReportFormat.CLI:
        return CliRenderer()
    elif fmt == ReportFormat.PDF:
        return PdfRenderer()
    elif fmt == ReportFormat.PLOT:
        return PlotRenderer()
    else:
        return CliRenderer()


@app.command()
def race_report_comparison(
    driver1: str, 
    driver2: str, 
    format: ReportFormat = typer.Option(ReportFormat.CLI, help="Format raportu: cli, pdf lub plot")
):
    """
    Generuje raport porównawczy między dwoma kierowcami.
    """
    factory = RaceReportFactory()
    
    renderer = get_renderer(format)
    
    print(f"Generowanie raportu dla {driver1} vs {driver2} w formacie {format.value}...")

    report = factory.create_comparison_report(driver1, driver2, renderer)
    
    report.generate_report()

@app.command()
def race_report_global(
    format: ReportFormat = typer.Option(ReportFormat.CLI, help="Wybierz format")
):
    """
    Generuje raport typu Race (Global Ranking).
    """
    factory = RaceReportFactory()
    renderer = get_renderer(format)
    
    report = factory.create_ranking_report(renderer)
    report.generate_report()

if __name__ == "__main__":
    app()