from presentation.ReportRenderer import ReportRenderer
import matplotlib.pyplot as plt
from F1_ANALYSIS.presentation.ReportRenderer import ReportRenderer

class PlotRenderer(ReportRenderer):
    def render(self, title: str, results: list):
        """
        Przyjmuje listę słowników danych, z których każdy to osobny wykres (subplot).
        """
        num_plots = len(results)
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 4 * num_plots), sharex=True)

        # Jeśli jest tylko jeden wykres, matplotlib nie zwraca listy, więc poprawiamy:
        if num_plots == 1: axes = [axes]

        for i, plot_data in enumerate(results):
            for name, d_data in plot_data["drivers"].items():
                axes[i].plot(d_data["x"], d_data["y"], label=name)

            axes[i].set_ylabel(plot_data["ylabel"])
            axes[i].legend(loc="upper right")
            axes[i].grid(True)

        axes[-1].set_xlabel("Dystans (m)")
        plt.tight_layout()
        plt.show()