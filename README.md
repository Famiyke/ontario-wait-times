# Project 4: Ontario Surgical Wait Time Analysis

> **DATA PROVENANCE:** This portfolio project uses simulated records informed by named Canadian public sources. All generated statistics, rankings, demographic differences, and savings models are illustrative rather than verified official estimates. Recommendations are hypothetical scenarios, not observed effects.

**Domain:** Health System Performance / Access to Care
**Tools:** Python · SQL · Tableau
**Public reference source (distinct from simulated analysis data):** Ontario Health — Wait Times Results
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

## Illustrative analytical outputs

This project's Python/SQL outputs illustrate data processing, comparisons, modeling and reporting using generated records. The specific rates, rankings, cost figures and trends in the demonstration are **not verified official findings**. See the analysis scripts for the computations and the data limitations section below for interpretation requirements.

## Interpretation and real-world next steps

Use the simulated findings to demonstrate analytical methods, not to rank actual jurisdictions or recommend clinical or policy interventions. A real decision requires matched official data, documented definitions, relevant uncertainty, and clinical or operational stakeholder review. Financial scenarios must include assumptions, costs and sensitivity analysis.

## Files

| File | Purpose |
|------|---------|
| `simulate_waittimes.py` | Builds representative hospital-level wait time data anchored to Ontario Health published statistics |
| `analysis.py` | Data cleaning, profiling, urban-rural analysis, hospital ranking, trend analysis, recommendations |
| `sql_queries.sql` | 8 SQL queries covering compliance, rankings, COVID impact, and below-target facilities |
| `ontario_waittimes.csv` | Generated dataset — 630 records, 15 hospitals, 7 procedures, 2018–2023 |
| `Dashboard.md` | Link to live Tableau Public dashboard |

---

## Data Provenance and Limitations

The 15-hospital dataset is simulated. Rankings, wait-time compliance, the urban-rural gap, and COVID effects should not be attributed to real facilities. Confirm Ontario Health definitions and benchmark years before interpreting source data.

Patient-level wait time data is classified as personal health information under PHIPA and is not publicly releasable by Ontario Health. This project uses simulated data anchored to published Ontario Health aggregate wait time statistics. The analytical methodology reflects the approach used in real health system performance analysis roles.





---

## Reproducibility and execution status

**Environment:** Python 3 with `pandas` and `numpy` installed. If working with the Excel files, install `openpyxl` as needed. Run the simulation script before the analysis commands shown above.

**Important:** The scripts are designed for the generated datasets and expected column names. Downloading a public government table does **not** guarantee that it will run with these scripts unchanged; a schema-mapping and validation step is required for authentic external data. The repository has undergone a static documentation and code-reference audit, but a fresh environment execution and independent reconciliation with official datasets have not yet been completed.

