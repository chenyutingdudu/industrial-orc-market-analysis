"""One-way tornado sensitivity on NPV."""

from __future__ import annotations

import copy

import pandas as pd

from utils import annual_net_cash_usd, ensure_dirs, load_config, npv_usd, plant_capex_usd


def baseline_npv(cfg: dict, power_kw: float = 1000, temp: float = 100) -> float:
    capex, cf = annual_net_cash_usd(power_kw, cfg, temp)
    f = cfg["finance"]
    return npv_usd(capex, cf, f["project_lifetime_y"], f["discount_rate"])


def main() -> None:
    cfg = load_config()
    data, _, _ = ensure_dirs()
    base = baseline_npv(cfg)
    rows = []
    mapping = {
        "electricity_price_usd_kWh": ("plant", "electricity_price_usd_kWh"),
        "capex_orc_usd_per_kw": ("capex", "orc_usd_per_kw"),
        "annual_operating_hours": ("plant", "annual_operating_hours"),
        "discount_rate": ("finance", "discount_rate"),
        "capacity_factor": ("plant", "capacity_factor"),
    }
    for var, (sec, key) in mapping.items():
        for pct in cfg["sensitivity"]["ranges_pct"]:
            c2 = copy.deepcopy(cfg)
            c2[sec][key] = c2[sec][key] * (1 + pct / 100.0)
            capex, cf = annual_net_cash_usd(1000, c2, 100)
            val = npv_usd(capex, cf, c2["finance"]["project_lifetime_y"], c2["finance"]["discount_rate"])
            rows.append({"variable": var, "shock_pct": pct, "npv_usd": val, "delta_npv": val - base})
    pd.DataFrame(rows).to_csv(data / "sensitivity_tornado.csv", index=False)
    print("Sensitivity complete -> data/sensitivity_tornado.csv")


if __name__ == "__main__":
    main()
