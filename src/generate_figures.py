"""
Generate the four figures used in the ORC investment analysis paper.
Run after financial_model.py if you want to reproduce the visual results.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from financial_model import calculate_metrics

OUT = Path("../figures")
OUT.mkdir(exist_ok=True)

prices = np.linspace(0.06, 0.24, 19)
npv_values = [calculate_metrics(p, 8000, 600000, 0.03)["npv_usd"] for p in prices]

plt.figure(figsize=(7, 4))
plt.plot(prices, [v / 1000 for v in npv_values], marker="o")
plt.axhline(0, linewidth=1)
plt.xlabel("Electricity Price (USD/kWh)")
plt.ylabel("NPV (thousand USD)")
plt.title("NPV Sensitivity to Electricity Price")
plt.tight_layout()
plt.savefig(OUT / "npv_curve.png", dpi=180)
plt.close()

scenario_results = pd.read_csv("../data/scenario_results.csv")
plt.figure(figsize=(7, 4))
plt.bar(scenario_results["scenario"], scenario_results["roi_percent"])
plt.ylabel("ROI (%)")
plt.title("ROI by Investment Scenario")
plt.tight_layout()
plt.savefig(OUT / "roi_scenarios.png", dpi=180)
plt.close()
