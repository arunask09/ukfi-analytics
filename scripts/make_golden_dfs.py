from pathlib import Path

import pandas as pd
import QuantLib as ql

ref = ql.Date(15, 1, 2026)
ql.Settings.instance().evaluationDate = ref
day_count = ql.Thirty360(ql.Thirty360.BondBasis)

months = [6, 12, 24, 60, 120, 360]  # your pillars, in months
rates = [0.0414, 0.0437, 0.0456, 0.0478, 0.0519, 0.0573]

# QuantLib treats the FIRST date as "today" (t = 0) and needs a rate there too.
# Put ref first, with the 6M rate again: this only affects t < 0.5, which we never test.
dates = [ref] + [ref + ql.Period(m, ql.Months) for m in months]
curve_rates = [rates[0]] + rates
curve = ql.ZeroCurve(
    dates, curve_rates, day_count, ql.NullCalendar(), ql.Linear(), ql.Continuous
)

rows = []
for n in range(6, 361):  # 6, 7, 8, ..., 360 months (range stops BEFORE 361)
    d = ref + ql.Period(n, ql.Months)
    t = day_count.yearFraction(ref, d)
    df = curve.discount(t)
    rows.append((t, df))

golden = pd.DataFrame(rows, columns=["t", "df"])
GOLDEN_FILE = (
    Path(__file__).resolve().parent.parent / "tests" / "data" / "golden_dfs_linear.csv"
)
golden.to_csv(GOLDEN_FILE, index=False)
