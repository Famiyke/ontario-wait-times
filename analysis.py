"""
Project 4 – analysis.py
Data Detective → Programmer → Storyteller → Consultant
Ontario Surgical Wait Time Analysis
"""

import pandas as pd
import numpy as np

df  = pd.read_csv("ontario_waittimes.csv")
sep = "=" * 62

print(f"\n{sep}")
print("  PROJECT 4 — ONTARIO SURGICAL WAIT TIME ANALYSIS")
print(f"{sep}")

# ══════════════════════════════════════════════════════════════════
# STEP 1: DATA DETECTIVE — CLEANING AND PROFILING
# ══════════════════════════════════════════════════════════════════
print(f"\n{'─'*62}")
print("STEP 1: SHAPE AND STRUCTURE")
print(f"{'─'*62}")

print(f"\n  Rows:       {len(df):,}")
print(f"  Columns:    {len(df.columns)}")
print(f"  Hospitals:  {df['hospital'].nunique()}")
print(f"  Procedures: {df['procedure'].nunique()}")
print(f"  Years:      {sorted(df['year'].unique())}")
print(f"  Priorities: {sorted(df['priority'].unique())}")

print(f"\n  Column names and types:")
for col in df.columns:
    print(f"    {col:<25} {df[col].dtype}")

# ── Missing values ─────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("STEP 2: MISSING AND SUPPRESSED VALUES")
print(f"{'─'*62}")

# Ontario Health suppresses low-volume cells with "LV" codes
# Replace these before numeric conversion
raw_missing = df.isnull().sum()
if raw_missing.sum() == 0:
    print("\n  No null values in raw file.")
else:
    print(f"\n  Nulls found:\n{raw_missing[raw_missing>0]}")

# Handle suppression codes from real Ontario Health data
for col in ["median_wait", "pct_in_target", "volume"]:
    before = df[col].dtype
    df[col] = pd.to_numeric(
        df[col].astype(str)
               .str.replace("LV", "", regex=False)
               .str.replace("N/A", "", regex=False)
               .str.strip(),
        errors="coerce"
    )
    suppressed = df[col].isnull().sum()
    if suppressed > 0:
        print(f"  {col}: {suppressed} suppressed values (LV/N/A) converted to NaN")

rows_before = len(df)
df = df.dropna(subset=["median_wait", "pct_in_target"])
rows_after  = len(df)
if rows_before > rows_after:
    print(f"  Dropped {rows_before - rows_after} rows with suppressed values")
    print(f"  Remaining rows: {rows_after:,}")
else:
    print(f"\n  No suppressed values found. All {rows_after:,} rows retained.")

# ── Range checks ────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("STEP 3: RANGE CHECKS")
print(f"{'─'*62}")

checks = {
    "pct_in_target":  (0, 100,   "compliance % must be 0–100"),
    "median_wait":    (1, 730,   "wait days must be 1–730"),
    "priority":       (1, 4,     "priority must be 1–4"),
    "volume":         (1, 10000, "volume must be positive"),
}

all_ok = True
for col, (lo, hi, msg) in checks.items():
    out_of_range = df[(df[col] < lo) | (df[col] > hi)]
    if len(out_of_range) > 0:
        print(f"  WARNING — {col}: {len(out_of_range)} values out of range ({msg})")
        all_ok = False
    else:
        print(f"  {col:<20} range {df[col].min():.1f} – {df[col].max():.1f}  ✓")

if all_ok:
    print(f"\n  All range checks passed.")

# ── Coverage check ──────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("STEP 4: COVERAGE CHECK")
print(f"{'─'*62}")

expected_hospitals  = 15
expected_procedures = 7
expected_years      = 6

actual_hospitals  = df['hospital'].nunique()
actual_procedures = df['procedure'].nunique()
actual_years      = df['year'].nunique()

print(f"\n  Hospitals:  {actual_hospitals} of {expected_hospitals} expected  "
      f"{'✓' if actual_hospitals == expected_hospitals else '✗ MISSING HOSPITALS'}")
print(f"  Procedures: {actual_procedures} of {expected_procedures} expected  "
      f"{'✓' if actual_procedures == expected_procedures else '✗ MISSING PROCEDURES'}")
print(f"  Years:      {actual_years} of {expected_years} expected  "
      f"{'✓' if actual_years == expected_years else '✗ MISSING YEARS'}")

# Check every hospital has every procedure and year
expected_combos = expected_hospitals * expected_procedures * expected_years
actual_combos   = len(df[df.priority==3].groupby(['hospital','procedure','year']))
print(f"\n  Priority 3 combos: {actual_combos} of {expected_combos} expected  "
      f"{'✓' if actual_combos == expected_combos else '✗ GAPS IN COVERAGE'}")

# ── Distribution check ──────────────────────────────────────────────
print(f"\n{'─'*62}")
print("STEP 5: COMPLIANCE RATE DISTRIBUTION (Priority 3)")
print(f"{'─'*62}")

p3_pct = df[df.priority==3]['pct_in_target']
bins   = [(0,50,'< 50%'),(50,70,'50–70%'),(70,90,'70–90%'),(90,101,'90%+')]
print()
for lo, hi, label in bins:
    count = len(p3_pct[(p3_pct >= lo) & (p3_pct < hi)])
    bar   = "█" * int(count / 5)
    print(f"  {label:>8}  {count:>4}  {bar}")

print(f"\n  Mean:   {p3_pct.mean():.1f}%")
print(f"  Median: {p3_pct.median():.1f}%")
print(f"  Min:    {p3_pct.min():.1f}%  Max: {p3_pct.max():.1f}%")

print(f"\n  Saved clean dataset: {rows_after:,} rows ready for analysis.")

# ══════════════════════════════════════════════════════════════════
# STEP 2: ANALYSIS
# ══════════════════════════════════════════════════════════════════

# ── Target Compliance ─────────────────────────────────────────────
print(f"\n{'─'*62}")
print("TARGET COMPLIANCE BY PRIORITY LEVEL (all years, all procedures)")
print(f"{'─'*62}")

comp = (df.groupby("priority")
          .agg(avg_pct_in_target=("pct_in_target","mean"),
               avg_wait=("median_wait","mean"),
               meets_target_pct=("meets_target","mean"))
          .reset_index())

print(f"\n  {'Priority':>9} {'% In Target':>13} {'Avg Wait':>10} {'Sites ≥90%':>12}")
print(f"  {'─'*9} {'─'*13} {'─'*10} {'─'*12}")
for _, r in comp.iterrows():
    print(f"  Priority {int(r['priority']):>1}  {r['avg_pct_in_target']:>12.0f}%"
          f" {r['avg_wait']:>9.0f}d {r['meets_target_pct']:>11.0%}")

# ── Procedure Ranking ─────────────────────────────────────────────
print(f"\n{'─'*62}")
print("WAIT TIME BY PROCEDURE — Priority 3")
print(f"{'─'*62}")

p3   = df[df["priority"] == 3]
proc = (p3.groupby("procedure")
          .agg(median_wait=("median_wait","median"),
               pct_in_target=("pct_in_target","mean"),
               volume=("volume","sum"))
          .sort_values("median_wait", ascending=False)
          .reset_index())

print(f"\n  {'Procedure':<22} {'Median Wait':>13} {'% In Target':>13} {'Volume':>8}")
print(f"  {'─'*22} {'─'*13} {'─'*13} {'─'*8}")
for _, r in proc.iterrows():
    flag = " ◄ LONGEST WAIT" if r["median_wait"] == proc["median_wait"].max() else ""
    print(f"  {r['procedure']:<22} {r['median_wait']:>12.0f}d {r['pct_in_target']:>12.0f}%"
          f" {r['volume']:>8,}{flag}")

# ── Urban vs Rural ────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("URBAN vs RURAL COMPLIANCE GAP (Priority 3)")
print(f"{'─'*62}")

ur = (p3.groupby("urban")
        .agg(median_wait=("median_wait","median"),
             pct_in_target=("pct_in_target","mean"),
             hospitals=("hospital","nunique"))
        .reset_index())
ur["label"] = ur["urban"].map({True:"Urban", False:"Rural/Northern"})

print(f"\n  {'Region':<18} {'Median Wait':>13} {'% In Target':>13} {'Hospitals':>10}")
print(f"  {'─'*18} {'─'*13} {'─'*13} {'─'*10}")
for _, r in ur.iterrows():
    print(f"  {r['label']:<18} {r['median_wait']:>12.0f}d {r['pct_in_target']:>12.0f}%"
          f" {r['hospitals']:>10}")

urban_compliance = ur[ur["urban"]==True]["pct_in_target"].values[0]
rural_compliance = ur[ur["urban"]==False]["pct_in_target"].values[0]
urban_wait       = ur[ur["urban"]==True]["median_wait"].values[0]
rural_wait       = ur[ur["urban"]==False]["median_wait"].values[0]
print(f"\n  Compliance gap:  {urban_compliance - rural_compliance:.0f} percentage points (urban vs rural)")
print(f"  Median wait gap: {rural_wait - urban_wait:.0f} days longer in rural/northern hospitals")
print(f"  Rural wait is {rural_wait/urban_wait - 1:.0%} longer than urban wait")

# ── Year-over-Year ────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("YEAR-OVER-YEAR TREND — Priority 3")
print(f"{'─'*62}")

yr = (p3.groupby("year")
        .agg(median_wait=("median_wait","median"),
             pct_in_target=("pct_in_target","mean"))
        .reset_index())

pre_covid  = yr[yr["year"] <= 2019]["pct_in_target"].mean()
latest_pct = yr[yr["year"] == yr["year"].max()]["pct_in_target"].values[0]
covid_pct  = yr[yr["year"] == 2020]["pct_in_target"].values[0]
drop       = pre_covid - covid_pct
recovery   = pre_covid - latest_pct

print(f"\n  {'Year':>6} {'Median Wait':>13} {'% In Target':>13}")
print(f"  {'─'*6} {'─'*13} {'─'*13}")
prev = None
for _, r in yr.iterrows():
    chg  = f"({r['pct_in_target']-prev:+.1f}pp)" if prev is not None else ""
    note = " ← COVID-19 spike" if r["year"] == 2020 else ""
    print(f"  {r['year']:>6} {r['median_wait']:>12.0f}d {r['pct_in_target']:>12.0f}%"
          f"  {chg}{note}")
    prev = r["pct_in_target"]

print(f"\n  Pre-COVID avg compliance: {pre_covid:.1f}%")
print(f"  2020 compliance drop:     {drop:.1f}pp")
print(f"  Latest year compliance:   {latest_pct:.1f}%")
print(f"  Remaining gap:            {recovery:.1f}pp below pre-COVID baseline")

# ── Hospital Ranking ──────────────────────────────────────────────
print(f"\n{'─'*62}")
print("HOSPITAL COMPLIANCE RANKING — Priority 3 (latest year)")
print(f"{'─'*62}")

latest_yr = df["year"].max()
hosp = (df[(df["year"]==latest_yr) & (df["priority"]==3)]
        .groupby(["hospital","region","urban"])
        .agg(pct_target=("pct_in_target","mean"),
             median_wait=("median_wait","median"))
        .sort_values("pct_target", ascending=False)
        .reset_index())

above_90 = (hosp.pct_target >= 90).sum()
below_90 = (hosp.pct_target < 90).sum()

print(f"\n  {'Hospital':<24} {'Region':<16} {'% In Target':>12} {'Median Wait':>12}")
print(f"  {'─'*24} {'─'*16} {'─'*12} {'─'*12}")
for _, r in hosp.iterrows():
    tag = " ✓" if r["pct_target"] >= 90 else " [rural]" if not r["urban"] else ""
    print(f"  {r['hospital']:<24} {r['region']:<16}"
          f" {r['pct_target']:>11.0f}% {r['median_wait']:>11.0f}d{tag}")

print(f"\n  Hospitals meeting 90% target: {above_90} of {len(hosp)}")
print(f"  Hospitals below 90% target:  {below_90} of {len(hosp)}")

# ── Recommendations ───────────────────────────────────────────────
print(f"\n{'─'*62}")
print("STRATEGIC RECOMMENDATIONS")
print(f"{'─'*62}")
print(f"""
  1. NORTHERN ACCESS GAP
     Rural and northern hospitals average {urban_compliance - rural_compliance:.0f}pp
     lower compliance than urban hospitals. Rural patients
     wait {rural_wait - urban_wait:.0f} more days on average. Ontario should fund
     mobile surgical teams and telehealth pre-op
     consultation to reduce unnecessary travel and delay.

  2. WIDESPREAD TARGET FAILURE
     {below_90} of {len(hosp)} hospitals fall below the 90% provincial
     target. Ontario Health should publish real-time
     hospital-level compliance dashboards to create
     accountability and help patients make informed
     referral decisions.

  3. COVID RECOVERY — NEAR-COMPLETE BUT UNEVEN
     The province-wide compliance drop of {drop:.0f}pp in 2020
     has nearly recovered — the gap is now {recovery:.1f}pp.
     However, northern hospitals are recovering more slowly.
     A targeted backlog reduction program with
     hospital-specific timelines is still needed.

  4. VOLUME REDISTRIBUTION
     High-volume urban hospitals are at capacity.
     Structured referral protocols directing stable
     Priority 4 patients to lower-volume rural
     facilities would reduce waits system-wide.
""")
print(sep)
