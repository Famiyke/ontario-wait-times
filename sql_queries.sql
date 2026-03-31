-- Project 4: Ontario Surgical Wait Time Analysis
-- sql_queries.sql  —  SQL Programmer Hat
-- Load ontario_waittimes.csv as table: waittimes

-- ── 1. Overall target compliance ─────────────────────────────────────────────
SELECT
    priority,
    ROUND(AVG(pct_in_target), 1)         AS avg_pct_in_target,
    ROUND(AVG(median_wait), 0)           AS avg_median_wait_days,
    ROUND(AVG(meets_target) * 100, 1)   AS pct_sites_meeting_target
FROM waittimes
GROUP BY priority
ORDER BY priority;

-- ── 2. Worst wait times by procedure (Priority 3) ────────────────────────────
SELECT
    procedure,
    ROUND(AVG(median_wait), 0)            AS avg_median_wait,
    ROUND(AVG(pct_in_target), 0)         AS pct_in_target,
    SUM(volume)                           AS total_volume
FROM waittimes
WHERE priority = 3
GROUP BY procedure
ORDER BY avg_median_wait DESC;

-- ── 3. Urban vs. rural gap ────────────────────────────────────────────────────
SELECT
    CASE WHEN urban = 1 THEN 'Urban' ELSE 'Rural/Northern' END AS location_type,
    ROUND(AVG(median_wait), 0)            AS avg_median_wait,
    ROUND(AVG(pct_in_target), 0)         AS pct_in_target,
    COUNT(DISTINCT hospital)              AS hospital_count
FROM waittimes
WHERE priority = 3
GROUP BY location_type;

-- ── 4. Year-over-year trend ───────────────────────────────────────────────────
SELECT
    year,
    ROUND(AVG(median_wait), 0)            AS avg_median_wait,
    ROUND(AVG(pct_in_target), 0)         AS avg_pct_in_target,
    SUM(volume)                           AS total_volume
FROM waittimes
WHERE priority = 3
GROUP BY year
ORDER BY year;

-- ── 5. Hospital ranking — latest year ────────────────────────────────────────
SELECT
    hospital,
    region,
    CASE WHEN urban = 1 THEN 'Urban' ELSE 'Rural' END AS location_type,
    ROUND(AVG(pct_in_target), 0)          AS avg_pct_in_target,
    ROUND(AVG(median_wait), 0)            AS avg_median_wait
FROM waittimes
WHERE year = (SELECT MAX(year) FROM waittimes)
  AND priority = 3
GROUP BY hospital, region, location_type
ORDER BY avg_pct_in_target ASC;  -- worst performers first

-- ── 6. Region-procedure worst combinations ────────────────────────────────────
SELECT
    region,
    procedure,
    ROUND(AVG(median_wait), 0)            AS avg_wait,
    ROUND(AVG(pct_in_target), 0)         AS pct_in_target
FROM waittimes
WHERE priority = 3
  AND year = (SELECT MAX(year) FROM waittimes)
GROUP BY region, procedure
ORDER BY avg_wait DESC
LIMIT 15;

-- ── 7. COVID impact — 2019 vs. 2022 vs. latest ───────────────────────────────
SELECT
    year,
    ROUND(AVG(median_wait), 0)            AS avg_wait,
    ROUND(
        (AVG(median_wait)
       - AVG(CASE WHEN year = 2019 THEN median_wait END) OVER ())
       / AVG(CASE WHEN year = 2019 THEN median_wait END) OVER () * 100
    , 1)                                   AS pct_change_from_2019
FROM waittimes
WHERE priority = 3
GROUP BY year
ORDER BY year;

-- ── 8. Facilities not meeting 90% target ─────────────────────────────────────
SELECT
    hospital,
    region,
    procedure,
    ROUND(AVG(pct_in_target), 0)         AS avg_pct_in_target,
    ROUND(AVG(median_wait), 0)            AS avg_wait_days,
    90 - ROUND(AVG(pct_in_target), 0)   AS gap_to_target
FROM waittimes
WHERE priority = 3
  AND year = (SELECT MAX(year) FROM waittimes)
GROUP BY hospital, region, procedure
HAVING avg_pct_in_target < 90
ORDER BY gap_to_target DESC;
