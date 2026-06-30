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

## Methodology

The project follows a layered **ETL → Analysis → Presentation** pipeline:

1. **Extract \& Profile (Excel / Power Query):** Raw CSV (2,640 rows × 10 columns) ingested; column types validated; missing values catalogued (see *Data Quality* below).
2. **Transform (SQL / PostgreSQL):** Standardized schema, derived metrics, and analytical queries (ranking, year-over-year change) executed at the database layer for reproducibility and scale.
3. **Analyze (Python):** Pandas for cleaning and aggregation; Seaborn/Matplotlib for statistical visualization and correlation analysis.
4. **Present (Power BI):** A single-canvas executive dashboard with region and year slicers, designed for non-technical public-health stakeholders.

### Data Quality \& Integrity

The raw data contains the following missing values, **retained and handled transparently** rather than silently imputed:

|Column|Missing rows|
|-|-|
|`estimated\\\_incidence\\\_rate\\\_...\\\_per\\\_1\\\_000`|120|
|`estimated\\\_number\\\_of\\\_annual\\\_new\\\_hiv\\\_infections`|120|
|`estimated\\\_number\\\_of\\\_annual\\\_aids\\\_related\\\_deaths`|60|
|`estimated\\\_rate\\\_of\\\_annual\\\_aids\\\_related\\\_deaths\\\_per\\\_100\\\_000`|60|

Nulls are excluded pairwise from rate calculations and correlation analysis. No values in the source file were altered.


## Deep Dive — Five Key Insights

### 1\. Gender Disparity in New Infections : Adolescent Girls Bear \~80% of the Burden

Across 1990–2019, adolescent **girls accounted for 5,635,470 new infections** versus **1,363,340 among boys** — a **4.13:1 ratio**. On a rate basis, mean incidence was **6.16 per 1,000** for girls versus **1.35 per 1,000** for boys (**4.57:1**).

**Why it matters:** This disparity is the epidemiological signature of the AGYW vulnerability pattern. Drivers include age-disparate sexual partnerships (older male partners with higher viral prevalence), heightened biological susceptibility of immature genital mucosa, and structural gender inequities limiting negotiation of safer sex. It justifies sex-targeted interventions — oral PrEP, DREAMS-style programming, and structural support — rather than sex-neutral resource allocation.

### 2\. Geographical Hotspots : A Steep Incidence Gradient Concentrated in Southern Africa

Mean adolescent incidence rates are dominated by the Southern African cluster: **Eswatini (23.23 per 1,000)**, **Lesotho (15.89)**, **South Africa (15.85)**, **Zimbabwe (14.67)**, and **Zambia (10.12)**. At the regional level, **ESA recorded 5,719,840 new infections** against **1,278,970 in WCA** — roughly a 4.5:1 burden concentration.

**Why it matters:** Hyperendemic transmission is geographically concentrated, not diffuse. This supports **geographic prioritization** of finite prevention budgets toward the highest-incidence corridor, and signals that national averages mask sub-regional hotspots requiring district-level microtargeting.

### 3\. Temporal Trends : Declining Incidence but a Delayed, Lagging Mortality Curve

Annual adolescent new infections fell from **200,280 (1990)** to **138,760 (2019)**. AIDS-related deaths, however, **rose from 10,300 (1990) to a peak of 50,950 (2008)** before declining to **36,150 (2019)**. The mean death rate per 100,000 traces the same arc: 2.12 (1990) → 27.57 (2008) → 16.53 (2019).

**Why it matters:** The roughly 18-year lag between the infection peak and the mortality peak reflects HIV's natural history (untreated progression over roughly a decade) and the **delayed-but-real impact of antiretroviral therapy (ART)** scale-up, which accelerated after 2005. The post-2008 mortality decline is among the strongest population-level signals of treatment effectiveness in this cohort.

### 4\. Mortality vs. Prevalence : Rising Prevalence with Falling Death Rates Signals ART Success

People living with HIV (PLHIV) in this adolescent cohort grew from **436,310 (1990) to 1,523,850 (2019)** this is a 3.5-fold increase , while the mean AIDS death rate fell from its 2008 peak. The correlation between prevalence (PLHIV) and mortality rate is **positive but only moderate (r = 0.42)**.

**Why it matters:** A **rising** PLHIV count alongside a **falling** death rate is the hallmark of a maturing treatment program: people are surviving with HIV rather than dying from it. The decoupling of prevalence from mortality is precisely what successful "treatment-as-prevention" and ART coverage should produce. The moderate (not strong) correlation confirms that mortality is no longer a simple function of how many people are infected — it is mediated by treatment access.

### 5\. Risk Stratification by Sex Within the Adolescent Band

> Scope-honest note: the source contains only a single age band (10–19), so stratification here is **by sex within adolescence**, not across age groups. Within this band, female sex is the dominant risk multiplier: a **4.57× higher mean incidence rate** and concentration in the ESA region. Combining the two strongest stratifiers ; female + ESA + Southern African hotspot country and defines the highest-risk profile in the dataset.

**Why it matters:** For a health-policy context, this collapses cleanly into a deployable **RiskLevel** schema:

|RiskLevel|Profile|Indicative incidence|
|-|-|-|
|**Critical**|Female, ESA, hotspot country (Eswatini/Lesotho/South Africa)|≥ 15 per 1,000|
|**High**|Female, ESA, non-hotspot|\~6 per 1,000|
|**Moderate**|Female, WCA / Male, ESA|1–3 per 1,000|
|**Lower**|Male, WCA|< 1.5 per 1,000|

This stratification operationalizes screening cadence, PrEP eligibility triage, and resource routing.


## Visualizations

All figures are reproducible via `notebooks/generate\\\_visualizations.py` and stored in `visualizations/`.

|File|Figure|Insight|
|-|-|-|
|`fig1\\\_gender\\\_disparity\\\_lines.png`|New infections by sex over time|1|
|`fig2\\\_incidence\\\_hotspots.png`|Top-10 country incidence (hyperendemic flagged)|2|
|`fig3\\\_temporal\\\_trends.png`|Infections vs. deaths dual-axis trend|3|
|`fig4\\\_prevalence\\\_vs\\\_mortality.png`|Prevalence vs. mortality scatter|4|
|`fig5\\\_correlation\\\_matrix.png`|Indicator correlation heatmap|5|


## Repository Structure

```
.
├── data/
│   └── jan\\\_2021\\\_data\\\_viz5\\\_gender\\\_inequality\\\_and\\\_hivaids1.csv
├── sql/
│   └── analysis\\\_queries.sql
├── notebooks/
│   ├── hiv\\\_adolescent\\\_analysis.py      # Jupyter-ready analysis cells
│   └── generate\\\_visualizations.py      # reproduces all figures
├── powerbi/
│   └── dax\\\_measures.md
├── visualizations/
│   ├── fig1\\\_gender\\\_disparity\\\_lines.png
│   ├── fig2\\\_incidence\\\_hotspots.png
│   ├── fig3\\\_temporal\\\_trends.png
│   ├── fig4\\\_prevalence\\\_vs\\\_mortality.png
│   ├── fig5\\\_correlation\\\_matrix.png
│   └── VISUALIZATION\\\_KEY.md
└── README.md
```

\---

## How to Reproduce

```bash
git clone https://github.com/<your-username>/adolescent-hiv-gender-analysis.git
cd adolescent-hiv-gender-analysis
pip install pandas plotly seaborn matplotlib
python notebooks/generate\\\_visualizations.py
```

\---

## Data Source \& Citation

UNICEF / UNAIDS modeled estimates of adolescent HIV indicators (10–19), sub-Saharan Africa, 1990–2019. Figures are statistical estimates and carry uncertainty intervals not reproduced in this dataset.

## License

Released under the MIT License. See `LICENSE`.

