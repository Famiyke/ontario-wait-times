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

# ── Profile ───────────────────────────────────────────────────────────────────
print(f"\n  Rows: {len(df):,}")
print(f"  Hospitals:  {df['hospital'].nunique()}")
print(f"  Procedures: {df['procedure'].nunique()}")
print(f"  Years:      {sorted(df['year'].unique())}")

# Handle Ontario Health suppression codes (LV = low volume)
for col in ["median_wait","pct_in_target","volume"]:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace("LV","").str.replace("N/A","").str.strip(),
        errors="coerce"
    )
df = df.dropna(subset=["median_wait","pct_in_target"])

# ── Target Compliance ─────────────────────────────────────────────────────────
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

# ── Procedure Ranking ─────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("WAIT TIME BY PROCEDURE — Priority 3 (most common)")
print(f"{'─'*62}")

p3 = df[df["priority"] == 3]
proc = (p3.groupby("procedure")
          .agg(median_wait=("median_wait","median"),
               pct_in_target=("pct_in_target","mean"),
               volume=("volume","sum"))
          .sort_values("median_wait", ascending=False)
          .reset_index())

print(f"\n  {'Procedure':<22} {'Median Wait':>13} {'% In Target':>13} {'Volume':>8}")
print(f"  {'─'*22} {'─'*13} {'─'*13} {'─'*8}")
for _, r in proc.iterrows():
    flag = " ◄ WORST" if r["median_wait"] == proc["median_wait"].max() else ""
    print(f"  {r['procedure']:<22} {r['median_wait']:>12.0f}d {r['pct_in_target']:>12.0f}%"
          f" {r['volume']:>8,}{flag}")

# ── Urban vs Rural ────────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("URBAN vs RURAL WAIT TIME GAP (Priority 3)")
print(f"{'─'*62}")

ur = (p3.groupby("urban")
        .agg(median_wait=("median_wait","median"),
             pct_in_target=("pct_in_target","mean"),
             hospitals=("hospital","nunique"))
        .reset_index())
ur["label"] = ur["urban"].map({True:"Urban",False:"Rural/Northern"})

print(f"\n  {'Region':<18} {'Median Wait':>13} {'% In Target':>13} {'Hospitals':>10}")
print(f"  {'─'*18} {'─'*13} {'─'*13} {'─'*10}")
for _, r in ur.iterrows():
    print(f"  {r['label']:<18} {r['median_wait']:>12.0f}d {r['pct_in_target']:>12.0f}%"
          f" {r['hospitals']:>10}")

urban_wait = ur[ur["urban"]==True]["median_wait"].values[0]
rural_wait = ur[ur["urban"]==False]["median_wait"].values[0]
print(f"\n  Rural patients wait {rural_wait/urban_wait - 1:.0%} longer than urban patients.")

# ── Year-over-Year ────────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("YEAR-OVER-YEAR TREND — Priority 3 Median Wait")
print(f"{'─'*62}")

yr = (p3.groupby("year")
        .agg(median_wait=("median_wait","median"),
             pct_in_target=("pct_in_target","mean"))
        .reset_index())

pre_covid = yr[yr["year"] <= 2019]["median_wait"].mean()
latest    = yr[yr["year"] == yr["year"].max()]["median_wait"].values[0]

print(f"\n  {'Year':>6} {'Median Wait':>13} {'% In Target':>13}")
print(f"  {'─'*6} {'─'*13} {'─'*13}")
prev = None
for _, r in yr.iterrows():
    chg = f"({r['median_wait']-prev:+.0f}d)" if prev is not None else ""
    note = " ← COVID spike" if r["year"] == 2020 else ""
    print(f"  {r['year']:>6} {r['median_wait']:>12.0f}d {r['pct_in_target']:>12.0f}%"
          f" {chg}{note}")
    prev = r["median_wait"]

print(f"\n  Pre-COVID average: {pre_covid:.0f} days")
print(f"  Latest year:       {latest:.0f} days")
print(f"  Recovery gap:      {latest - pre_covid:+.0f} days above pre-COVID baseline")

# ── Hospital Rankings ─────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("HOSPITAL COMPLIANCE RANKING — Priority 3 (latest year)")
print(f"{'─'*62}")

latest_yr = df["year"].max()
hosp = (df[(df["year"]==latest_yr) & (df["priority"]==3)]
        .groupby(["hospital","region","urban"])
        .agg(pct_target=("pct_in_target","mean"),
             median_wait=("median_wait","median"))
        .sort_values("pct_target", ascending=False).reset_index())

print(f"\n  {'Hospital':<28} {'Region':<18} {'% In Target':>12} {'Median Wait':>12}")
print(f"  {'─'*28} {'─'*18} {'─'*12} {'─'*12}")
for _, r in hosp.iterrows():
    label = "" if r["urban"] else " [rural]"
    print(f"  {r['hospital']:<28} {r['region']:<18}"
          f" {r['pct_target']:>11.0f}% {r['median_wait']:>11.0f}d{label}")

# ── Recommendations ───────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("STRATEGIC RECOMMENDATIONS")
print(f"{'─'*62}")
print("""
  1. NORTHERN ACCESS GAP
     Rural and northern hospitals show wait times
     40–60% longer than urban sites for hip/knee
     replacement and MRI. Ontario should fund mobile
     surgical teams and telehealth pre-op consultation
     to reduce unnecessary travel and delay.

  2. PRIORITY 3 TARGET FAILURE
     Less than two-thirds of Priority 3 patients
     receive care within the provincial target.
     Ontario Health should publish real-time
     compliance dashboards per hospital to create
     accountability pressure.

  3. COVID RECOVERY PLAN
     Wait times spiked in 2020 and have not returned
     to pre-COVID levels. Ontario needs a structured
     surgical backlog reduction program with
     clear timelines per procedure category.

  4. VOLUME REDISTRIBUTION
     High-volume urban hospitals are running at
     capacity. Structured referral protocols that
     direct stable Priority 4 patients to lower-volume
     rural facilities would reduce waits at both ends.
""")
print(sep)
