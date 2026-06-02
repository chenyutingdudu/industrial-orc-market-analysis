"""Technology adoption: Bass diffusion + industry penetration scenarios."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from utils import ensure_dirs, load_config


def bass_diffusion(cfg: dict) -> pd.DataFrame:
    a = cfg["adoption"]
    p, q = a["bass_p"], a["bass_q"]
    m = a["market_potential_units"]
    years = np.arange(0, a["forecast_years"] + 1)
    adopters = np.zeros(len(years))
    adopters[0] = 0.01 * m
    for t in range(1, len(years)):
        adopters[t] = adopters[t - 1] + (p + q * adopters[t - 1] / m) * (m - adopters[t - 1])
    installs = np.diff(adopters, prepend=0)
    return pd.DataFrame(
        {
            "year_index": years,
            "cumulative_adopters": adopters,
            "new_installations": installs,
            "penetration_pct": adopters / m * 100,
        }
    )


def industry_scenarios(cfg: dict) -> pd.DataFrame:
    industries = ["Cement", "Steel", "Glass", "Chemical", "Textile", "Non-ferrous"]
    whr_potential_gwh = [420, 680, 180, 350, 120, 90]
    orc_readiness = [0.72, 0.68, 0.55, 0.61, 0.58, 0.50]
    rows = []
    for ind, pot, ready in zip(industries, whr_potential_gwh, orc_readiness):
        rows.append(
            {
                "industry": ind,
                "waste_heat_potential_GWh_y": pot,
                "orc_readiness_index": ready,
                "addressable_gwh_y": pot * ready * cfg["market"]["china_industrial_whr_share"],
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    cfg = load_config()
    data, _, rep = ensure_dirs()
    bass = bass_diffusion(cfg)
    ind = industry_scenarios(cfg)
    bass.to_csv(data / "adoption_bass.csv", index=False)
    ind.to_csv(data / "adoption_by_industry.csv", index=False)
    with (rep / "adoption_summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "year_15_penetration_pct": float(bass["penetration_pct"].iloc[-1]),
                "total_addressable_gwh": float(ind["addressable_gwh_y"].sum()),
            },
            f,
            indent=2,
        )
    print("Adoption analysis complete.")


if __name__ == "__main__":
    main()
