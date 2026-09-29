import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline, PchipInterpolator, interp1d

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
pchip_interp = PchipInterpolator(tenors, zero_rate)
