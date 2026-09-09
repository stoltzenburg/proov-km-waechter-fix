# analyze.py
# Summary: km_since_service, avg_daily_km, and load_factor predict breakdown;
# total odometer and age_years do not — cars with low mileage and fresh service
# records still break down if they are driven hard and loaded heavily.
#
# KM-Waechter breakdown-risk analysis — Vossberg Mobility fleet, 120 cars.
#
# The 80 % rule only flags cars that are almost due for service. This script
# goes further: it ranks every car by how likely it is to break down BEFORE
# the odometer-based rule would ever catch it.
#
# Method
# ------
# 1. For each numeric column, compare the 26 cars that later broke down against
#    the 94 that did not using a Mann-Whitney U test (no normality assumption).
# 2. Only three columns pass p < 0.05:
#      - km_since_service  (p ≈ 0.000008, strongest)  weight 0.5
#      - avg_daily_km      (p ≈ 0.006)                weight 0.3
#      - load_factor       (p ≈ 0.018)                weight 0.2
#    Total odometer and age_years do NOT separate the groups (p > 0.8).
# 3. Each passing column is min-max normalised to [0, 1] and multiplied by its
#    weight; the weighted sum is scaled to 0-100 as the risk score.

import pandas as pd
from scipy import stats

# ── 1. Load ──────────────────────────────────────────────────────────────────

df = pd.read_csv("fleet_history.csv")

# ── 2. Compare groups column by column ───────────────────────────────────────

features = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

print("Group comparison  (Mann-Whitney U, two-sided)")
print(f"  Broke down: {len(broke)} cars    Did not: {len(ok)} cars\n")
print(f"{'Column':<20}  {'Mean (broke)':>13}  {'Mean (ok)':>11}  {'p-value':>10}  {'Separates?'}")
print("-" * 73)
for col in features:
    m_b = broke[col].mean()
    m_o = ok[col].mean()
    _, p = stats.mannwhitneyu(broke[col], ok[col], alternative="two-sided")
    flag = "YES  ✓" if p < 0.05 else "no"
    print(f"{col:<20}  {m_b:>13.2f}  {m_o:>11.2f}  {p:>10.6f}  {flag}")

# ── 3. Build risk score from the three separating columns ────────────────────

print("\nUsing km_since_service (w=0.5), avg_daily_km (w=0.3), load_factor (w=0.2)\n")

def minmax(series: pd.Series) -> pd.Series:
    """Min-max normalise a series to [0, 1]."""
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo)

df["risk_score"] = (
    minmax(df["km_since_service"]) * 0.5
    + minmax(df["avg_daily_km"])   * 0.3
    + minmax(df["load_factor"])    * 0.2
) * 100

# ── 4. Rank by risk and print the top 10 ─────────────────────────────────────

ranked = (
    df[["car_id", "risk_score", "km_since_service", "avg_daily_km",
        "load_factor", "broke_down"]]
    .sort_values("risk_score", ascending=False)
    .reset_index(drop=True)
)

print("Top 10 cars by breakdown risk (highest first):")
print(ranked.head(10).to_string(index=False))

# ── Sanity check ─────────────────────────────────────────────────────────────

top20    = ranked.head(20)
bottom20 = ranked.tail(20)
print(f"\nMean risk score — broke down: {df[df.broke_down == 1]['risk_score'].mean():.1f}  "
      f"/ did not: {df[df.broke_down == 0]['risk_score'].mean():.1f}")
print(f"Breakdown rate in top-20 by risk   : "
      f"{top20['broke_down'].mean() * 100:.1f}%  ({int(top20['broke_down'].sum())}/20)")
print(f"Breakdown rate in bottom-20 by risk: "
      f"{bottom20['broke_down'].mean() * 100:.1f}%  ({int(bottom20['broke_down'].sum())}/20)")
