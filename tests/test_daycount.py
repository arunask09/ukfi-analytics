from datetime import date

import pytest
import QuantLib as ql
from hypothesis import strategies as st
from hypothesis import given

from ukfi_analytics.daycount import act_365f

def to_ql(d: date) -> ql.Date:
    ql_date = ql.Date(d.day, d.month, d.year)
    return ql_date

@given(start = st.dates(min_value=date(1901,1,1), max_value=date(2199, 12, 31)),
       end = st.dates(min_value=date(1901,1,1), max_value=date(2199, 12, 31)))
def test_act_365f_matches_quantlib(start: date, end:date) -> None:
    expected = ql.Actual365Fixed().yearFraction(to_ql(start), to_ql(end))
    # A one-day error is 2.7e-3 years and must fail. Correct code matches 
    # QuantLib exactly (gap 0.0), so a tolerance near float noise (1e-14) 
    # can't give false failures and catches anything bigger.
    assert act_365f(start, end) == pytest.approx(expected, abs=1e-14)

def test_act365f_matches_quantlib() -> None:
    start = date(2026, 8,31)
    end = date(2027, 2, 28)
    excepted = ql.Actual365Fixed().yearFraction(to_ql(start), to_ql(end))
    assert act_365f(start, end) == pytest.approx(excepted, 1e-14)