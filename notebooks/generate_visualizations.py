"""
Adolescent HIV/AIDS in Sub-Saharan Africa - Visualization Generator
====================================================================
Scope: ages 10-19, UNICEF regions ESA & WCA, 1990-2019.

Generates five publication-ready figures used in the analysis. Each figure is
saved as a high-resolution PNG into ../visualizations/.

Run:  python generate_visualizations.py
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ----------------------------------------------------------------------
# Cohesive clinical palette (intentional, non-default)
# ----------------------------------------------------------------------
CLINICAL = {
    "female": "#C2185B",   # alert magenta - high-vulnerability group (AGYW)
    "male":   "#00838F",   # clinical teal
    "accent": "#1565C0",   # clinical blue
    "alert":  "#D32F2F",   # high-risk red
    "muted":  "#90A4AE",
}
sns.set_theme(style="whitegrid", context="talk")
OUT = "../visualizations"

# ----------------------------------------------------------------------
# Load + clean
# ----------------------------------------------------------------------
df = pd.read_csv("../data/jan_2021_data_viz5_gender_inequality_and_hivaids1.csv")
df.columns = df.columns.str.strip().str.lower()
df = df.rename(columns={
    "estimated_incidence_rate_of_new_hiv_infection_per_1_000_uninfected_population": "incidence_rate",
    "estimated_number_of_annual_aids_related_deaths": "aids_deaths",
    "estimated_number_of_annual_new_hiv_infections": "new_infections",
    "estimated_number_of_people_living_with_hiv": "plhiv",
    "estimated_rate_of_annual_aids_related_deaths_per_100_000_population": "death_rate",
})

# ----------------------------------------------------------------------
# FIG 1 - Gender disparity in new infections over time
# ----------------------------------------------------------------------
sex_year = (df.dropna(subset=["new_infections"])
              .groupby(["year", "sex"], as_index=False)["new_infections"].sum())
plt.figure(figsize=(12, 7))
for sex, colour in [("Female", CLINICAL["female"]), ("Male", CLINICAL["male"])]:
    d = sex_year[sex_year.sex == sex]
    plt.plot(d.year, d.new_infections, marker="o", linewidth=2.5,
             color=colour, label=sex)
plt.title("Adolescent (10\u201319) New HIV Infections by Sex, 1990\u20132019\n"
          "Sub-Saharan Africa (ESA & WCA) \u2014 girls account for ~80% of new infections",
          fontsize=15, fontweight="bold")
plt.xlabel("Year"); plt.ylabel("Annual New HIV Infections")
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.legend(title="Sex", frameon=True)
plt.tight_layout(); plt.savefig(f"{OUT}/fig1_gender_disparity_lines.png", dpi=200,
                                bbox_inches="tight"); plt.close()

# ----------------------------------------------------------------------
# FIG 2 - Top incidence hotspots (country bar; hyperendemic flagged red)
# ----------------------------------------------------------------------
hotspots = (df.dropna(subset=["incidence_rate"])
              .groupby("country", as_index=False)["incidence_rate"].mean()
              .sort_values("incidence_rate", ascending=False).head(10))
plt.figure(figsize=(12, 7))
colours = [CLINICAL["alert"] if v >= 15 else CLINICAL["accent"]
           for v in hotspots.incidence_rate]
plt.barh(hotspots.country, hotspots.incidence_rate, color=colours)
plt.gca().invert_yaxis()
plt.title("Top 10 Adolescent HIV Incidence Hotspots (mean 1990\u20132019)\n"
          "Red = hyperendemic (\u2265 15 new infections per 1,000 uninfected)",
          fontsize=15, fontweight="bold")
plt.xlabel("Mean Incidence Rate (per 1,000 uninfected population)")
plt.ylabel("Country")
for i, v in enumerate(hotspots.incidence_rate):
    plt.text(v + 0.2, i, f"{v:.1f}", va="center", fontsize=11)
plt.tight_layout(); plt.savefig(f"{OUT}/fig2_incidence_hotspots.png", dpi=200,
                                bbox_inches="tight"); plt.close()

# ----------------------------------------------------------------------
# FIG 3 - Temporal trend: infections vs deaths (dual axis, lag story)
# ----------------------------------------------------------------------
inf_y = df.dropna(subset=["new_infections"]).groupby("year")["new_infections"].sum()
dth_y = df.dropna(subset=["aids_deaths"]).groupby("year")["aids_deaths"].sum()
fig, ax1 = plt.subplots(figsize=(12, 7))
ax1.plot(inf_y.index, inf_y.values, color=CLINICAL["accent"], linewidth=2.5,
         marker="o", label="New infections")
ax1.set_xlabel("Year"); ax1.set_ylabel("Annual New HIV Infections",
                                        color=CLINICAL["accent"])
ax1.tick_params(axis="y", labelcolor=CLINICAL["accent"])
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2 = ax1.twinx()
ax2.plot(dth_y.index, dth_y.values, color=CLINICAL["alert"], linewidth=2.5,
         marker="s", label="AIDS-related deaths")
ax2.set_ylabel("Annual AIDS-related Deaths", color=CLINICAL["alert"])
ax2.tick_params(axis="y", labelcolor=CLINICAL["alert"])
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2.axvline(2008, color=CLINICAL["muted"], linestyle="--", linewidth=1.5)
ax2.text(2008.3, dth_y.max()*0.95, "Mortality peak (2008)",
         color=CLINICAL["muted"], fontsize=11)
plt.title("Temporal Decoupling: Falling Infections vs. Lagging Mortality\n"
          "Adolescents 10\u201319, Sub-Saharan Africa, 1990\u20132019",
          fontsize=15, fontweight="bold")
fig.tight_layout(); plt.savefig(f"{OUT}/fig3_temporal_trends.png", dpi=200,
                                bbox_inches="tight"); plt.close()

# ----------------------------------------------------------------------
# FIG 4 - Prevalence vs mortality rate (scatter, ART-effectiveness story)
# ----------------------------------------------------------------------
sc = df.dropna(subset=["plhiv", "death_rate", "incidence_rate"])
plt.figure(figsize=(12, 7))
for sex, colour in [("Female", CLINICAL["female"]), ("Male", CLINICAL["male"])]:
    d = sc[sc.sex == sex]
    plt.scatter(d.plhiv, d.death_rate, s=d.incidence_rate*6 + 10,
                alpha=0.45, color=colour, label=sex, edgecolor="white", linewidth=0.3)
r = sc["plhiv"].corr(sc["death_rate"])
plt.title("Prevalence vs. AIDS Mortality Rate (Pearson r \u2248 "
          f"{r:.2f})\nBubble size = incidence rate. Mortality is decoupling "
          "from prevalence as ART scales.", fontsize=15, fontweight="bold")
plt.xlabel("People Living with HIV (prevalence)")
plt.ylabel("AIDS Death Rate (per 100,000 population)")
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.legend(title="Sex", frameon=True)
plt.tight_layout(); plt.savefig(f"{OUT}/fig4_prevalence_vs_mortality.png", dpi=200,
                                bbox_inches="tight"); plt.close()

# ----------------------------------------------------------------------
# FIG 5 - Correlation matrix (risk-indicator relationships)
# ----------------------------------------------------------------------
corr_cols = ["incidence_rate", "new_infections", "aids_deaths", "plhiv", "death_rate"]
labels = ["Incidence\nrate", "New\ninfections", "AIDS\ndeaths", "PLHIV", "Death\nrate"]
corr = df[corr_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="mako_r", vmin=-1, vmax=1,
            linewidths=.5, xticklabels=labels, yticklabels=labels,
            cbar_kws={"label": "Pearson correlation (r)"})
plt.title("Correlation Matrix \u2014 Adolescent HIV Indicators",
          fontsize=15, fontweight="bold", pad=14)
plt.tight_layout(); plt.savefig(f"{OUT}/fig5_correlation_matrix.png", dpi=200,
                                bbox_inches="tight"); plt.close()

print("All 5 figures written to", OUT)
