"""Techno-economic cash-flow model for industrial ORC WHR plants."""

from __future__ import annotations

import pandas as pd

from utils import annual_opex_usd, annual_revenue_breakdown, ensure_dirs, load_config, plant_capex_usd


def build_plant_matrix(cfg: dict) -> pd.DataFrame:
    rows = []
    for pw in cfg["plant"]["power_kw"]:
        for t in cfg["plant"]["heat_source_temp_C"]:
            capex = plant_capex_usd(pw, cfg)
            rev = annual_revenue_breakdown(pw, cfg, t)
            total_rev = rev["total_revenue_usd"]
            opex = annual_opex_usd(capex, rev["electricity_MWh"], cfg)
            rows.append(
                {
                    "power_kw": pw,
                    "heat_source_temp_C": t,
                    "capex_usd": capex,
                    "annual_revenue_usd": total_rev,
                    "annual_opex_usd": opex,
                    "annual_net_cash_usd": total_rev - opex,
                    "electricity_MWh": rev["electricity_MWh"],
                    "mentor_steam_value_usd_per_ton": cfg["plant"]["steam_value_usd_per_ton"],
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    cfg = load_config()
    data, _, _ = ensure_dirs()
    df = build_plant_matrix(cfg)
    df.to_csv(data / "plant_techno_economic.csv", index=False)
    print("Techno-economic matrix -> data/plant_techno_economic.csv")


if __name__ == "__main__":
    main()
