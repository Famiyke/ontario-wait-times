# Ontario surgical wait times: official FAO public tables, 2019–2022

The analysis uses published surgery aggregates from the Financial Accountability Office of Ontario’s 2023 report, based on data supplied by Ontario Health.

**Official source:** https://fao-on.org/en/report/health-2023/

## Scope and checked headline figures

| Indicator | 2019 | 2022 | Source |
|---|---:|---:|---|
| Surgeries performed, annual count | 649,299 | 555,487 | FAO Table A-1 |
| FAO estimated average surgical waiting time, months | 3.7 | 5.5 | FAO Table A-3 |
| Average surgical waitlist, persons | 199,890 | 252,986 | FAO Table A-2 |

The 2022 average waitlist is based on January to September only. The FAO wait-time measure is an **estimate based on waitlist size and surgical throughput**. It describes the aggregate estimated wait, rather than the distribution of individual Wait 2 times.

## Reproducibility and validation

The extraction reads the original HTML tables A-1, A-2 and A-3. It checks the presence of all 22 reported service areas plus the total row, verifies expected official total surgery counts and wait-month figures, and writes 276 source-linked records (23 areas including the total, four years, three measures).

```bash
pip install requests beautifulsoup4
python official_ontario_fao_surgery.py
```

To reproduce the extraction from a saved report, run `python official_ontario_fao_surgery.py --source path/to/report.html`. The earlier facility-level Tableau scenario uses simulated data and is retained separately.

## Limitations

- Source edition is **2023** and the last year analysed is **2022**. These values do not represent 2026 wait times.
- The annual FAO estimated wait measure is based on aggregate waitlists and surgical activity, not directly observed patient wait experiences, procedure priority or risk-adjusted case mix.
- Hospital-level rankings cannot be inferred from these aggregate service-area tables.
- The 2022 waitlist summary uses nine months, not a complete calendar-year average.
- The percentage changes supplied in the FAO report may not equal changes computed from its one-decimal rounded estimates.
- This is descriptive reporting, not an analysis of intervention impact or causal effects.
