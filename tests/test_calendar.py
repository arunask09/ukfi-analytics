from datetime import date

import pytest

from ukfi_analytics.calendar import fixed_holidays, weekday_holidays

TEST_SET = [
    (2022, {date(2022, 1, 3), date(2022, 12, 26), date(2022, 12, 27)}),
    (2027, {date(2027, 1, 1), date(2027, 12, 27), date(2027, 12, 28)}),
]

WEEKDAY_SET = [
    (2026, {date(2026, 5, 4), date(2026, 5, 25), date(2026, 8, 31)}),
    (2027, {date(2027, 5, 3), date(2027, 5, 31), date(2027, 8, 30)}),
    (2028, {date(2028, 5, 1), date(2028, 5, 29), date(2028, 8, 28)}),
]


@pytest.mark.parametrize("year, expected", TEST_SET)
def test_fixed_holidays(year: int, expected: set[date]) -> None:
    assert fixed_holidays(year) == expected


@pytest.mark.parametrize("year, expected", WEEKDAY_SET)
def test_weekday_holidays(year: int, expected: set[date]) -> None:
    assert weekday_holidays(year) == expected
