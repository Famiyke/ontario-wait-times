"""
Project 4 – simulate_waittimes.py
Builds representative Ontario surgical wait time data
modeled on Ontario Health WTIS public extracts.
Real data: https://www.ontariohealth.ca/system/reporting/wait-times
"""

import pandas as pd
import numpy as np

np.random.seed(4)

HOSPITALS = {
    "Toronto General":         {"region":"Toronto","urban":True},
    "Mount Sinai Hospital":    {"region":"Toronto","urban":True},
    "Sunnybrook HSC":          {"region":"Toronto","urban":True},
    "Ottawa Civic":            {"region":"Ottawa","urban":True},
    "Ottawa General":          {"region":"Ottawa","urban":True},
    "Hamilton General":        {"region":"Hamilton","urban":True},
    "St. Joseph's Hamilton":   {"region":"Hamilton","urban":True},
    "London Health Sciences":  {"region":"London","urban":True},
    "Kingston Health Sci.":    {"region":"Kingston","urban":False},
    "Thunder Bay Regional":    {"region":"Thunder Bay","urban":False},
    "Health Sciences North":   {"region":"Sudbury","urban":False},
    "North Bay Regional":      {"region":"North Bay","urban":False},
    "Sault Area Hospital":     {"region":"Sault Ste. Marie","urban":False},
    "Timmins District":        {"region":"Timmins","urban":False},
    "Kenora District":         {"region":"Kenora","urban":False},
}

PROCEDURES = {
    "Hip Replacement":     {"p2_target":84,"p3_target":182,"p4_target":365,"base_p3":195},
    "Knee Replacement":    {"p2_target":84,"p3_target":182,"p4_target":365,"base_p3":210},
    "Cataract Surgery":    {"p2_target":28,"p3_target":112,"p4_target":365,"base_p3":120},
    "Cancer Surgery":      {"p2_target":14,"p3_target":28, "p4_target":84, "base_p3":32},
    "Cardiac Bypass":      {"p2_target":14,"p3_target":42, "p4_target":182,"base_p3":45},
    "MRI":                 {"p2_target":28,"p3_target":84, "p4_target":180,"base_p3":95},
    "CT Scan":             {"p2_target":7, "p3_target":28, "p4_target":90, "base_p3":31},
}

YEARS     = [2018,2019,2020,2021,2022,2023]
YEAR_MULT = {2018:0.95,2019:1.00,2020:1.32,2021:1.25,2022:1.18,2023:1.08}

rows = []
for year in YEARS:
    for hosp, hinfo in HOSPITALS.items():
        for proc, pinfo in PROCEDURES.items():
            for priority in [2, 3, 4]:
                target = pinfo[f"p{priority}_target"]
                base   = pinfo["base_p3"]
                p_mult = {2: 0.55, 3: 1.00, 4: 1.45}[priority]
                rural_mult = 1.40 if not hinfo["urban"] else 1.00
                wait = max(1, int(
                    base * p_mult * rural_mult * YEAR_MULT[year]
                    + np.random.normal(0, base * 0.08)
                ))
                pct_in_target = min(98, max(20, int(
                    (target / wait) * 100 * np.random.uniform(0.85, 1.10)
                )))
                volume = max(5, int(
                    np.random.normal(
                        80 if hinfo["urban"] else 25,
                        15 if hinfo["urban"] else 8
                    )
                ))
                rows.append({
                    "year":            year,
                    "hospital":        hosp,
                    "region":          hinfo["region"],
                    "urban":           hinfo["urban"],
                    "procedure":       proc,
                    "priority":        priority,
                    "target_days":     target,
                    "median_wait":     wait,
                    "pct_in_target":   pct_in_target,
                    "volume":          volume,
                    "meets_target":    int(pct_in_target >= 90),
                })

df = pd.DataFrame(rows)
df.to_csv("ontario_waittimes.csv", index=False)
print(f"Created ontario_waittimes.csv  —  {len(df):,} rows")
print(f"Hospitals: {df['hospital'].nunique()}")
print(f"Procedures: {df['procedure'].nunique()}")
print(f"Years: {sorted(df['year'].unique())}")
