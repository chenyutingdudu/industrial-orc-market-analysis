"""Shared utilities for ORC WHR economic feasibility package."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict:
    path = ROOT / "config" / "assumptions.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def plant_capex_usd(power_kw: float, cfg: dict) -> float:
    c = cfg["capex"]
    base = power_kw * c["orc_usd_per_kw"]
    return base * (1 + c["balance_of_plant_pct"] + c["installation_pct"] + c["cu_foam_hx_premium_pct"])


def annual_electricity_kwh(power_kw: float, cfg: dict) -> float:
    p = cfg["plant"]
    return power_kw * p["annual_operating_hours"] * p["capacity_factor"]


def annual_revenue_breakdown(power_kw: float, cfg: dict, temp_c: float = 100) -> dict:
    p = cfg["plant"]
    elec_kwh = annual_electricity_kwh(power_kw, cfg)
    temp_bonus = 1.0 + 0.003 * (temp_c - 100)
    elec_rev = elec_kwh * p["electricity_price_usd_kWh"]
    steam_tons = power_kw * p["steam_tons_per_kw_year"]
    steam_rev = steam_tons * p["steam_value_usd_per_ton"]
    total = (elec_rev + steam_rev) * temp_bonus
    return {
        "electricity_kWh": elec_kwh,
        "electricity_MWh": elec_kwh / 1000.0,
        "electricity_revenue_usd": elec_rev * temp_bonus,
        "steam_revenue_usd": steam_rev * temp_bonus,
        "total_revenue_usd": total,
        "steam_tons_y": steam_tons,
    }


def annual_opex_usd(capex: float, elec_mwh: float, cfg: dict) -> float:
    o = cfg["opex"]
    return capex * o["fixed_pct_capex"] + elec_mwh * o["variable_usd_per_MWh"]


def annual_net_cash_usd(power_kw: float, cfg: dict, temp_c: float = 100) -> tuple[float, float]:
    rev = annual_revenue_breakdown(power_kw, cfg, temp_c)
    capex = plant_capex_usd(power_kw, cfg)
    opex = annual_opex_usd(capex, rev["electricity_MWh"], cfg)
    return capex, rev["total_revenue_usd"] - opex


def npv_usd(capex: float, annual_cf: float, years: int, rate: float) -> float:
    import numpy as np

    yrs = np.arange(1, years + 1)
    return float(np.sum(annual_cf / (1 + rate) ** yrs) - capex)


def ensure_dirs() -> tuple[Path, Path, Path]:
    data = ROOT / "data"
    fig = ROOT / "figures"
    rep = ROOT / "reports"
    for p in (data, fig, rep):
        p.mkdir(parents=True, exist_ok=True)
    return data, fig, rep
