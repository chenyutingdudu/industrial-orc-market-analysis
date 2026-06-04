"""
Simple ORC investment analysis model.
This file contains only the financial calculations used in the project:
revenue, ROI, NPV, payback period, scenario analysis, and sensitivity analysis.
It intentionally avoids thermodynamic modeling so the project remains focused on
business analytics and investment decision support.
"""

import math
import pandas as pd

CAPACITY_KW = 200
PROJECT_LIFE = 20
DISCOUNT_RATE = 0.08


def calculate_metrics(electricity_price, operating_hours, initial_investment, om_rate):
    annual_generation = CAPACITY_KW * operating_hours
    annual_revenue = annual_generation * electricity_price
    annual_om_cost = initial_investment * om_rate
    annual_net_cash_flow = annual_revenue - annual_om_cost
    discounted_cash_flows = [annual_net_cash_flow / ((1 + DISCOUNT_RATE) ** year) for year in range(1, PROJECT_LIFE + 1)]
    npv = sum(discounted_cash_flows) - initial_investment
    total_profit = annual_net_cash_flow * PROJECT_LIFE - initial_investment
    roi_percent = total_profit / initial_investment * 100
    payback_years = initial_investment / annual_net_cash_flow if annual_net_cash_flow > 0 else math.inf
    return {
        "annual_generation_kwh": annual_generation,
        "annual_revenue_usd": annual_revenue,
        "annual_om_cost_usd": annual_om_cost,
        "annual_net_cash_flow_usd": annual_net_cash_flow,
        "npv_usd": npv,
        "roi_percent": roi_percent,
        "payback_years": payback_years,
    }


if __name__ == "__main__":
    scenarios = pd.DataFrame([
        {"scenario": "Conservative", "electricity_price": 0.11, "operating_hours": 6000, "initial_investment": 690000, "om_rate": 0.04},
        {"scenario": "Base", "electricity_price": 0.15, "operating_hours": 8000, "initial_investment": 600000, "om_rate": 0.03},
        {"scenario": "Optimistic", "electricity_price": 0.19, "operating_hours": 8500, "initial_investment": 540000, "om_rate": 0.025},
    ])
    results = []
    for _, row in scenarios.iterrows():
        metrics = calculate_metrics(row.electricity_price, row.operating_hours, row.initial_investment, row.om_rate)
        metrics["scenario"] = row.scenario
        results.append(metrics)
    print(pd.DataFrame(results))
