"""Qualitative risk register + Monte Carlo financial risk."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from utils import annual_net_cash_usd, ensure_dirs, load_config, npv_usd


def risk_register() -> pd.DataFrame:
    rows = [
        ("R1", "Technical", "ORC evaporator fouling / low source temperature", "Medium", 0.35, "HX cleaning SOP; Cu-foam compact HX (Paper 1)"),
        ("R2", "Technical", "Working-fluid regulatory phase-out", "Low", 0.20, "Low-GWP fluid selection per Paper 2 R600a benchmark"),
        ("R3", "Financial", "Electricity price volatility", "High", 0.45, "PPA hedge; sensitivity in Section 5"),
        ("R4", "Financial", "CAPEX overrun >15%", "Medium", 0.40, "EPC wrap; modular ORC skid"),
        ("R5", "Regulatory", "Carbon pricing / ETS expansion", "Medium", 0.25, "Include carbon benefit in CBA"),
        ("R6", "Market", "Competing WHP (steam cycle) for >400C sources", "Low", 0.15, "Target <150C per Paper 2 envelope"),
        ("R7", "Operational", "Insufficient annual operating hours", "High", 0.50, "Process integration audit before FID"),
        ("R8", "Operational", "Grid interconnection delay", "Medium", 0.30, "Early utility engagement"),
    ]
    return pd.DataFrame(rows, columns=["id", "category", "description", "likelihood", "impact_score", "mitigation"])


def monte_carlo_npv(cfg: dict, n: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    f = cfg["finance"]
    npvs = []
    for _ in range(n):
        c = json.loads(json.dumps(cfg))  # deep copy via json
        c["plant"]["electricity_price_usd_kWh"] *= rng.lognormal(0, 0.12)
        c["capex"]["orc_usd_per_kw"] *= rng.lognormal(0, 0.10)
        c["plant"]["annual_operating_hours"] *= rng.uniform(0.85, 1.10)
        c["plant"]["capacity_factor"] *= rng.uniform(0.90, 1.08)
        capex, cf = annual_net_cash_usd(1000, c, 100)
        npvs.append(npv_usd(capex, cf, f["project_lifetime_y"], f["discount_rate"]))
    arr = np.asarray(npvs)
    return pd.DataFrame(
        {
            "metric": ["mean", "p5", "p50", "p95", "prob_negative_npv"],
            "value": [arr.mean(), np.percentile(arr, 5), np.percentile(arr, 50), np.percentile(arr, 95), (arr < 0).mean()],
        }
    )


def main() -> None:
    data, _, rep = ensure_dirs()
    cfg = load_config()
    risk_register().to_csv(data / "risk_register.csv", index=False)
    mc = monte_carlo_npv(cfg)
    mc.to_csv(data / "risk_monte_carlo_npv.csv", index=False)
    with (rep / "risk_summary.json").open("w", encoding="utf-8") as f:
        json.dump(mc.set_index("metric")["value"].to_dict(), f, indent=2)
    print("Risk analysis complete.")


if __name__ == "__main__":
    main()
