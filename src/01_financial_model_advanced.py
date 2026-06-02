from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "orc_three_real_cases.csv"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

PROJECT_LIFE_YEARS = 15
DISCOUNT_RATE = 0.08

def annuity_factor(rate: float, years: int) -> float:
    return sum(1 / ((1 + rate) ** year) for year in range(1, years + 1))

def calculate_npv(initial_investment: float, annual_cashflow: float, years: int = PROJECT_LIFE_YEARS, discount_rate: float = DISCOUNT_RATE) -> float:
    return -initial_investment + annual_cashflow * annuity_factor(discount_rate, years)

def discounted_cumulative_cashflow(initial_investment: float, annual_cashflow: float, years: int = PROJECT_LIFE_YEARS, discount_rate: float = DISCOUNT_RATE):
    values = [-initial_investment]
    running = -initial_investment
    for year in range(1, years + 1):
        running += annual_cashflow / ((1 + discount_rate) ** year)
        values.append(running)
    return values

def discounted_payback_year(initial_investment: float, annual_cashflow: float, years: int = PROJECT_LIFE_YEARS, discount_rate: float = DISCOUNT_RATE):
    curve = discounted_cumulative_cashflow(initial_investment, annual_cashflow, years, discount_rate)
    for year in range(1, len(curve)):
        if curve[year] >= 0:
            previous = curve[year - 1]
            current = curve[year]
            fraction = (0 - previous) / (current - previous)
            return (year - 1) + fraction
    return np.nan

def evaluate_case(row, electricity_price_multiplier=1.0, capex_multiplier=1.0, power_output_multiplier=1.0, operating_hours_multiplier=1.0):
    power_kw = row["reported_orc_power_kw"] * power_output_multiplier
    operating_hours = row["annual_operating_hours_assumption"] * operating_hours_multiplier
    annual_generation_kwh = power_kw * operating_hours
    capex_eur = power_kw * row["capex_eur_per_kw"] * capex_multiplier
    annual_om_cost_eur = capex_eur * row["om_cost_rate"]
    electricity_price = row["electricity_price_eur_kwh_assumption"] * electricity_price_multiplier
    annual_electricity_value_eur = annual_generation_kwh * electricity_price
    annual_net_benefit_eur = annual_electricity_value_eur - annual_om_cost_eur
    npv_eur = calculate_npv(capex_eur, annual_net_benefit_eur)
    simple_payback = capex_eur / annual_net_benefit_eur if annual_net_benefit_eur > 0 else np.nan
    discounted_payback = discounted_payback_year(capex_eur, annual_net_benefit_eur)
    roi_percent = (((annual_net_benefit_eur * PROJECT_LIFE_YEARS) - capex_eur) / capex_eur) * 100
    co2_tons = annual_generation_kwh * row["emission_factor_kgco2_kwh_assumption"] / 1000
    return {
        "annual_generation_kwh": annual_generation_kwh,
        "capex_eur": capex_eur,
        "annual_om_cost_eur": annual_om_cost_eur,
        "annual_electricity_value_eur": annual_electricity_value_eur,
        "annual_net_benefit_eur": annual_net_benefit_eur,
        "npv_eur": npv_eur,
        "simple_payback_years": simple_payback,
        "discounted_payback_years": discounted_payback,
        "roi_percent": roi_percent,
        "annual_co2_avoided_tons": co2_tons,
    }

def main():
    df = pd.read_csv(DATA_PATH)
    records = []
    cashflow_records = []
    for _, row in df.iterrows():
        metrics = evaluate_case(row)
        record = row.to_dict()
        record.update(metrics)
        records.append(record)
        curve = discounted_cumulative_cashflow(metrics["capex_eur"], metrics["annual_net_benefit_eur"])
        for year, value in enumerate(curve):
            cashflow_records.append({"case_id": row["case_id"], "industry": row["industry"], "year": year, "discounted_cumulative_cashflow_eur": value})
    financial = pd.DataFrame(records)
    cashflows = pd.DataFrame(cashflow_records)
    financial.to_csv(RESULTS_DIR / "financial_results_advanced.csv", index=False)
    cashflows.to_csv(RESULTS_DIR / "discounted_cashflow_curves.csv", index=False)
    print("Saved advanced financial model outputs.")

if __name__ == "__main__":
    main()
