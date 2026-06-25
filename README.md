# HIV-GENDER-DISPARITY-IN-ADOLESCENTS
Epidemiological analysis of sex-based HIV risk among  adolescents in sub-Saharan Africa using SQL, Python and PowerBI
# HIV-GENDER-DISPARITY-IN-ADOLESCENTS
Executive Summary
This repository presents an end-to-end epidemiological analysis of HIV incidence, prevalence, and AIDS-related mortality among adolescents aged 10–19 across 44 countries in two UNICEF sub-Saharan African regions — Eastern and Southern Africa (ESA) and West and Central Africa (WCA) — covering the period 1990–2019.
The central finding is a profound and persistent sex-based disparity: adolescent girls accounted for 5,635,470 new HIV infections versus 1,363,340 among adolescent boys over the study period — a 4.13:1 female-to-male ratio in absolute new infections, and a 4.57:1 ratio in mean incidence rate per 1,000 uninfected population. This is not a statistical artifact; it reflects well-documented structural, biological, and behavioral drivers of HIV vulnerability in adolescent girls and young women (AGYW), a population designated as a priority demographic by UNAIDS and PEPFAR.
The analysis is intended as both a public-health narrative and a technical demonstration, spanning ETL, SQL window-function analytics, Python statistical visualization, and Power BI dashboarding.
> Scope note (read me before interpreting): This dataset is restricted to the 10–19 age band and to two African UNICEF regions. All findings are specific to adolescents in sub-Saharan Africa and must NOT be generalized to adults or to global populations. Figures are modeled estimates (UNAIDS/UNICEF methodology), not direct case counts.
## Tech Stack

|Layer|Tooling|Purpose|
|-|-|-|
|**Ingestion \& Cleaning**|Excel **Power Query (M)**|Initial profiling, type coercion, null inspection|
|**Data Wrangling**|**SQL (PostgreSQL)**|Window functions, CTEs, ranked aggregations|
|**Analysis \& Visualization**|**Python** — Pandas, Plotly, Seaborn, Matplotlib|Statistical analysis, publication-ready charts|
|**Business Intelligence**|**Power BI** (DAX + M)|Interactive stakeholder dashboard|

\---
