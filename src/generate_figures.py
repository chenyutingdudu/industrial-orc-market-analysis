#!/usr/bin/env python3
"""Publication figures for ORC WHR economic feasibility paper."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures"


def main() -> None:
    FIG.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", context="paper")

    market = pd.read_csv(DATA / "market_forecast.csv")
    roi = pd.read_csv(DATA / "roi_analysis.csv")
    sens = pd.read_csv(DATA / "sensitivity_tornado.csv")
    bass = pd.read_csv(DATA / "adoption_bass.csv")
    risk = pd.read_csv(DATA / "risk_register.csv")

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    axes[0, 0].plot(market["year"], market["global_market_usd_bn"], "o-", lw=2)
    axes[0, 0].plot(market["year"], market["china_market_usd_bn"], "s--", lw=2)
    axes[0, 0].set_title("(a) Market size forecast")
    axes[0, 0].set_xlabel("Year")
    axes[0, 0].set_ylabel("USD billion")
    axes[0, 0].legend(["Global", "China industrial"])

    sub = roi[roi["heat_source_temp_C"] == 100]
    axes[0, 1].bar(sub["power_kw"].astype(str), sub["npv_usd"] / 1e6, color="steelblue")
    axes[0, 1].set_title("(b) NPV by plant size @100°C")
    axes[0, 1].set_ylabel("NPV (MUSD)")

    axes[0, 2].scatter(sub["payback_y"], sub["roi_pct"], s=80, c=sub["power_kw"], cmap="viridis")
    axes[0, 2].set_xlabel("Payback (years)")
    axes[0, 2].set_ylabel("ROI (%)")
    axes[0, 2].set_title("(c) ROI vs payback")

    for var in sens["variable"].unique():
        d = sens[sens["variable"] == var]
        axes[1, 0].plot(d["shock_pct"], d["delta_npv"] / 1e6, marker="o", label=var.split("_")[0])
    axes[1, 0].axhline(0, color="k", lw=0.8)
    axes[1, 0].set_title("(d) Sensitivity tornado")
    axes[1, 0].set_xlabel("Shock (%)")
    axes[1, 0].legend(fontsize=7)

    axes[1, 1].plot(bass["year_index"], bass["penetration_pct"], "o-", color="darkgreen", lw=2)
    axes[1, 1].set_title("(e) Bass adoption curve")
    axes[1, 1].set_xlabel("Years from 2025")
    axes[1, 1].set_ylabel("Penetration (%)")

    risk.groupby("category")["impact_score"].mean().plot(kind="barh", ax=axes[1, 2], color="coral")
    axes[1, 2].set_title("(f) Risk impact by category")

    fig.tight_layout()
    out = FIG / "fig_orc_economic_feasibility.pdf"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=300)
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
