"""Global and regional ORC waste-heat-to-power market sizing."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from utils import ensure_dirs, load_config


def market_forecast(cfg: dict) -> pd.DataFrame:
    m = cfg["market"]
    years = np.arange(m["base_year"], m["base_year"] + cfg["adoption"]["forecast_years"] + 1)
    v0 = m["global_market_usd_bn_2025"]
    g = m["cagr"]
    global_rev = v0 * (1 + g) ** (years - m["base_year"])

    china = global_rev * m["china_industrial_whr_share"]
    cement_steel_glass = china * 0.55
    addressable_twh = m["addressable_waste_heat_EJ"] * 277.78  # EJ to TWh

    return pd.DataFrame(
        {
            "year": years,
            "global_market_usd_bn": global_rev,
            "china_market_usd_bn": china,
            "core_industry_market_usd_bn": cement_steel_glass,
            "addressable_waste_heat_TWh": addressable_twh,
        }
    )


def main() -> None:
    cfg = load_config()
    data, _, rep = ensure_dirs()
    df = market_forecast(cfg)
    df.to_csv(data / "market_forecast.csv", index=False)

    summary = {
        "base_year": cfg["market"]["base_year"],
        "global_2025_usd_bn": cfg["market"]["global_market_usd_bn_2025"],
        "global_2035_usd_bn": cfg["market"]["global_market_usd_bn_2035"],
        "cagr_pct": cfg["market"]["cagr"] * 100,
        "china_share_pct": cfg["market"]["china_industrial_whr_share"] * 100,
        "sources_note": "Market CAGR from industry WHP/ORC forecasts (Research Nester, SkyQuest); calibrate with mentor data.",
    }
    with (rep / "market_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("Market sizing complete -> data/market_forecast.csv")


if __name__ == "__main__":
    main()
