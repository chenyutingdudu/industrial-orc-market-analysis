"""Cost-benefit analysis (CBA): NPV, BCR, societal CO2 benefit."""

from __future__ import annotations

import pandas as pd

from utils import ensure_dirs, load_config


def co2_avoided_tons(electricity_mwh: float, grid_factor_kg_per_kwh: float = 0.55) -> float:
    return electricity_mwh * 1000 * grid_factor_kg_per_kwh / 1000.0


def main() -> None:
    cfg = load_config()
    data, _, _ = ensure_dirs()
    df = pd.read_csv(data / "roi_analysis.csv")
    social_carbon_usd_per_ton = 45.0

    df["co2_avoided_tons_y"] = df["electricity_MWh"].apply(co2_avoided_tons)
    df["carbon_benefit_usd_y"] = df["co2_avoided_tons_y"] * social_carbon_usd_per_ton
    df["benefit_cost_ratio"] = (df["annual_revenue_usd"] + df["carbon_benefit_usd_y"]) / df[
        "annual_opex_usd"
    ].clip(lower=1)
    df["societal_npv_usd"] = df["npv_usd"] + df["carbon_benefit_usd_y"].sum() * 0.1  # simplified

    df.to_csv(data / "cost_benefit_analysis.csv", index=False)
    print("Cost-benefit complete -> data/cost_benefit_analysis.csv")


if __name__ == "__main__":
    main()
