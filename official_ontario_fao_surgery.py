"""Reproduce published Ontario surgery aggregate tables from the FAO report.

Official public report: Financial Accountability Office of Ontario,
Health Sector Spending Plan Review (2023).
https://fao-on.org/en/report/health-2023/

Table A-1: annual surgeries performed (observed reported aggregates)
Table A-2: average surgical waitlist (2022 Jan–Sep only)
Table A-3: FAO-estimated months of surgical waiting (Little's Law proxy)

These are real published tables based on data provided by Ontario Health,
not the previous fictional hospital-level performance dataset.
"""
import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup

URL = "https://fao-on.org/en/report/health-2023/"
OUTPUT = Path("official_ontario_fao_surgery_2019_2022.csv")
REPORT = Path("OFFICIAL_ONTARIO_SURGERY_FINDINGS.md")
TABLES = {
    "A-1": ("surgeries_performed", "count"),
    "A-2": ("average_waitlist", "count"),
    "A-3": ("fao_estimated_wait_months", "months"),
}


def clean_number(v):
    return float(v.replace(",", "").replace("−", "-").strip())


def main():
    response = requests.get(URL, timeout=50, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    page = BeautifulSoup(response.text, "html.parser")
    tables = page.find_all("table")
    output = []
    by_table = {}
    for table_id, (metric, unit) in TABLES.items():
        matches = [table for table in tables
                   if table.get_text(" ", strip=True).startswith(f"Table {table_id} ")]
        assert len(matches) == 1, f"Could not uniquely locate official {table_id}"
        table = matches[0]
        entries = {}
        for tr in table.find_all("tr"):
            values = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
            if len(values) < 6 or values[0] in ("Service Area", ""):
                continue
            try:
                numbers = [clean_number(v) for v in values[1:5]]
            except ValueError:
                continue
            area = values[0]
            assert area not in entries, f"Duplicate service area {table_id}: {area}"
            entries[area] = numbers
            reported = values[5]
            for year, val in zip((2019, 2020, 2021, 2022), numbers):
                output.append({
                    "service_area": area,
                    "year": year,
                    "metric": metric,
                    "value": int(val) if unit == "count" else val,
                    "unit": unit,
                    "source_table": table_id,
                    "fao_reported_change_2019_to_2022": reported,
                    "source_publisher": "Financial Accountability Office of Ontario",
                    "source_url": URL
                })
        assert len(entries) == 23, f"Expected 22 service areas + total in {table_id}; got {len(entries)}"
        assert "Total" in entries and "General Surgery" in entries
        by_table[table_id] = entries
    assert len(output) == 23 * 4 * 3
    assert by_table["A-1"]["Total"] == [649299, 461785, 532241, 555487]
    assert by_table["A-3"]["Total"] == [3.7, 5.4, 5.1, 5.5]
    assert by_table["A-3"]["General Surgery"] == [2.7, 4.1, 4.3, 4.9]
    assert by_table["A-2"]["Total"][0] == 199890
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    surgeries = by_table["A-1"]["Total"]
    waits = by_table["A-3"]["Total"]
    report = f"""# Ontario surgical wait times: official FAO public tables, 2019–2022

This analysis reproduces **real published aggregate surgery data**, using the Financial Accountability Office of Ontario's 2023 report and underlying data supplied by Ontario Health. It is distinct from the former synthetic hospital-level dashboard.

**Official source:** {URL}

## Scope and checked headline figures

| Indicator | 2019 | 2022 | Source |
|---|---:|---:|---|
| Surgeries performed, annual count | {surgeries[0]:,} | {surgeries[3]:,} | FAO Table A-1 |
| FAO estimated average surgical waiting time, months | {waits[0]:.1f} | {waits[3]:.1f} | FAO Table A-3 |
| Average surgical waitlist, persons | {by_table['A-2']['Total'][0]:,} | {by_table['A-2']['Total'][3]:,} | FAO Table A-2 |

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
"""
    REPORT.write_text(report, encoding="utf-8")
    print(f"PASS: {len(output)} real official FAO table observations")
    print(f"2019 and 2022 total surgeries: {surgeries[0]}, {surgeries[3]}")
    print(f"2019 and 2022 FAO estimated wait months: {waits[0]}, {waits[3]}")
    print(f"Wrote {OUTPUT} and {REPORT}")


if __name__ == "__main__":
    main()
