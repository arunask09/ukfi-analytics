from datetime import date, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ukfi_analytics.calendar import (
    easter_holidays,
    easter_sunday,
    fixed_holidays,
    paschal_full_moon,
    weekday_holidays,
    weekday_on_or_after,
    weekday_on_or_before,
)

TEST_SET = [
    (2022, {date(2022, 1, 3), date(2022, 12, 26), date(2022, 12, 27)}),
    (2027, {date(2027, 1, 1), date(2027, 12, 27), date(2027, 12, 28)}),
]

WEEKDAY_SET = [
    (2026, {date(2026, 5, 4), date(2026, 5, 25), date(2026, 8, 31)}),
    (2027, {date(2027, 5, 3), date(2027, 5, 31), date(2027, 8, 30)}),
    (2028, {date(2028, 5, 1), date(2028, 5, 29), date(2028, 8, 28)}),
]

EASTER_SET = [
    (2024, {date(2024, 3, 29), date(2024, 4, 1)}),  # GF and EM in different months
    (2025, {date(2025, 4, 18), date(2025, 4, 21)}),  # PFM on a Sunday
]

YEARS = st.integers(min_value=1901, max_value=2199)
DATES = st.dates(min_value=date(1901, 1, 1), max_value=date(2199, 12, 31))
WEEKDAYS = st.integers(min_value=0, max_value=6)


@pytest.mark.parametrize("year, expected", TEST_SET)
def test_fixed_holidays(year: int, expected: set[date]) -> None:
    assert fixed_holidays(year) == expected


@pytest.mark.parametrize("year, expected", WEEKDAY_SET)
def test_weekday_holidays(year: int, expected: set[date]) -> None:
    assert weekday_holidays(year) == expected


@given(d=DATES, target=WEEKDAYS)
def test_weekday_on_or_after_properties(d: date, target: int) -> None:
    result = weekday_on_or_after(d, target)
    assert result.weekday() == target
    assert result >= d
    assert result - d < timedelta(days=7)


@given(d=DATES, target=WEEKDAYS)
def test_weekday_on_or_before_properties(d: date, target: int) -> None:
    result = weekday_on_or_before(d, target)
    assert result.weekday() == target
    assert result <= d
    assert d - result < timedelta(days=7)


@pytest.mark.parametrize("year, expected", EASTER_SET)
def test_easter_holidays(year: int, expected: set[date]) -> None:
    assert easter_holidays(year) == expected


@given(year=YEARS)
def test_easter_sunday_properties(year: int) -> None:
    easter = easter_sunday(year)
    gap = easter - paschal_full_moon(year)
    assert easter.weekday() == 6
    assert date(year, 3, 22) <= easter <= date(year, 4, 25)
    assert timedelta(days=1) <= gap <= timedelta(days=7)
