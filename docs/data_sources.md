# Data Sources and Modeling Notes

## Important Explanation

This project does **not** claim to use a proprietary dataset of many factories.  
It uses three public ORC / waste heat recovery cases as representative industrial scenarios.

The CSV contains two kinds of variables:

1. **Reported case variables**  
   These come from published papers or public industry reports, such as reported ORC power output, industry, location, and reported efficiency when available.

2. **Modeling assumptions**  
   These are used to make the three cases comparable in one financial model, including operating hours, electricity price, O&M rate, and emissions factor.

This is normal for techno-economic analysis because public case papers often report different levels of detail.

---

## Case 1: Industrial Kiln ORC, Flanders, Belgium

Source:
- Lemmens et al., *Case study of an organic Rankine cycle applied for excess heat recovery: Technical, economic and policy matters*, Energy Conversion and Management, 2017.
- Related cost engineering summary: *Cost Engineering Techniques and Their Applicability for Cost Estimation of Organic Rankine Cycle Systems*, Energies, 2016.

Reported public values used:
- 375 kW gross ORC system
- Flue gas heat recovery from an industrial kiln
- Flanders, Belgium
- Specific investment cost: 4216 EUR/kW gross

Source URLs:
- https://www.sciencedirect.com/science/article/abs/pii/S0196890417300936
- https://www.mdpi.com/1996-1073/9/7/485

---

## Case 2: Cement Plant Waste Heat Recovery, Greece

Source:
- Karellas et al., *Energetic and exergetic analysis of waste heat recovery systems in the cement industry*, Energy, 2013.

Reported public values used:
- Typical cement WHR can offer about 6 MW of electric power
- Rotary kiln exhaust gases around 380C
- Clinker cooler hot air around 360C
- ORC system efficiency: 17.56%
- Industrial electricity price: about 100 EUR/MWh
- Specific capital cost range: 1500–3000 EUR/kW
- O&M cost: 3% of capital cost

Source URL:
- https://www.aspire2050.eu/sites/default/files/users/user222/Epos-docs/Energetic%20and%20exergetic%20analysis%20of%20waste%20heat%20recovery%20systems%20in%20the%20cement%20industry.pdf

---

## Case 3: Steel Electric Arc Furnace ORC, Germany

Source:
- AIST article on the first EAF waste heat recovery ORC-based system.
- Ja'fari et al., *Waste heat recovery in iron and steel industry using organic Rankine cycles*, Chemical Engineering Journal, 2023.

Reported public values used:
- Around 3 MW electrical output ORC unit
- Electric arc furnace waste heat recovery
- German steel plant
- Steel ORC review supports ORC as a suitable technology for power generation and carbon reduction in iron and steel waste heat recovery.

Source URLs:
- https://www.aist.org/first-eaf-waste-heat-recovery-orc-based-system-now-in-operation-at-german-steel-plant
- https://www.sciencedirect.com/science/article/pii/S1385894723056565

---

## Financial Modeling Assumptions

The following assumptions are not claimed as direct measurements from each plant:

- Annual operating hours:
  - 7500 hours for continuous kiln/cement operation
  - 6500 hours for EAF steel operation due to more intermittent process characteristics

- Electricity price:
  - 0.10 EUR/kWh baseline, aligned with the cement paper's 100 EUR/MWh value.

- Emissions factor:
  - 0.40 kg CO2/kWh as a simplified grid displacement assumption.
  - For a more detailed environmental paper, this could be replaced with country-specific grid factors.

- Discount rate:
  - 8%

- Project life:
  - 15 years

These assumptions are intentionally simple so the project remains explainable in interviews.