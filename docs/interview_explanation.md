# Interview Explanation

## 30-Second Version

My project evaluates whether industrial Organic Rankine Cycle systems are financially attractive for waste heat recovery. Instead of generating a fake large dataset, I used three public case studies: an industrial kiln ORC case in Belgium, a cement plant waste heat recovery case, and a steel electric arc furnace ORC case. I then built a simple techno-economic model to calculate annual power generation value, CAPEX, O&M, NPV, ROI, and payback period. Finally, I tested how sensitive profitability is to electricity price, ORC capital cost, and recoverable waste heat.

## If Asked: Where Did the Data Come From?

The data came from public literature and industry case summaries. The project does not claim to have proprietary plant-level data. The contribution is a unified evaluation framework that puts three real ORC cases into the same financial model.

## If Asked: What Was Your Main Finding?

The main finding is that ORC feasibility is strongly driven by project scale, electricity price, and capital cost. Larger continuous industrial heat sources, such as cement and steel applications, are more likely to achieve attractive payback periods than smaller systems unless policy incentives or high electricity prices are available.

## If Asked: Why Only Three Cases?

Because this is a case-study-based techno-economic project. The goal is depth and interpretability, not training a predictive model. With three cases, I can explain every input, every assumption, and every result clearly.