"""
ORC Investment Analysis - Interview Version
Author: Yuting Chen

This script calculates:
1. Annual electricity generation
2. Annual revenue
3. Annual O&M cost
4. Annual net cash flow
5. NPV
6. ROI
7. Payback period
8. Scenario analysis
9. Sensitivity analysis
10. Simple interview-ready figures
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("../figures")
DATA_DIR = Path("../data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

CAPACITY_KW = 200
PROJECT_LIFE = 20
DISCOUNT_RATE = 0.08

SCENARIOS = pd.DataFrame([
    {"Scenario": "Conservative", "Electricity_Price_USD_per_kWh": 0.11, "Operating_Hours": 6000, "Initial_Investment_USD": 690000, "OM_Rate": 0.040},
    {"Scenario": "Base", "Electricity_Price_USD_per_kWh": 0.15, "Operating_Hours": 8000, "Initial_Investment_USD": 600000, "OM_Rate": 0.030},
    {"Scenario": "Optimistic", "Electricity_Price_USD_per_kWh": 0.19, "Operating_Hours": 8500, "Initial_Investment_USD": 540000, "OM_Rate": 0.025},
])

def calculate_npv(annual_cash_flow, discount_rate, project_life, initial_investment):
    """NPV = present value of future cash flows - initial investment."""
    present_value = 0
    for year in range(1, project_life + 1):
        present_value += annual_cash_flow / ((1 + discount_rate) ** year)
    return present_value - initial_investment

def evaluate_orc_case(row):
    """Calculate financial metrics for one ORC investment case."""
    annual_generation = CAPACITY_KW * row["Operating_Hours"]
    annual_revenue = annual_generation * row["Electricity_Price_USD_per_kWh"]
    annual_om_cost = row["Initial_Investment_USD"] * row["OM_Rate"]
    annual_net_cf = annual_revenue - annual_om_cost

    npv_value = calculate_npv(
        annual_cash_flow=annual_net_cf,
        discount_rate=DISCOUNT_RATE,
        project_life=PROJECT_LIFE,
        initial_investment=row["Initial_Investment_USD"]
    )

    total_profit = annual_net_cf * PROJECT_LIFE - row["Initial_Investment_USD"]
    roi_percent = total_profit / row["Initial_Investment_USD"] * 100
    payback_years = row["Initial_Investment_USD"] / annual_net_cf

    return pd.Series({
        "Annual_Generation_kWh": annual_generation,
        "Annual_Revenue_USD": annual_revenue,
        "Annual_OM_Cost_USD": annual_om_cost,
        "Annual_Net_CF_USD": annual_net_cf,
        "NPV_USD": npv_value,
        "ROI_percent": roi_percent,
        "Payback_Years": payback_years
    })

def main():
    results = pd.concat([SCENARIOS, SCENARIOS.apply(evaluate_orc_case, axis=1)], axis=1)
    results.to_csv(DATA_DIR / "orc_scenario_results.csv", index=False)
    print(results[["Scenario", "Annual_Revenue_USD", "Annual_Net_CF_USD", "NPV_USD", "ROI_percent", "Payback_Years"]])

    base_case = SCENARIOS[SCENARIOS["Scenario"] == "Base"].iloc[0].copy()
    base_result = results[results["Scenario"] == "Base"].iloc[0]

    # Figure 1: NPV sensitivity to electricity price
    prices = np.linspace(0.06, 0.24, 19)
    npvs = []
    for price in prices:
        temp = base_case.copy()
        temp["Electricity_Price_USD_per_kWh"] = price
        npvs.append(evaluate_orc_case(temp)["NPV_USD"] / 1000)

    plt.figure(figsize=(8, 5))
    plt.plot(prices, npvs, marker="o")
    plt.axhline(0, linewidth=1)
    plt.title("NPV Sensitivity to Electricity Price")
    plt.xlabel("Electricity price (USD/kWh)")
    plt.ylabel("NPV (thousand USD)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "figure_1_npv_sensitivity_price.png", dpi=200)
    plt.close()

    # Figure 2: ROI by scenario
    plt.figure(figsize=(8, 5))
    plt.bar(results["Scenario"], results["ROI_percent"])
    plt.title("ROI by Investment Scenario")
    plt.xlabel("Scenario")
    plt.ylabel("ROI (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "figure_2_roi_by_scenario.png", dpi=200)
    plt.close()

    # Figure 3: Sensitivity analysis
    variables = [
        ("Electricity Price", "Electricity_Price_USD_per_kWh"),
        ("Operating Hours", "Operating_Hours"),
        ("Capital Cost", "Initial_Investment_USD"),
        ("O&M Rate", "OM_Rate"),
    ]
    sensitivity_rows = []
    for label, col in variables:
        low = base_case.copy()
        high = base_case.copy()
        low[col] *= 0.8
        high[col] *= 1.2
        low_npv = evaluate_orc_case(low)["NPV_USD"]
        high_npv = evaluate_orc_case(high)["NPV_USD"]
        sensitivity_rows.append({"Variable": label, "Low_NPV_USD": low_npv, "High_NPV_USD": high_npv})

    sensitivity = pd.DataFrame(sensitivity_rows)
    sensitivity.to_csv(DATA_DIR / "orc_sensitivity_results.csv", index=False)

    plt.figure(figsize=(8, 5))
    y = np.arange(len(sensitivity))
    for i, row in sensitivity.iterrows():
        xmin = min(row["Low_NPV_USD"], row["High_NPV_USD"]) / 1000
        xmax = max(row["Low_NPV_USD"], row["High_NPV_USD"]) / 1000
        plt.barh(i, xmax - xmin, left=xmin)
    plt.axvline(base_result["NPV_USD"] / 1000, linewidth=1)
    plt.yticks(y, sensitivity["Variable"])
    plt.title("Sensitivity Analysis Tornado Chart")
    plt.xlabel("NPV under +/-20% change (thousand USD)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "figure_3_sensitivity_tornado.png", dpi=200)
    plt.close()

    # Figure 4: Discounted cumulative cash flow
    annual_cf = base_result["Annual_Net_CF_USD"]
    initial = base_case["Initial_Investment_USD"]
    years = np.arange(1, PROJECT_LIFE + 1)
    cumulative = []
    for year in years:
        cumulative_value = -initial + sum(annual_cf / ((1 + DISCOUNT_RATE) ** t) for t in range(1, year + 1))
        cumulative.append(cumulative_value)

    cashflow = pd.DataFrame({"Year": years, "Cumulative_Discounted_CF_USD": cumulative})
    cashflow.to_csv(DATA_DIR / "orc_discounted_cashflow_curve.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(years, np.array(cumulative) / 1000, marker="o")
    plt.axhline(0, linewidth=1)
    plt.title("Discounted Cash Flow Curve")
    plt.xlabel("Project year")
    plt.ylabel("Cumulative discounted cash flow (thousand USD)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "figure_4_discounted_cash_flow.png", dpi=200)
    plt.close()

if __name__ == "__main__":
    main()
