#!/usr/bin/env python3
"""Execute full ORC WHR economic feasibility pipeline."""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

MODULES = [
    "01_market_sizing",
    "02_techno_economic_model",
    "03_roi_npv",
    "04_cost_benefit",
    "05_sensitivity",
    "06_adoption_analysis",
    "07_risk_analysis",
]


def main() -> None:
    for name in MODULES:
        print(f"\n>>> Running {name}...")
        importlib.import_module(name).main()
    print("\n>>> Generating figures...")
    importlib.import_module("generate_figures").main()
    print("\n=== All analyses complete. See data/, figures/, reports/ ===")


if __name__ == "__main__":
    main()
