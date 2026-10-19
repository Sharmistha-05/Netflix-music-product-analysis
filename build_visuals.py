"""Step 1-2: compute the analysis tables, then render every visual as PNG and as one PDF.

Usage:  python build_visuals.py [path/to/Netflix_Dataset.xlsx]
Outputs go to ./output/ (tables/, figures/, Netflix_Music_Visuals.pdf)
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from src import analysis, charts

OUT = Path(__file__).resolve().parent / "output"


def main(data_path=analysis.DEFAULT_DATA):
    users, journey, seg, scores, pain, motive = analysis.export_tables(OUT / "tables", data_path)
    fig_dir = OUT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    figs = charts.all_figures(users, journey, seg, scores, pain, motive)

    with PdfPages(OUT / "Netflix_Music_Visuals.pdf") as pdf:
        cover = charts._fig("Netflix Music: Project Visuals",
                            "Charts, personas, journey maps, frameworks and roadmap for the Netflix Music launch",
                            source=None)
        for i, (_, caption, _) in enumerate(figs):
            cover.text(0.06 + (i // 12) * 0.46, 0.76 - (i % 12) * 0.055, f"{i + 1:>2}.  {caption}", fontsize=12.5)
        pdf.savefig(cover)
        plt.close(cover)
        for name, caption, build in figs:
            fig = build()
            fig.savefig(fig_dir / f"{name}.png", dpi=150)
            pdf.savefig(fig)
            plt.close(fig)
        info = pdf.infodict()
        info["Title"] = "Netflix Music: Project Visuals"
    print(f"Wrote {len(figs)} figures to {fig_dir} and {OUT / 'Netflix_Music_Visuals.pdf'}")


if __name__ == "__main__":
    main(*sys.argv[1:])
