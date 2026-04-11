# Project 1 — Tableau Dashboard Spec
## "Canada 30-Day Readmission Monitor"

### Data source
Connect to: `cihi_hospital_clean.csv`  
Set `year` as discrete dimension. Set `readmit_rate_pct` and `avg_los_days` as measures.

---

### Sheet 1 — KPI Banner (Text tiles)
- **Measure 1:** `SUM(readmissions)` → label "Total Readmissions"
- **Measure 2:** `SUM(readmissions)/SUM(separations)*100` → label "National Rate %" → format 1 decimal
- **Measure 3:** `AVG(avg_los_days)` → label "Avg Length of Stay"
- Layout: 3 tiles side by side, 28pt bold numbers

---

### Sheet 2 — Province Bar Chart
- **Type:** Horizontal bar
- **Rows:** Province (sorted descending by rate)
- **Columns:** `AVG(readmit_rate_pct)`
- **Color:** Red-green diverging on rate value
- **Reference line:** National average (dashed, labelled)
- **Tooltip:** Province, Rate, Total Readmissions, ALOS

---

### Sheet 3 — Canada Map
- **Type:** Filled map
- **Geographic field:** Province (assign Canada geography)
- **Color:** `AVG(readmit_rate_pct)` — sequential orange-red
- **Tooltip:** Province, Rate, Readmissions

---

### Sheet 4 — Diagnosis Bar Chart
- **Type:** Horizontal bar
- **Rows:** Diagnosis (sorted by rate)
- **Columns:** `AVG(readmit_rate_pct)`
- **Size:** `SUM(readmissions)` (dual axis — bar for rate, dot for volume)
- **Color:** Single accent colour; highlight top 3

---

### Sheet 5 — Year-over-Year Trend Line
- **Type:** Line chart
- **Columns:** Year (discrete)
- **Rows:** `AVG(readmit_rate_pct)`
- **Color:** Province (multi-line — or filter to top 5)
- **Annotation:** Add a band mark over 2020 labelled "COVID Disruption"

---

### Sheet 6 — Province × Diagnosis Heat Table
- **Type:** Highlight table
- **Rows:** Province
- **Columns:** Diagnosis
- **Values:** `AVG(readmit_rate_pct)`
- **Color:** Sequential — deeper red = higher risk
- **Calculated field — Risk Tier:**
```
IF AVG([readmit_rate_pct]) > 13 THEN "Critical"
ELSEIF AVG([readmit_rate_pct]) > 10 THEN "High"
ELSEIF AVG([readmit_rate_pct]) > 8  THEN "Medium"
ELSE "Standard"
END
```

---

### Dashboard Assembly  1200 × 900px
```
┌──────────────────────────────────────────┐
│  KPI Banner (Sheet 1)                    │
├────────────────────┬─────────────────────┤
│  Province Bar      │  Canada Map         │
│  (Sheet 2)         │  (Sheet 3)          │
├────────────────────┴─────────────────────┤
│  YoY Trend Line (Sheet 5)                │
├────────────────────┬─────────────────────┤
│  Diagnosis Bar     │  Heat Table         │
│  (Sheet 4)         │  (Sheet 6)          │
└────────────────────┴─────────────────────┘
```

**Dashboard-wide filters:** Year (slider), Province (multi-select), Diagnosis (dropdown)

---

### Colours
| Element | Hex |
|---------|-----|
| High risk | `#C0392B` |
| Medium | `#E67E22` |
| Low | `#27AE60` |
| Neutral | `#2C3E50` |
| Background | `#F8F6F2` |
