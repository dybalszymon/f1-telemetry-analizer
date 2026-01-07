import matplotlib.pyplot as plt
from F1_ANALYSIS.presentation.ReportRenderer import ReportRenderer


class PlotRenderer(ReportRenderer):
    def render(self, title: str, report_data: list):
        
        num_plots = len(report_data)
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 4 * num_plots), sharex=True)


        if num_plots == 1:
            axes = [axes]

        for i, plot_cfg in enumerate(report_data):
            ax = axes[i]
            for driver_code, telemetry in plot_cfg["drivers"].items():
                ax.plot(telemetry["x"], telemetry["y"], label=f"Kierowca {driver_code}")

            ax.set_ylabel(f"{plot_cfg['label']} [{plot_cfg['unit']}]")
            ax.legend(loc="upper right")
            ax.grid(True, linestyle='--', alpha=0.7)

        axes[-1].set_xlabel("Dystans (m)")
        plt.suptitle(title, fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()