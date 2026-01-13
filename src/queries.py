queries = {

"Rice Trend Top 3": """
WITH rice_year_state AS (
    SELECT state_name, year, SUM(rice_production_1000_tons) AS rice_production
    FROM agri_data_1
    GROUP BY state_name, year
),
top_states AS (
    SELECT state_name
    FROM rice_year_state
    GROUP BY state_name
    ORDER BY SUM(rice_production) DESC
    LIMIT 3
)
SELECT r.year, r.state_name, r.rice_production
FROM rice_year_state r
JOIN top_states t ON r.state_name = t.state_name
ORDER BY r.year, r.state_name;
""",

"Wheat Yield Growth": """
WITH years AS (SELECT MAX(year) AS max_year FROM agri_data_1),
wheat AS (
    SELECT dist_name, year, AVG(wheat_yield_kg_per_ha) AS y
    FROM agri_data_1, years
    WHERE year IN (max_year, max_year - 5)
    GROUP BY dist_name, year
),
p AS (
    SELECT dist_name,
    MAX(CASE WHEN year = (SELECT max_year FROM years) THEN y END) AS latest,
    MAX(CASE WHEN year = (SELECT max_year FROM years)-5 THEN y END) AS old
    FROM wheat
    GROUP BY dist_name
)
SELECT dist_name, old, latest, (latest-old) AS increase
FROM p
ORDER BY increase DESC
LIMIT 5;
""",

"Oilseed Growth 5 Year": """
WITH years AS (SELECT MAX(year) AS max_year FROM agri_data_1),
oilseed AS (
    SELECT state_name, year, SUM(oilseeds_production_1000_tons) AS prod
    FROM agri_data_1, years
    WHERE year IN (max_year, max_year - 5)
    GROUP BY state_name, year
),
pivoted AS (
    SELECT state_name,
           MAX(CASE WHEN year = (SELECT max_year FROM years) THEN prod END) AS latest,
           MAX(CASE WHEN year = (SELECT max_year FROM years)-5 THEN prod END) AS old
    FROM oilseed
    GROUP BY state_name
)
SELECT state_name, old, latest,
       ((latest - old)/old)*100 AS growth_rate_percent
FROM pivoted
WHERE old > 0
ORDER BY growth_rate_percent DESC;
""",

"Groundnut 2017": """
SELECT dist_name,
       SUM(groundnut_production_1000_tons) AS groundnut_production
FROM agri_data_1
WHERE year = 2017
GROUP BY dist_name
ORDER BY groundnut_production DESC
LIMIT 10;
""",

"Maize Yield Trend": """
SELECT year,
       AVG(maize_yield_kg_per_ha) AS avg_maize_yield
FROM agri_data_1
GROUP BY year
ORDER BY year;
""",

"Oilseed Area by State": """
SELECT state_name,
       SUM(oilseeds_area_1000_ha) AS total_oilseed_area
FROM agri_data_1
GROUP BY state_name
ORDER BY total_oilseed_area DESC;
""",

"Top Rice Yield Districts": """
SELECT dist_name,
       AVG(rice_yield_kg_per_ha) AS avg_rice_yield
FROM agri_data_1
GROUP BY dist_name
ORDER BY avg_rice_yield DESC
LIMIT 10;
""",

"Wheat vs Rice Top States": """
WITH top_states AS (
    SELECT state_name
    FROM agri_data_1
    GROUP BY state_name
    ORDER BY SUM(rice_production_1000_tons + wheat_production_1000_tons) DESC
    LIMIT 5
),
years AS (SELECT MAX(year) AS max_year FROM agri_data_1)
SELECT a.year, a.state_name,
       SUM(a.rice_production_1000_tons) AS rice,
       SUM(a.wheat_production_1000_tons) AS wheat
FROM agri_data_1 a, years
WHERE a.state_name IN (SELECT state_name FROM top_states)
  AND a.year >= max_year - 10
GROUP BY a.year, a.state_name
ORDER BY a.year, a.state_name;
"""
}
