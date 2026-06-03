# Advanced Interview Talking Points

## What changed in this advanced version?

The first version only showed baseline NPV, payback, and one simple sensitivity chart. This version adds deeper but still explainable business analytics:

1. Scenario analysis: conservative, baseline, and optimistic cases.
2. Discounted cash-flow curves: shows when the investment becomes positive after discounting future cash flows.
3. Break-even electricity price: shows what electricity price is needed for the project to achieve NPV >= 0.
4. Sensitivity heatmap: shows which assumptions change NPV the most across the three ORC cases.
5. Investment dashboard: compares return, payback, ROI, and CO2 benefit together.

## Simple explanation for interviews

I wanted to avoid making the project look like just three bar charts. So I extended it into a small decision-support framework. First, I calculated baseline financial metrics for each ORC case. Then I asked: would the same conclusion still hold if electricity price is lower, CAPEX is higher, or recoverable heat is lower? That is why I added scenario testing, sensitivity analysis, break-even price analysis, and discounted cash-flow curves.

## Main finding

Cement and steel cases look more attractive mainly because they are larger-scale industrial heat sources. The kiln case is smaller, so its payback is longer and its NPV is more fragile. Across the three cases, electricity price and CAPEX are the most important business drivers.

## Why this is still explainable

The project does not use complicated black-box machine learning. Every chart comes from the same simple financial logic: annual generation, annual revenue, CAPEX, O&M cost, discounted cash flow, and NPV. This makes it easier to defend in a PhD or research interview.
