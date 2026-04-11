"""
Project 4 – simulate_waittimes.py
Generates representative Ontario surgical wait time data
anchored to published Ontario Health statistics.
Real data: https://www.ontariohealth.ca/system-performance/wait-times

Urban high-performing hospitals (Toronto, Ottawa core) average 90%+ compliance.
Rural/Northern hospitals average 60-65% compliance.
COVID-19 impact modelled for 2020-2021.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

HOSPITALS = {
    # Urban high performers — meet 90% target on average
    'Toronto General':    {'region': 'Toronto',          'urban': True,  'performance': 'high'},
    'Sunnybrook HSC':     {'region': 'Toronto',          'urban': True,  'performance': 'high'},
    'Mount Sinai Hos.':   {'region': 'Toronto',          'urban': True,  'performance': 'high'},
    'Ottawa Civic':       {'region': 'Ottawa',           'urban': True,  'performance': 'high'},
    # Urban medium performers — below 90% on average
    'Ottawa General':     {'region': 'Ottawa',           'urban': True,  'performance': 'medium'},
    'Hamilton General':   {'region': 'Hamilton',         'urban': True,  'performance': 'medium'},
    'St Josephs Ham.':    {'region': 'Hamilton',         'urban': True,  'performance': 'medium'},
    'London Health S.':   {'region': 'London',           'urban': True,  'performance': 'medium'},
    'Kingston Health':    {'region': 'Kingston',         'urban': True,  'performance': 'medium'},
    'Health Sciences':    {'region': 'Hamilton',         'urban': True,  'performance': 'medium'},
    # Rural/Northern — well below 90% target
    'Thunder Bay Reg.':   {'region': 'Thunder Bay',      'urban': False, 'performance': 'low'},
    'Sault Area Hospi.':  {'region': 'Sault Ste Marie',  'urban': False, 'performance': 'low'},
    'North Bay Regio.':   {'region': 'North Bay',        'urban': False, 'performance': 'low'},
    'Timmins District':   {'region': 'Timmins',          'urban': False, 'performance': 'low'},
    'Kenora District':    {'region': 'Kenora',           'urban': False, 'performance': 'low'},
}

PROCEDURES = [
    'Cancer Surgery',
    'Cardiac Bypass',
    'Cataract Surgery',
    'CT Scan',
    'Hip Replacement',
    'Knee Replacement',
    'MRI',
]

YEARS = [2018, 2019, 2020, 2021, 2022, 2023]

# Ontario Health Priority 3 target: 84 days
TARGET_DAYS = 84

# Base compliance rates anchored to published Ontario Health wait time reports
# Source: Ontario Health Wait Time targets and provincial summaries
BASE_COMPLIANCE = {
    'high':   {'mean': 97, 'std': 3},   # Average ~93% across all years including COVID
    'medium': {'mean': 87, 'std': 4},   # Average ~84%
    'low':    {'mean': 68, 'std': 6},   # Average ~64%
}

# Procedure-level adjustments — some procedures easier to hit targets for
PROC_ADJUSTMENT = {
    'Cancer Surgery':    +3,
    'Cardiac Bypass':    +2,
    'Cataract Surgery':  +5,
    'CT Scan':           +4,
    'Hip Replacement':   -2,
    'Knee Replacement':  -3,
    'MRI':               +1,
}

# Year adjustments — COVID-19 impact on surgical volumes and wait times
# Source: Ontario Health COVID-19 impact reports
YEAR_ADJUSTMENT = {
    2018:  0,
    2019: +1,
    2020: -15,   # COVID-19 surgical cancellations
    2021:  -8,   # Partial recovery
    2022:  -3,   # Continued backlog
    2023:  -1,   # Near recovery
}

rows = []
for hosp, info in HOSPITALS.items():
    perf = info['performance']
    base_mean = BASE_COMPLIANCE[perf]['mean']
    base_std  = BASE_COMPLIANCE[perf]['std']

    for proc in PROCEDURES:
        proc_adj = PROC_ADJUSTMENT[proc]

        for yr in YEARS:
            yr_adj = YEAR_ADJUSTMENT[yr]

            pct = round(max(0, min(100,
                base_mean + proc_adj + yr_adj +
                np.random.normal(0, base_std)
            )), 1)

            # Median wait derived from compliance rate
            wait = round(
                TARGET_DAYS * (1 + (90 - pct) / 100) *
                np.random.uniform(0.9, 1.1), 0
            )

            rows.append({
                'hospital':      hosp,
                'region':        info['region'],
                'urban':         info['urban'],
                'procedure':     proc,
                'year':          yr,
                'priority':      3,
                'median_wait':   wait,
                'pct_in_target': pct,
                'meets_target':  int(pct >= 90),
                'volume':        np.random.randint(80, 600),
            })

df = pd.DataFrame(rows)
df.to_csv('ontario_waittimes.csv', index=False)

print(f"Created ontario_waittimes.csv  —  {len(df):,} rows")
print(f"Hospitals: {df['hospital'].nunique()}")
print(f"Procedures: {df['procedure'].nunique()}")
print(f"Years: {sorted(df['year'].unique())}")

print("\nHospital compliance averages:")
hosp_avg = (df.groupby(['hospital', 'urban'])['pct_in_target']
              .mean().round(1).reset_index()
              .sort_values('pct_in_target', ascending=False))
for _, r in hosp_avg.iterrows():
    flag = " MEETS 90+" if r['pct_in_target'] >= 90 else " below 90"
    print(f"  {r['hospital']:<22} urban={str(r['urban']):<5}  {r['pct_in_target']}%  {flag}")

print(f"\nHospitals meeting 90% on average: {(hosp_avg.pct_in_target >= 90).sum()}")
print(f"Hospitals below 90% on average:  {(hosp_avg.pct_in_target < 90).sum()}")
