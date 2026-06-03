from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

def savefig(name):
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / name, dpi=220)
    plt.close()

def classify_risk(score):
    if score < 35:
        return "Low"
    elif score < 65:
        return "Medium"
    return "High"

def main():
    financial = pd.read_csv(RESULTS_DIR / "financial_results_advanced.csv")
    sensitivity = pd.read_csv(RESULTS_DIR / "sensitivity_results_advanced.csv")

    # 1. Investment risk ranking based on average absolute NPV sensitivity.
    risk = (
        sensitivity
        .assign(abs_change=lambda x: x["change_from_baseline_percent"].abs())
        .groupby("industry", as_index=False)["abs_change"]
        .mean()
        .rename(columns={"abs_change": "risk_score"})
    )
    risk["risk_level"] = risk["risk_score"].apply(classify_risk)
    risk = risk.sort_values("risk_score", ascending=True)
    risk.to_csv(RESULTS_DIR / "risk_ranking.csv", index=False)

    plt.figure(figsize=(8.5, 4.8))
    plt.bar(risk["industry"], risk["risk_score"])
    plt.ylabel("Average absolute NPV sensitivity, %")
    plt.xlabel("Case / Industry")
    plt.title("Investment Risk Ranking Based on NPV Sensitivity")
    for i, row in risk.reset_index(drop=True).iterrows():
        plt.text(i, row["risk_score"], row["risk_level"], ha="center", va="bottom", fontsize=9)
    savefig("06_risk_ranking.png")

    # 2. Carbon efficiency: annual CO2 avoided per million EUR of CAPEX.
    carbon = financial[["industry", "capex_eur", "annual_co2_avoided_tons", "npv_eur"]].copy()
    carbon["co2_tons_per_million_eur_capex"] = carbon["annual_co2_avoided_tons"] / (carbon["capex_eur"] / 1_000_000)
    carbon = carbon.sort_values("co2_tons_per_million_eur_capex", ascending=False)
    carbon.to_csv(RESULTS_DIR / "carbon_efficiency.csv", index=False)

    plt.figure(figsize=(8.5, 4.8))
    plt.bar(carbon["industry"], carbon["co2_tons_per_million_eur_capex"])
    plt.ylabel("Annual CO2 avoided per million EUR CAPEX")
    plt.xlabel("Case / Industry")
    plt.title("Carbon Efficiency of ORC Investment")
    savefig("07_carbon_efficiency.png")

    # 3. Literature benchmark comparison table.
    benchmark = pd.DataFrame([
        {"framework": "Typical thermodynamic ORC paper", "technical_analysis": "High", "economic_analysis": "Limited / variable", "scenario_analysis": "Usually limited", "decision_support": "Limited"},
        {"framework": "Single-case feasibility study", "technical_analysis": "Medium to high", "economic_analysis": "Yes", "scenario_analysis": "Sometimes", "decision_support": "Moderate"},
        {"framework": "This V2 framework", "technical_analysis": "Uses reported technical case values", "economic_analysis": "Yes", "scenario_analysis": "Yes", "decision_support": "Stronger: NPV, break-even, risk, carbon"},
    ])
    benchmark.to_csv(RESULTS_DIR / "literature_benchmark_framework.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.axis("off")
    table = ax.table(
        cellText=benchmark.values,
        colLabels=benchmark.columns,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.6)
    plt.title("Literature Benchmark: How This Project Extends Standard ORC Feasibility Studies")
    savefig("08_literature_benchmark_table.png")

    print("V2 results and figures saved.")

if __name__ == "__main__":
    main()
