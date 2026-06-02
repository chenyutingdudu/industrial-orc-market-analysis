from pathlib import Path
import pandas as pd
import numpy as np
from importlib.machinery import SourceFileLoader

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "orc_three_real_cases.csv"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

model = SourceFileLoader("model", str(ROOT / "src" / "01_financial_model_advanced.py")).load_module()
PROJECT_LIFE_YEARS = model.PROJECT_LIFE_YEARS
DISCOUNT_RATE = model.DISCOUNT_RATE

SCENARIOS = {
    "conservative": {"electricity_price_multiplier": 0.80, "capex_multiplier": 1.20, "power_output_multiplier": 0.90, "operating_hours_multiplier": 0.95},
    "baseline": {"electricity_price_multiplier": 1.00, "capex_multiplier": 1.00, "power_output_multiplier": 1.00, "operating_hours_multiplier": 1.00},
    "optimistic": {"electricity_price_multiplier": 1.20, "capex_multiplier": 0.85, "power_output_multiplier": 1.10, "operating_hours_multiplier": 1.05},
}

def break_even_electricity_price(row):
    power_kw = row["reported_orc_power_kw"]
    annual_generation = power_kw * row["annual_operating_hours_assumption"]
    capex = power_kw * row["capex_eur_per_kw"]
    om = capex * row["om_cost_rate"]
    required_annual_net_benefit = capex / model.annuity_factor(DISCOUNT_RATE, PROJECT_LIFE_YEARS)
    return (required_annual_net_benefit + om) / annual_generation

def main():
    df = pd.read_csv(DATA_PATH)
    scenario_records = []
    sensitivity_records = []
    break_even_records = []

    for _, row in df.iterrows():
        base = model.evaluate_case(row)
        break_even_records.append({
            "case_id": row["case_id"], "industry": row["industry"],
            "baseline_electricity_price_eur_kwh": row["electricity_price_eur_kwh_assumption"],
            "break_even_electricity_price_eur_kwh": break_even_electricity_price(row),
            "baseline_npv_eur": base["npv_eur"]
        })
        for scenario_name, multipliers in SCENARIOS.items():
            metrics = model.evaluate_case(row, **multipliers)
            scenario_records.append({
                "case_id": row["case_id"], "industry": row["industry"], "scenario": scenario_name,
                **metrics
            })
        tests = [
            ("electricity_price", "low", {"electricity_price_multiplier": 0.80}),
            ("electricity_price", "high", {"electricity_price_multiplier": 1.20}),
            ("capex", "low", {"capex_multiplier": 0.80}),
            ("capex", "high", {"capex_multiplier": 1.20}),
            ("power_output", "low", {"power_output_multiplier": 0.80}),
            ("power_output", "high", {"power_output_multiplier": 1.20}),
            ("operating_hours", "low", {"operating_hours_multiplier": 0.90}),
            ("operating_hours", "high", {"operating_hours_multiplier": 1.10}),
        ]
        for variable, direction, kwargs in tests:
            metrics = model.evaluate_case(row, **kwargs)
            sensitivity_records.append({
                "case_id": row["case_id"], "industry": row["industry"], "variable": variable, "direction": direction,
                "npv_eur": metrics["npv_eur"], "change_from_baseline_eur": metrics["npv_eur"] - base["npv_eur"],
                "change_from_baseline_percent": ((metrics["npv_eur"] - base["npv_eur"]) / abs(base["npv_eur"])) * 100 if base["npv_eur"] != 0 else np.nan
            })

    pd.DataFrame(scenario_records).to_csv(RESULTS_DIR / "scenario_results.csv", index=False)
    pd.DataFrame(sensitivity_records).to_csv(RESULTS_DIR / "sensitivity_results_advanced.csv", index=False)
    pd.DataFrame(break_even_records).to_csv(RESULTS_DIR / "break_even_prices.csv", index=False)
    print("Saved scenario, sensitivity, and break-even outputs.")

if __name__ == "__main__":
    main()
