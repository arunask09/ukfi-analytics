"""
Guided tour: bootstrap a discount curve with QuantLib, then price a bond off it.

Run it as-is first and read the three printed numbers. Then do the three
hands-on edits at the bottom, one at a time, re-running after each.

All quotes below are synthesised for this exercise, not real market data —
clean-room rule.
"""
import QuantLib as ql

# --- 1. Fix "today" so results are reproducible run to run ---
today = ql.Date(15, 9, 2026)
ql.Settings.instance().evaluationDate = today

calendar = ql.UnitedKingdom()
day_counter = ql.Actual365Fixed()
settlement_days = 2

# --- 2. Market quotes (SONIA-style, synthesised) ---
deposit_quotes = {
    ql.Period(1, ql.Weeks): 0.0475,
    ql.Period(1, ql.Months): 0.0472,
    ql.Period(3, ql.Months): 0.0465,
}
swap_quotes = {
    ql.Period(1, ql.Years): 0.0450,
    ql.Period(2, ql.Years): 0.0420,
    ql.Period(5, ql.Years): 0.0405,
    ql.Period(10, ql.Years): 0.0410,
    ql.Period(20, ql.Years): 0.0415
}

# --- 3. Wrap each quote so QuantLib can watch it for changes ---
deposit_helpers = [
    ql.DepositRateHelper(
        ql.QuoteHandle(ql.SimpleQuote(rate)),
        tenor,
        settlement_days,
        calendar,
        ql.ModifiedFollowing,
        False,
        day_counter,
    )
    for tenor, rate in deposit_quotes.items()
]

ibor_index = ql.IborIndex(
    "SONIA-style",
    ql.Period(1, ql.Days),
    settlement_days,
    ql.GBPCurrency(),
    calendar,
    ql.ModifiedFollowing,
    False,
    day_counter,
)

swap_helpers = [
    ql.SwapRateHelper(
        ql.QuoteHandle(ql.SimpleQuote(rate)),
        tenor,
        calendar,
        ql.Annual,
        ql.ModifiedFollowing,
        day_counter,
        ibor_index,
    )
    for tenor, rate in swap_quotes.items()
]

helpers = deposit_helpers + swap_helpers

# --- 4. Bootstrap: solve for the curve that reprices every quote above
#        to (approximately) zero ---
curve = ql.PiecewiseLogCubicDiscount(today, helpers, day_counter)
curve.enableExtrapolation()
curve_handle = ql.YieldTermStructureHandle(curve)

# --- 5. Read off two curve numbers ---
one_year = today + ql.Period(1, ql.Years)
five_year = today + ql.Period(5, ql.Years)

df_1y = curve.discount(one_year)
zero_5y = curve.zeroRate(five_year, day_counter, ql.Continuous).rate()

print(f"1y discount factor : {df_1y:.6f}")
print(f"5y zero rate        : {zero_5y:.4%}")

# --- 6. Price a bond off this curve ---
issue_date = ql.Date(15, 9, 2021)
maturity_date = ql.Date(15, 9, 2031)
coupon = 0.04

schedule = ql.Schedule(
    issue_date,
    maturity_date,
    ql.Period(ql.Annual),
    calendar,
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Backward,
    False,
)

bond = ql.FixedRateBond(settlement_days, 100.0, schedule, [coupon], day_counter)
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))

print(f"Clean price (4% coupon): {bond.cleanPrice():.4f}")

# ---------------------------------------------------------------------
# YOUR TURN — do these one at a time, re-running the script after each.
#
# 1. Add a 20y point to `swap_quotes` above (any rate near the 10y one,
#    e.g. 0.0405) and re-run. Write down the NEW 5y zero rate.
#    It will move even though you only added a point at the far end —
#    that's the interpolation artefact: the curve refits as a whole,
#    not point by point.
#
# 2. Undo that. Change `coupon = 0.04` to `coupon = 0.05` and re-run.
#    Write down the NEW clean price. This is "more cash promised", not
#    duration — you fed the bond a bigger coupon, the discount curve
#    underneath it didn't move.
#
# 3. (Optional, to actually see duration) Undo the coupon change.
#    Instead add 0.0010 (10bp) to every value in `swap_quotes` and
#    re-run. The clean price change now IS a duration effect: same
#    cash flows, different discounting.
# ---------------------------------------------------------------------
