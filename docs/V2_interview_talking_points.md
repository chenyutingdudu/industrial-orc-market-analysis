# ORC V2 Interview Talking Points

## 30-Second Version

This project evaluates the financial feasibility of industrial Organic Rankine Cycle systems for waste heat recovery. I used three public industrial cases and built a Python-based techno-economic model to estimate power generation, CAPEX, O&M, NPV, ROI, payback, break-even electricity price, and CO2 reduction. In the V2 version, I extended the project into a decision-support framework by adding scenario analysis, sensitivity analysis, investment risk ranking, and carbon efficiency comparison.

## If Asked: What Is Your Contribution?

The contribution is not inventing a new ORC thermodynamic model. The contribution is building a unified, explainable decision-support framework that compares different ORC applications under the same financial assumptions.

## If Asked: Why Is This Ongoing?

I am still improving the project by adding more robust comparison metrics. The current extension focuses on ranking project risk, comparing carbon reduction efficiency, and connecting the analysis more clearly to industrial investment decisions.

## If Asked: What Did You Learn?

I learned that technical feasibility does not automatically mean investment feasibility. Electricity price, capital cost, operating hours, and project scale can strongly change the financial outcome. That is why sensitivity and break-even analysis are important.

## If Asked: Why Only Three Cases?

Because this is a case-study-based techno-economic project. The goal is interpretability and explainability rather than training a predictive model on a large dataset.

## Simple Explanation of Each V2 Chart

1. Investment dashboard: compares return, payback, ROI, and CO2 benefit.
2. Discounted cash-flow curve: shows when each case becomes financially positive.
3. Scenario NPV comparison: tests conservative, baseline, and optimistic assumptions.
4. Sensitivity heatmap: shows which assumptions affect NPV the most.
5. Break-even electricity price: shows the electricity price needed for NPV >= 0.
6. Risk ranking: shows which project is most financially sensitive.
7. Carbon efficiency: shows environmental benefit per euro invested.
8. Literature benchmark: explains how this framework extends common ORC feasibility studies.
