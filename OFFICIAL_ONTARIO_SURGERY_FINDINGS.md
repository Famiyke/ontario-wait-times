# Ontario surgical wait times: official FAO public tables, 2019–2022

This analysis reproduces **real published aggregate surgery data**, using the Financial Accountability Office of Ontario's 2023 report and underlying data supplied by Ontario Health. It is distinct from the former synthetic hospital-level dashboard.

**Official source:** https://fao-on.org/en/report/health-2023/

## Scope and checked headline figures

| Indicator | 2019 | 2022 | Source |
|---|---:|---:|---|
| Surgeries performed, annual count | 649,299 | 555,487 | FAO Table A-1 |
| FAO estimated average surgical waiting time, months | 3.7 | 5.5 | FAO Table A-3 |
| Average surgical waitlist, persons | 199,890 | 252,986 | FAO Table A-2 |

The 2022 average waitlist is based on January to September only. The FAO wait-time measure is an **estimate based on waitlist size and surgical throughput**, NOT a direct distribution of patient-level Wait 2 times.

## Reproducibility and validation

The extraction parses the original HTML tables **A-1, A-2 and A-3**, rather than using simulated numbers. It checks the presence of all 22 reported service areas plus the total row, verifies expected official total surgery counts and wait-month figures, and writes 276 source-linked records (23 areas including the total, four years, three measures).

```bash
pip install requests beautifulsoup4
python official_ontario_fao_surgery.py
```

The original `ontario_waittimes.csv` and Tableau report show a **synthetic hospital-level scenario**, not these FAO public aggregates. Do not use the simulated facility rankings to make clinical or hospital-performance comparisons.

## Limitations

- Source edition is **2023** and the last year analysed is **2022**. These values do not represent 2026 wait times.
- The annual FAO estimated wait measure is based on aggregate waitlists and surgical activity, not directly observed patient wait experiences, procedure priority or risk-adjusted case mix.
- Hospital-level rankings cannot be inferred from these aggregate service-area tables.
- The 2022 waitlist summary uses nine months, not a complete calendar-year average.
- The percentage changes supplied in the FAO report may not equal changes computed from its one-decimal rounded estimates.
- This is descriptive reporting, not an analysis of intervention impact or causal effects.
