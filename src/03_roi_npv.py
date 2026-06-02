"""ROI, NPV, IRR, and payback for ORC WHR projects."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from utils import ensure_dirs, load_config


def npv(capex: float, annual_cf: float, years: int, rate: float) -> float:
    yrs = np.arange(1, years + 1)
    return float(np.sum(annual_cf / (1 + rate) ** yrs) - capex)


def irr(capex: float, annual_cf: float, years: int) -> float:
    def f(r):
        return npv(capex, annual_cf, years, r)

    lo, hi = -0.5, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def enrich_roi(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    f = cfg["finance"]
    out = df.copy()
    out["npv_usd"] = out.apply(
        lambda r: npv(r["capex_usd"], r["annual_net_cash_usd"], f["project_lifetime_y"], f["discount_rate"]),
        axis=1,
    )
    cf = out["annual_net_cash_usd"]
    out["payback_y"] = np.where(cf > 0, out["capex_usd"] / cf, np.inf)
    out["roi_pct"] = (
        out["annual_net_cash_usd"] * f["project_lifetime_y"] - out["capex_usd"]
    ) / out["capex_usd"] * 100
    out["irr"] = out.apply(
        lambda r: irr(r["capex_usd"], r["annual_net_cash_usd"], f["project_lifetime_y"]),
        axis=1,
    )
    return out


def main() -> None:
    cfg = load_config()
    data, _, rep = ensure_dirs()
    base = pd.read_csv(data / "plant_techno_economic.csv")
    df = enrich_roi(base, cfg)
    df.to_csv(data / "roi_analysis.csv", index=False)

    viable = df[df["annual_net_cash_usd"] > 0]
    best = viable.loc[viable["npv_usd"].idxmax()] if len(viable) else df.loc[df["npv_usd"].idxmax()]
    summary = {
        "best_case": {
            "power_kw": int(best["power_kw"]),
            "heat_source_temp_C": int(best["heat_source_temp_C"]),
            "npv_usd": round(float(best["npv_usd"]), 0),
            "payback_y": round(float(best["payback_y"]), 2),
            "roi_pct": round(float(best["roi_pct"]), 1),
            "irr": round(float(best["irr"]), 4),
        },
        "mentor_benchmark": {
            "steam_usd_per_ton": cfg["plant"]["steam_value_usd_per_ton"],
            "exergy_efficiency_pct": cfg["plant"]["exergy_efficiency_pct"],
        },
    }
    with (rep / "roi_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("ROI/NPV complete -> data/roi_analysis.csv")


if __name__ == "__main__":
    main()
