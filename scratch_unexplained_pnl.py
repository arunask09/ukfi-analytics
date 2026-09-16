"""
Exercise 3 (0.1 seed for Phase 4.7): unexplained_pnl.

A P&L-explain residual check. Given yesterday's and today's PV, and a dict of
*predicted* contributions to the change (e.g. carry, roll, curve_move,
spread_move), work out how much of the actual change is NOT explained by the
prediction -- the residual -- and flag it if it's bigger than a documented
threshold.

Why this matters: a persistent unexplained residual is often the first
symptom of a pricing bug (wrong convention, stale curve, bad interpolation),
not "the market did something weird". See
knowledge/lessons/P0-quant-roles-and-pipeline.md, stage 6, and
knowledge/lessons/P1-time-value-of-money.md for the PV mechanics this builds on.

TODO: pick THRESHOLD and justify the choice in a comment.
TODO: implement unexplained_pnl().
TODO: write the three tests described in the exercise spec (see docstring
      below) -- in test_unexplained_pnl.py or wherever your suite expects it.
"""

THRESHOLD = 0.2  # TODO: pick a number (absolute £, or a % of PV?) and threshold can be bid ask spread value. so if the residual is higher or lower we can flag


def unexplained_pnl(pv_yesterday: float, pv_today: float, predicted: dict) -> tuple[float, bool]:
    """
    Returns (residual, flagged).

    residual = actual PV change - sum of predicted's components.
    flagged  = True if abs(residual) exceeds THRESHOLD.

    Decide explicitly how a missing predicted component (e.g. no
    "spread_move" key at all) should be treated as contributing zero.
    """
    # TODO 1: what is the actual PV change?
    actual_pv_change = pv_today - pv_yesterday
    # TODO 2: what does `predicted` sum to? (sum up with values to handle missing component as zero)
    predicted_total = sum(predicted.values())
    # TODO 3: what is the residual?
    residual = actual_pv_change - predicted_total
    # TODO 4: is it flagged?
    if abs(residual) > THRESHOLD:
        flagged = True
    else:
        flagged = False
    # TODO 5: return (residual, flagged)
    return (residual, flagged)
    


# ---------------------------------------------------------------------------
# Tests to write (in test_unexplained_pnl.py, or inline here with pytest if
# you prefer for this scratch exercise):
#
# 1. residual ~= 0 when predicted's components sum exactly to
#    (pv_today - pv_yesterday).
# 2. flagged triggers for a residual just ABOVE THRESHOLD, and does NOT
#    trigger for one just BELOW it (boundary test, both sides).
# 3. a missing predicted component key doesn't crash -- behaves per whatever
#    you documented above.
# ---------------------------------------------------------------------------
