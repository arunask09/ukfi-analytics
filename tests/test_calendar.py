from datetime import date, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ukfi_analytics.calendar import (
    Convention,
    add_business_days,
    adjust,
    easter_holidays,
    easter_sunday,
    fixed_holidays,
    is_business_day,
    paschal_full_moon,
    uk_holidays,
    weekday_holidays,
    weekday_on_or_after,
    weekday_on_or_before,
)

UK_SET = [
    (
        2020,
        {
            date(2020, 1, 1),
            date(2020, 4, 10),
            date(2020, 4, 13),
            date(2020, 5, 8),
            date(2020, 5, 25),
            date(2020, 8, 31),
            date(2020, 12, 25),
            date(2020, 12, 28),
        },
    ),  # VE Day move
    (
        2022,
        {
            date(2022, 1, 3),
            date(2022, 4, 15),
            date(2022, 4, 18),
            date(2022, 5, 2),
            date(2022, 6, 2),
            date(2022, 6, 3),
            date(2022, 8, 29),
            date(2022, 9, 19),
            date(2022, 12, 26),
            date(2022, 12, 27),
        },
    ),  # spring move + jubilee + funeral
]


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


@pytest.mark.parametrize("year, expected", UK_SET)
def test_uk_holidays(year, expected):
    assert uk_holidays(year) == expected


@pytest.mark.parametrize(
    ("d", "expected"),
    [
        (date(2026, 12, 24), True),  # Thu, weekday
        (date(2026, 12, 25), False),  # Fri, Christmas Day
        (date(2026, 12, 26), False),  # Sat, weekend (Boxing Day moves to Mon 28)
        (date(2026, 12, 27), False),  # Sun, Weekend
        (date(2026, 12, 28), False),  # Mon, boxing day substitute
        (date(2026, 12, 29), True),  # Tue, Business day
        (date(2026, 12, 30), True),  # Wed, Business day
    ],
)
def test_is_business_day_christmas_2026(d: date, expected: bool) -> None:
    assert is_business_day(d) == expected


@pytest.mark.parametrize(
    ("start", "n", "expected"),
    [
        (date(2026, 12, 24), 0, date(2026, 12, 24)),
        (date(2026, 12, 25), 1, date(2026, 12, 29)),
        (date(2026, 12, 26), 2, date(2026, 12, 30)),
        (date(2026, 12, 27), 1, date(2026, 12, 29)),
        (date(2026, 12, 28), 0, date(2026, 12, 28)),
        (date(2026, 12, 29), 0, date(2026, 12, 29)),
        (date(2026, 12, 30), 0, date(2026, 12, 30)),
        (date(2026, 12, 31), 1, date(2027, 1, 4)),
        (
            date(2026, 12, 29),
            -1,
            date(2026, 12, 24),
        ),  # backward over Christmas + Boxing Day substitute
        (date(2027, 1, 4), -1, date(2026, 12, 31)),  # backward across the year boundary
    ],
)
def test_add_business_days(start: date, n: int, expected: date) -> None:
    assert add_business_days(start, n) == expected


@pytest.mark.parametrize(
    ("d", "convention", "expected"),
    [
        # closed day, December: F and MF agree
        (date(2026, 12, 25), "F", date(2026, 12, 29)),
        (date(2026, 12, 25), "MF", date(2026, 12, 29)),
        (date(2026, 12, 25), "P", date(2026, 12, 24)),
        # closed day, end of Feb: F crosses into March, so MF falls back
        (date(2027, 2, 27), "F", date(2027, 3, 1)),
        (date(2027, 2, 27), "MF", date(2027, 2, 26)),
        (date(2027, 2, 27), "P", date(2027, 2, 26)),
        # open day: returned unchanged under every convention
        (date(2026, 12, 24), "F", date(2026, 12, 24)),
        (date(2026, 12, 24), "MF", date(2026, 12, 24)),
        (date(2026, 12, 24), "P", date(2026, 12, 24)),
        # year-end: F crosses into January
        (date(2022, 12, 31), "F", date(2023, 1, 3)),
        (date(2022, 12, 31), "MF", date(2022, 12, 30)),
        (date(2022, 12, 31), "P", date(2022, 12, 30)),
    ],
)
def test_adjust(d: date, convention: Convention, expected: date) -> None:
    assert adjust(d, convention) == expected
