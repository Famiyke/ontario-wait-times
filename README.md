# Project 4: Ontario Surgical Wait Time Analysis

**Domain:** Health System Performance / Access to Care
**Tools:** Python · SQL · Tableau
**Real Data Source:** Ontario Health — Wait Times Results
**Download:** https://www.ontariohealth.ca/system/reporting/wait-times/wait-times-results
(Free — filter by procedure and click "Download CSV")

---

## Business Question
Which surgical procedures and hospitals have the longest wait times in Ontario, are wait times improving or worsening, and which regions show the largest access gaps between urban and rural patients?

---

## How to Get the Real Data
1. Go to: https://www.ontariohealth.ca/system/reporting/wait-times/wait-times-results
2. Select: Procedure → All, Hospital → All, Year → All available
3. Click **Download (csv)** button on the page
4. Rename file: `ontario_waittimes.csv`
5. Place in this folder

## How to Run (demo mode)
```bash
pip install pandas numpy
python simulate_waittimes.py   # creates ontario_waittimes.csv (~630 records)
python analysis.py             # full analysis with cleaning, rankings, recommendations
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Profiled Ontario Health wait time records, checked for missing values and out-of-range compliance rates, handled "LV" (low volume) suppression codes, validated priority level coding across all hospitals and procedures |
| SQL/Python Programmer | Ranked hospitals by compliance, measured target achievement rates, identified worst-performing procedure-region combinations, quantified the urban-rural gap |
| Dashboard Architect | Built Tableau Public dashboard with compliance heat map, hospital ranking, year-over-year trend with COVID annotation, and below-90% filter |
| Data Storyteller | Produced a patient access brief for a regional health planning team |
| Strategic Consultant | Recommended capacity rebalancing and mobile surgical team deployment for northern Ontario |

---

## Live Dashboard
[Ontario Surgical Wait Times — Health Analytics Dashboard](https://public.tableau.com/app/profile/ikenna.nwogu/viz/OntarioSurgicalWaitTimesHealthAnalyticsDashboard/ONTARIOSURGICALWAITTIMES-HEALTHANALYTICSDASHBOARD)

**Views included:**
- KPI cards: Hospitals meeting 90% target, average compliance rate, wait time change 2018 vs 2023
- Target compliance heat map by hospital and procedure
- Hospital compliance ranking — Priority 3
- Median wait time trend 2018–2023 with COVID-19 spike annotation
- Hospitals below 90% compliance target

---

## Key Findings

1. **Northern access gap.** Hip and knee replacement wait times in northern Ontario average 31% longer than in Toronto for the same Priority 3 level. Rural hospitals average 23 percentage points lower compliance than urban hospitals.

2. **Widespread target failure.** Overall Priority 3 compliance averages 80% — below the 90% provincial target. 11 of 15 hospitals fall below the 90% benchmark.

3. **COVID recovery near-complete.** COVID-19 caused a 15 percentage point compliance drop in 2020. Near-full recovery by 2023, now only 1.2pp below the pre-COVID baseline — but northern hospitals have recovered more slowly than urban ones.

4. **Procedure variation.** Hip and knee replacement show the longest median wait times. MRI and CT Scan show greater variation by region, with northern hospitals disproportionately affected.

---

## Strategic Recommendations

1. **Deploy mobile surgical teams to northern Ontario.** Kenora, Timmins, and North Bay show the lowest compliance rates. Quarterly mobile orthopaedic teams would reduce the northern access gap without requiring permanent facility investment.

2. **Publish real-time hospital compliance dashboards.** Ontario Health should make hospital-level compliance data publicly available on a rolling 90-day basis to create accountability pressure and help patients make informed referral decisions.

3. **Structured COVID backlog program.** Despite near-full recovery at the provincial level, individual hospitals — particularly in the north — have not returned to pre-COVID performance. A targeted backlog reduction program with hospital-specific timelines is needed.

---

## Files

| File | Purpose |
|------|---------|
| `simulate_waittimes.py` | Builds representative hospital-level wait time data anchored to Ontario Health published statistics |
| `analysis.py` | Data cleaning, profiling, urban-rural analysis, hospital ranking, trend analysis, recommendations |
| `sql_queries.sql` | 8 SQL queries covering compliance, rankings, COVID impact, and below-target facilities |
| `ontario_waittimes.csv` | Generated dataset — 630 records, 15 hospitals, 7 procedures, 2018–2023 |
| `Dashboard.md` | Link to live Tableau Public dashboard |

---

## Data Note
Patient-level wait time data is classified as personal health information under PHIPA and is not publicly releasable by Ontario Health. This project uses simulated data anchored to published Ontario Health aggregate wait time statistics. The analytical methodology reflects the approach used in real health system performance analysis roles.
