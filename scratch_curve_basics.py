import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import CubicSpline, interp1d

# BoE nominal spot curve, [21 SEP 2026] -- from "GLC Nominal daily data current month.xlsx"
tenors = [0.5, 1, 2, 5, 10, 30]
zero_rates_pct = [4.14, 4.37, 4.56, 4.78, 5.19, 5.73]

zero_rate = pd.Series(zero_rates_pct, index=tenors)
zero_rate = zero_rate * 0.01

zero_rate = zero_rate.rename("zero_rate")

DF = pd.Series(
    np.exp(-zero_rate * zero_rate.index),
    index=zero_rate.index,
    name="discount_factor",
)
linear_interp = interp1d(tenors, zero_rate)
cubic_interp = CubicSpline(tenors, zero_rate)

print(zero_rate)
print(DF)
print(linear_interp(7.5))
print(cubic_interp(7.5))


grid = np.linspace(min(tenors), max(tenors), 200)
linear_vals = linear_interp(grid)
cubic_vals = cubic_interp(grid)

plt.plot(grid, linear_vals, label="linear")
plt.plot(grid, cubic_vals, label="cubic spline")
plt.scatter(tenors, zero_rate, color="black", label="pillars", zorder=5)
plt.xlabel("tenor (years)")
plt.ylabel("zero rate")
plt.legend()
plt.savefig("curve_interp.png")

fig = go.Figure()
fig.add_scatter(x=grid, y=linear_vals, mode="lines", name="linear")
fig.add_scatter(x=grid, y=cubic_vals, mode="lines", name="cubic spline")
fig.add_scatter(x=tenors, y=zero_rate, mode="markers", name="pillars")
fig.write_html("curve_interp_plotly.html")
