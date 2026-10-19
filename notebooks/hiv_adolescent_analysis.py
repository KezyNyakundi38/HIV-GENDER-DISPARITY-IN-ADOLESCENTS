# %% [markdown]
# # Adolescent HIV/AIDS in Sub-Saharan Africa - Analysis
# Scope: ages 10-19, UNICEF regions ESA & WCA, 1990-2019.
# Each `# %%` block is a Jupyter cell.

# %% Imports & cohesive clinical palette
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

CLINICAL = {
    "female": "#C2185B",   # alert magenta - high-vulnerability group (AGYW)
    "male":   "#00838F",   # clinical teal
    "accent": "#1565C0",   # clinical blue
    "alert":  "#D32F2F",   # high-risk red
    "muted":  "#90A4AE",
}
sns.set_theme(style="whitegrid", context="talk")

# %% Load
df = pd.read_csv("../data/jan_2021_data_viz5_gender_inequality_and_hivaids1.csv")

# %% Cleaning
# Standardize column names (already snake_case; strip whitespace defensively).
df.columns = df.columns.str.strip().str.lower()

# Short, analysis-friendly aliases for the verbose epidemiological columns.
df = df.rename(columns={
    "estimated_incidence_rate_of_new_hiv_infection_per_1_000_uninfected_population": "incidence_rate",
    "estimated_number_of_annual_aids_related_deaths": "aids_deaths",
    "estimated_number_of_annual_new_hiv_infections": "new_infections",
    "estimated_number_of_people_living_with_hiv": "plhiv",
    "estimated_rate_of_annual_aids_related_deaths_per_100_000_population": "death_rate",
})

# Missing values are retained as NaN and excluded pairwise per metric, rather
# than imputed - imputing modeled epidemiological estimates would fabricate signal.
print("Missing value footprint:\n", df.isna().sum(), "\n")

# %% Insight 1 - Gender disparity in new infections (Plotly line)
sex_year = (df.dropna(subset=["new_infections"])
              .groupby(["year", "sex"], as_index=False)["new_infections"].sum())

fig1 = px.line(
    sex_year, x="year", y="new_infections", color="sex",
    color_discrete_map={"Female": CLINICAL["female"], "Male": CLINICAL["male"]},
    markers=True,
    labels={"new_infections": "New HIV Infections (annual)", "year": "Year", "sex": "Sex"},
    title="Adolescent (10-19) New HIV Infections by Sex, 1990-2019",
)
fig1.update_layout(template="plotly_white", legend_title_text="Sex", font=dict(size=14))
fig1.show()

# %% Insight 4 - Prevalence vs mortality rate (Plotly scatter)
scatter_df = df.dropna(subset=["plhiv", "death_rate", "incidence_rate"])
fig2 = px.scatter(
    scatter_df, x="plhiv", y="death_rate",
    color="sex", size="incidence_rate", size_max=22, opacity=0.55,
    color_discrete_map={"Female": CLINICAL["female"], "Male": CLINICAL["male"]},
    labels={"plhiv": "People Living with HIV (prevalence)",
            "death_rate": "AIDS Death Rate (per 100,000)",
            "incidence_rate": "Incidence /1,000"},
    title="Prevalence vs. AIDS Mortality Rate (bubble = incidence rate)",
)
fig2.update_layout(template="plotly_white", font=dict(size=14))
fig2.show()

# %% Correlation matrix (Seaborn heatmap)
corr_cols = ["incidence_rate", "new_infections", "aids_deaths", "plhiv", "death_rate"]
corr = df[corr_cols].corr()
plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="mako_r", vmin=-1, vmax=1,
            linewidths=.5, cbar_kws={"label": "Pearson r"})
plt.title("Correlation Matrix - Adolescent HIV Indicators", pad=14)
plt.tight_layout()
plt.show()

# %% Headline figures (printed for the README)
g = df.groupby("sex")["new_infections"].sum()
print(f"New infections  F={int(g['Female']):,}  M={int(g['Male']):,}  ratio={g['Female']/g['Male']:.2f}")
si = df.groupby("sex")["incidence_rate"].mean()
print(f"Mean incidence  F={si['Female']:.2f}  M={si['Male']:.2f}  ratio={si['Female']/si['Male']:.2f}")
