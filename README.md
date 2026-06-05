
## What this package contains

- `src/orc_investment_analysis.py`  
  Main Python script that calculates the formulas and generates charts.

- `data/orc_scenario_assumptions.csv`  
  Conservative, base, and optimistic scenario assumptions.

- `data/orc_scenario_results.csv`  
  Calculated annual revenue, net cash flow, NPV, ROI, and payback period.

- `data/orc_sensitivity_results.csv`  
  Sensitivity analysis results using +/-20% changes.

- `data/orc_discounted_cashflow_curve.csv`  
  Cumulative discounted cash flow by year.

- `data/orc_interview_formula_summary.csv`  
  Simple formula explanations for interview preparation.

- `figures/`  
  Four simple charts:
  1. NPV sensitivity to electricity price
  2. ROI by investment scenario
  3. Sensitivity tornado chart
  4. Discounted cash flow curve

## How to run

```bash
cd src
python orc_investment_analysis.py
```



The project converts a technical ORC waste heat recovery idea into a financial decision model.  
The key logic is:

1. Estimate annual electricity generation:
   installed capacity × operating hours

2. Estimate annual revenue:
   annual electricity generation × electricity price

3. Subtract annual O&M cost:
   initial investment × O&M rate

4. Calculate financial attractiveness:
   NPV, ROI, and payback period

5. Test uncertainty:
   compare conservative, base, and optimistic scenarios; then change each key variable by +/-20%.

The main conclusion is that electricity price, operating hours, and capital cost are the most important drivers of ORC investment value.
