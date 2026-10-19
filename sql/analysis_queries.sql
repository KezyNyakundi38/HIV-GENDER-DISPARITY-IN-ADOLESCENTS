-- ============================================================
-- Adolescent HIV/AIDS Analysis - PostgreSQL Analytical Queries
-- Scope: ages 10-19, UNICEF regions ESA & WCA, 1990-2019
-- Table assumed: hiv_data (loaded from source CSV, columns verbatim)
-- ============================================================

-- ------------------------------------------------------------
-- (Optional) Reference DDL for loading the source CSV
-- ------------------------------------------------------------
-- CREATE TABLE hiv_data (
--     country                                                                       TEXT,
--     unicef_region                                                                 TEXT,
--     year                                                                          INT,
--     sex                                                                           TEXT,
--     age                                                                           TEXT,
--     estimated_incidence_rate_of_new_hiv_infection_per_1_000_uninfected_population NUMERIC,
--     estimated_number_of_annual_aids_related_deaths                                NUMERIC,
--     estimated_number_of_annual_new_hiv_infections                                 NUMERIC,
--     estimated_number_of_people_living_with_hiv                                    BIGINT,
--     estimated_rate_of_annual_aids_related_deaths_per_100_000_population           NUMERIC
-- );


-- ------------------------------------------------------------
-- QUERY 1: Top 3 countries by mean incidence rate, WITHIN each region
-- Demonstrates: RANK() window function partitioned by region.
-- Rationale: identifies regional hotspots for geographic prioritization.
-- NULL incidence rows are excluded so they do not distort the mean.
-- ------------------------------------------------------------
WITH country_incidence AS (
    SELECT
        unicef_region,
        country,
        AVG(estimated_incidence_rate_of_new_hiv_infection_per_1_000_uninfected_population)
            AS mean_incidence_rate
    FROM hiv_data
    WHERE estimated_incidence_rate_of_new_hiv_infection_per_1_000_uninfected_population IS NOT NULL
    GROUP BY unicef_region, country
),
ranked AS (
    SELECT
        unicef_region,
        country,
        ROUND(mean_incidence_rate::numeric, 2) AS mean_incidence_rate,
        RANK() OVER (
            PARTITION BY unicef_region
            ORDER BY mean_incidence_rate DESC
        ) AS region_rank
    FROM country_incidence
)
SELECT unicef_region, country, mean_incidence_rate, region_rank
FROM ranked
WHERE region_rank <= 3
ORDER BY unicef_region, region_rank;


-- ------------------------------------------------------------
-- QUERY 2: Year-over-Year (YoY) % change in global AIDS-related deaths
-- Demonstrates: CTE + LAG() window function for temporal differencing.
-- Rationale: surfaces the mortality inflection (peak ~2008, then ART-driven decline).
-- ------------------------------------------------------------
WITH annual_deaths AS (
    SELECT
        year,
        SUM(estimated_number_of_annual_aids_related_deaths) AS total_deaths
    FROM hiv_data
    WHERE estimated_number_of_annual_aids_related_deaths IS NOT NULL
    GROUP BY year
),
yoy AS (
    SELECT
        year,
        total_deaths,
        LAG(total_deaths) OVER (ORDER BY year) AS prev_year_deaths
    FROM annual_deaths
)
SELECT
    year,
    total_deaths,
    prev_year_deaths,
    ROUND(
        100.0 * (total_deaths - prev_year_deaths) / NULLIF(prev_year_deaths, 0),
        2
    ) AS yoy_pct_change
FROM yoy
ORDER BY year;


-- ------------------------------------------------------------
-- QUERY 3 (bonus): Gender Inequality Ratio by region
-- Demonstrates: conditional aggregation (FILTER) to compute a derived KPI.
-- Rationale: quantifies the female-to-male new-infection ratio per region.
-- ------------------------------------------------------------
SELECT
    unicef_region,
    SUM(estimated_number_of_annual_new_hiv_infections)
        FILTER (WHERE sex = 'Female') AS female_new_infections,
    SUM(estimated_number_of_annual_new_hiv_infections)
        FILTER (WHERE sex = 'Male')   AS male_new_infections,
    ROUND(
        SUM(estimated_number_of_annual_new_hiv_infections) FILTER (WHERE sex = 'Female')
        / NULLIF(SUM(estimated_number_of_annual_new_hiv_infections) FILTER (WHERE sex = 'Male'), 0),
        2
    ) AS gender_inequality_ratio
FROM hiv_data
WHERE estimated_number_of_annual_new_hiv_infections IS NOT NULL
GROUP BY unicef_region
ORDER BY gender_inequality_ratio DESC;
