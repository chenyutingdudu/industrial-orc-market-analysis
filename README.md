# Techno-Economic Feasibility and Decision-Support Modeling of Industrial ORC Systems

This is an ongoing research-style business analytics project evaluating whether industrial Organic Rankine Cycle (ORC) systems are financially and environmentally attractive for waste heat recovery.

The project uses three public ORC / waste heat recovery cases as representative industrial scenarios:

1. Industrial kiln ORC case in Flanders, Belgium
2. Cement plant waste heat recovery case
3. Steel electric arc furnace ORC case in Germany

## Research Goal

The goal is not to design a new ORC thermodynamic cycle. Instead, the project builds an explainable decision-support framework that compares multiple industrial ORC applications under a unified set of financial assumptions.

## What the Model Evaluates

The project estimates:

- Annual electricity generation
- CAPEX and O&M cost
- Annual net benefit
- Net Present Value (NPV)
- ROI
- Simple and discounted payback period
- Break-even electricity price
- Conservative / baseline / optimistic scenario outcomes
- NPV sensitivity to electricity price, CAPEX, power output, and operating hours
- Investment risk ranking
- Carbon efficiency: CO2 reduction per million EUR invested

## V2 Additions

This V2 version adds three interview-friendly but more research-oriented extensions:

1. **Investment Risk Ranking**  
   Uses sensitivity analysis to identify which ORC case is most financially fragile.

2. **Carbon Efficiency Analysis**  
   Compares annual CO2 avoided per million EUR of CAPEX.

3. **Literature Benchmark Framework**  
   Positions the project as a unified decision-support model rather than only a one-case feasibility calculation.

## Main Finding

Larger and more continuous heat sources, such as cement and steel applications, are more financially attractive than smaller kiln systems. Across cases, electricity price and capital cost are the strongest drivers of investment feasibility. The cement case has the strongest financial performance, while smaller systems are more sensitive to market and cost assumptions.

## How to Run

```bash
pip install -r requirements.txt
python src/run_all.py
```

Outputs will be saved in:

- `results/`
- `figures/`

## Suggested Interview Explanation

I am currently extending the project from a simple techno-economic analysis into a decision-support framework for industrial ORC investments. Besides NPV, ROI, and payback, I added scenario analysis, break-even electricity price analysis, investment risk ranking, and sustainability metrics. The goal is to evaluate how robust project feasibility remains under different operating and market conditions.

## Project Positioning

This project is best described as:

**Techno-economic feasibility + decision-support modeling + sustainability analytics**

It is especially relevant to research areas such as:

- Energy systems modeling
- Data-driven engineering analysis
- Industrial decarbonization
- Sustainable technology adoption
- Decision analytics for engineering systems
