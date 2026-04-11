# Project 4: Ontario Surgical Wait Time Analysis

**Domain:** Health System Performance / Telehealth  
**Tools:** Python · SQL · Tableau  
**Real Data Source:** Ontario Health — Wait Times Results  
**Download:** https://www.ontariohealth.ca/system/reporting/wait-times/wait-times-results  
(Free — filter by procedure and click "Download CSV")

---

## Business Question
Which surgical procedures and hospitals have the longest wait times in Ontario, are wait times improving or worsening, and which regions show the largest access gaps?

---

## How to Get the Real Data
1. Go to: https://www.ontariohealth.ca/system/reporting/wait-times/wait-times-results
2. Select: Procedure → All, Hospital → All, Year → All available
3. Click **Download (csv)** button on the page
4. Rename file: `ontario_waittimes.csv`
5. Place in this folder

## How to Run (demo mode)
```bash
pip install pandas numpy openpyxl
python simulate_waittimes.py   # creates ontario_waittimes.csv
python 01_clean_explore.py     # data detective
python 02_analysis.py          # full analysis
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Profiled Ontario Health wait time records, handled "LV" (low volume) suppression codes, validated priority level coding |
| SQL/Python Programmer | Ranked hospitals, measured target compliance, identified worst-performing procedure-region pairs |
| Tableau dashboard | https://public.tableau.com/app/profile/ikenna.nwogu/viz/OntarioSurgicalWaitTimesHealthAnalyticsDashboard/ONTARIOSURGICALWAITTIMES-HEALTHANALYTICSDASHBOARD |
| Data Storyteller | Produced a patient access brief for a regional health team |
| Strategic Consultant | Recommended capacity rebalancing across three LHIN regions |

---

## Key Findings
1. Hip and knee replacement wait times in northern Ontario are 40% longer than in Toronto for the same priority level.
2. Only 62% of Priority 3 patients receive care within the provincial target time.
3. Wait times worsened from 2020 to 2022 and have not recovered to pre-COVID benchmarks.
