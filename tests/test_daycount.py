from datetime import date

import pytest
import QuantLib as ql
from hypothesis import example, given
from hypothesis import strategies as st

from ukfi_analytics.daycount import (
    act_360,
    act_365f,
    thirty_360_bond_basis,
    thirty_e_360,
)


def to_ql(d: date) -> ql.Date:
    ql_date = ql.Date(d.day, d.month, d.year)
    return ql_date

@given(start = st.dates(min_value=date(1901,1,1), max_value=date(2199, 12, 31)),
       end = st.dates(min_value=date(1901,1,1), max_value=date(2199, 12, 31)))
def test_act_365f_matches_quantlib_random_dates(start: date, end:date) -> None:
    expected = ql.Actual365Fixed().yearFraction(to_ql(start), to_ql(end))
    # A one-day error is 2.7e-3 years and must fail. Correct code matches 
    # QuantLib exactly (gap 0.0), so a tolerance near float noise (1e-14) 
    # can't give false failures and catches anything bigger.
    assert act_365f(start, end) == pytest.approx(expected, abs=1e-14)

def test_act_365f_matches_quantlib() -> None:
    start = date(2026, 8,31)
    end = date(2027, 2, 28)
    expected = ql.Actual365Fixed().yearFraction(to_ql(start), to_ql(end))
    assert act_365f(start, end) == pytest.approx(expected, abs=1e-14)

@given(
        start = st.dates(min_value=date(1901,1,1), max_value=date(2199,12,31)),
        end = st.dates(min_value=date(1901,1,1), max_value=date(2199,12,31))
)
def test_act_360_matches_quantlib_random_dates(start: date, end: date) -> None:
    expected = ql.Actual360().yearFraction(to_ql(start), to_ql(end))
    assert act_360(start, end) == pytest.approx(expected, abs=1e-14)

def test_act_360_matches_quantlib() -> None:
    start = date(2026, 8, 31)
    end = date(2027,2,28)
    expected = ql.Actual360().yearFraction(to_ql(start), to_ql(end))
    assert act_360(start, end) == pytest.approx(expected, abs=1e-14)

@given(
        start = st.dates(min_value=date(1901,1,1), max_value=date(2199,12,31)),
        end = st.dates(min_value=date(1901,1,1), max_value=date(2199,12,31))
)
@example(start=date(2026,8, 31),end=date(2027, 2 ,28))
@example(start=date(2026,8, 21),end=date(2027, 3 ,31))
@example(start=date(2026,1, 31),end=date(2027, 12 ,31))
def test_thirty_e_360_matches_quantlib_random_dates(start: date, end: date) -> None:
    expected = ql.Thirty360(ql.Thirty360.European).yearFraction(to_ql(start), to_ql(end))
    assert thirty_e_360(start, end) == pytest.approx(expected, abs=1e-14)

def test_thirty_e_360_matches_quantlib() -> None:
    start = date(2026, 8, 31)
    end = date(2027,2,28)
    expected = ql.Thirty360(ql.Thirty360.European).yearFraction(to_ql(start), to_ql(end))
    assert thirty_e_360(start, end) == pytest.approx(expected, abs=1e-14)

@given(
        start = st.dates(min_value=date(1901,1,1), max_value=date(2199,12,31)),
        end = st.dates(min_value=date(1901,1,1), max_value=date(2199,12,31))
)
@example(start=date(2026,1, 15),end=date(2027, 3 ,31))
@example(start=date(2026,4, 30),end=date(2027, 5 ,31))
@example(start=date(2026,1, 31),end=date(2027, 12 ,31))
def test_thirty_360_bond_basis_matches_quantlib_random_dates(start: date, end: date) -> None:
    expected = ql.Thirty360(ql.Thirty360.BondBasis).yearFraction(to_ql(start), to_ql(end))
    assert thirty_360_bond_basis(start, end) == pytest.approx(expected, abs=1e-14)

def test_thirty_360_bond_basis_matches_quantlib() -> None:
    start = date(2026, 1, 15)
    end = date(2026,3,31)
    expected = ql.Thirty360(ql.Thirty360.BondBasis).yearFraction(to_ql(start), to_ql(end))
    assert thirty_360_bond_basis(start, end) == pytest.approx(expected, abs=1e-14)