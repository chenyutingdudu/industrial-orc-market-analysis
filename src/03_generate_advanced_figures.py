from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

def savefig(name):
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / name, dpi=220)
    plt.close()

def money_millions(x):
    return x / 1_000_000

def main():
    financial = pd.read_csv(RESULTS_DIR / "financial_results_advanced.csv")
    scenarios = pd.read_csv(RESULTS_DIR / "scenario_results.csv")
    sensitivity = pd.read_csv(RESULTS_DIR / "sensitivity_results_advanced.csv")
    cashflows = pd.read_csv(RESULTS_DIR / "discounted_cashflow_curves.csv")
    break_even = pd.read_csv(RESULTS_DIR / "break_even_prices.csv")

    # 1. Dashboard: several business metrics in one explainable view.
    metrics = financial.set_index("industry")[["npv_eur", "simple_payback_years", "roi_percent", "annual_co2_avoided_tons"]].copy()
    metrics["npv_million_eur"] = metrics["npv_eur"] / 1_000_000
    metrics = metrics[["npv_million_eur", "simple_payback_years", "roi_percent", "annual_co2_avoided_tons"]]
    normalized = (metrics - metrics.min()) / (metrics.max() - metrics.min())
    # Payback is better when smaller, so reverse it for the dashboard score.
    normalized["simple_payback_years"] = 1 - normalized["simple_payback_years"]
    plt.figure(figsize=(10, 5.8))
    x = np.arange(len(normalized.index))
    width = 0.18
    for i, col in enumerate(normalized.columns):
        plt.bar(x + (i - 1.5) * width, normalized[col], width, label=col)
    plt.xticks(x, normalized.index)
    plt.ylabel("Normalized score, 0 to 1")
    plt.title("ORC Investment Dashboard: Financial Return, Payback, ROI, and CO2 Benefit")
    plt.legend(fontsize=8)
    savefig("01_investment_dashboard.png")

    # 2. Discounted cumulative cash-flow curve.
    plt.figure(figsize=(9, 5.3))
    for industry, group in cashflows.groupby("industry"):
        plt.plot(group["year"], money_millions(group["discounted_cumulative_cashflow_eur"]), marker="o", label=industry)
    plt.axhline(0, linewidth=1)
    plt.xlabel("Project year")
    plt.ylabel("Discounted cumulative cash flow, million EUR")
    plt.title("Discounted Cash-Flow Break-Even Path by ORC Case")
    plt.legend()
    savefig("02_discounted_cashflow_curve.png")

    # 3. Scenario NPV comparison.
    pivot = scenarios.pivot(index="industry", columns="scenario", values="npv_eur")[["conservative", "baseline", "optimistic"]] / 1_000_000
    pivot.plot(kind="bar", figsize=(9, 5.3))
    plt.ylabel("NPV, million EUR")
    plt.xlabel("Case / Industry")
    plt.title("NPV Under Conservative, Baseline, and Optimistic Scenarios")
    plt.xticks(rotation=0)
    savefig("03_scenario_npv_comparison.png")

    # 4. Sensitivity heatmap using percent NPV impact.
    sens = sensitivity.copy()
    sens["test"] = sens["variable"] + "_" + sens["direction"]
    heat = sens.pivot_table(index="industry", columns="test", values="change_from_baseline_percent")
    order = ["electricity_price_low", "electricity_price_high", "capex_low", "capex_high", "power_output_low", "power_output_high", "operating_hours_low", "operating_hours_high"]
    heat = heat[order]
    plt.figure(figsize=(11, 4.8))
    im = plt.imshow(heat.values, aspect="auto")
    plt.colorbar(im, label="NPV change from baseline, %")
    plt.xticks(range(len(heat.columns)), heat.columns, rotation=35, ha="right", fontsize=8)
    plt.yticks(range(len(heat.index)), heat.index)
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            plt.text(j, i, f"{heat.values[i, j]:.0f}%", ha="center", va="center", fontsize=8)
    plt.title("Sensitivity Heatmap: Which Assumptions Move NPV the Most?")
    savefig("04_sensitivity_heatmap.png")

    # 5. Break-even electricity price.
    x = np.arange(len(break_even))
    width = 0.35
    plt.figure(figsize=(9, 5.2))
    plt.bar(x - width/2, break_even["baseline_electricity_price_eur_kwh"], width, label="baseline price")
    plt.bar(x + width/2, break_even["break_even_electricity_price_eur_kwh"], width, label="break-even price")
    plt.xticks(x, break_even["industry"])
    plt.ylabel("EUR/kWh")
    plt.xlabel("Case / Industry")
    plt.title("Required Electricity Price for NPV to Break Even")
    plt.legend()
    savefig("05_break_even_electricity_price.png")

    print("Advanced figures saved to:", FIGURES_DIR)

if __name__ == "__main__":
    main()
