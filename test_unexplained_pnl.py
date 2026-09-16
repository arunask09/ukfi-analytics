"""
Tests for unexplained_pnl() — see scratch_unexplained_pnl.py.

Three cases (from that file's docstring):
1. residual ~= 0 when predicted's components sum exactly to the actual PV change.
2. flagged triggers just above THRESHOLD, does not trigger just below it (both sides).
3. a missing predicted component key doesn't crash.
"""

import pytest

from scratch_unexplained_pnl import unexplained_pnl


def test_residual_zero_on_exact_match() -> None:
    # TODO: pick pv_yesterday / pv_today and a `predicted` dict whose values
    # sum to exactly (pv_today - pv_yesterday).
    pv_today=102.0
    pv_yesterday=100.00
    predicted={"carry" : 1.0, "curve_move": 1.0}
    # TODO: call unexplained_pnl(...) and unpack (residual, flagged).
    result = unexplained_pnl(pv_yesterday, pv_today, predicted)
    residual, flagged = result
    # TODO: assert residual is ~0 (use pytest.approx) and flagged is False.
    assert residual == pytest.approx(0.0)
    assert flagged is False


def test_flag_boundary_above_and_below() -> None:
    # TODO: construct a case where residual lands just ABOVE THRESHOLD.
    #       What pv_yesterday/pv_today/predicted gives you that, given THRESHOLD?
    pv_today = 104.00
    pv_yesterday = 100.00
    predicted={"carry": 3.5, "spread_move": 0.29 }

    result = unexplained_pnl(pv_yesterday, pv_today, predicted)
    residual, flagged = result
    # TODO: assert flagged is True for that case.
    assert flagged is True
    # TODO: construct a second case where residual lands just BELOW THRESHOLD.
    pv_today = 102.00
    pv_yesterday = 100.00
    predicted={"carry": 1.00, "spread_move": 0.81 }
    
    result = unexplained_pnl(pv_yesterday, pv_today, predicted)
    residual, flagged = result
    # TODO: assert flagged is False for that case.
    assert flagged is False
    assert residual == pytest.approx(0.19)


def test_missing_predicted_key_does_not_crash() -> None:
    # TODO: build a `predicted` dict missing one usual key (e.g. no "spread_move").
    pv_today = 102.00
    pv_yesterday = 100.00
    predicted={"carry": 1.90}
    # TODO: call unexplained_pnl(...) — should not raise.
    result = unexplained_pnl(pv_yesterday, pv_today,predicted)
    _residual, flagged = result
    # TODO: assert the result matches what you documented in
    #       unexplained_pnl()'s docstring for a missing component.
    assert flagged is False
