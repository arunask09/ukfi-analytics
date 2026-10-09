from datetime import date, timedelta


def fixed_holidays(year: int) -> set[date]:
    """Bucket A: New Year, Christmas, Boxing Day, with forward-only substitutes."""
    raw = [date(year, 1, 1), date(year, 12, 25), date(year, 12, 26)]
    holidays: set[date] = set()

    for d in raw:
        while d.weekday() >= 5 or d in holidays:
            d += timedelta(days=1)
        holidays.add(d)
    return holidays


def weekday_on_or_after(d: date, target: int) -> date:
    """First date >= d whose weekday() == target (0=Mon … 6=Sun)."""
    return d + timedelta(days=(target - d.weekday()) % 7)


def weekday_on_or_before(d: date, target: int) -> date:
    """Last date <= d whose weekday() == target."""
    return d - timedelta(days=(d.weekday() - target) % 7)


def weekday_holidays(year: int) -> set[date]:
    """Bucket B: early May, spring and summer bank holidays (Mondays)."""
    return {
        weekday_on_or_after(date(year, 5, 1), 0),
        weekday_on_or_before(date(year, 5, 31), 0),
        weekday_on_or_before(date(year, 8, 31), 0),
    }


def paschal_full_moon(year: int) -> date:

    golden = year % 19 + 1
    century = year // 100 + 1
    solar = 3 * century // 4 - 12
    lunar = (8 * century + 5) // 25 - 5
    epact = (11 * golden + 20 + lunar - solar) % 30
    if (epact == 25 and golden > 11) or epact == 24:
        epact += 1
    n = 44 - epact
    if n < 21:
        n += 30
    return date(year, 3, 1) + timedelta(days=n - 1)


def easter_sunday(year: int) -> date:
    """First Sunday strictly after the paschal full moon"""
    return weekday_on_or_after(paschal_full_moon(year) + timedelta(days=1), 6)


def easter_holidays(year: int) -> set[date]:
    """Bucket C: Good Friday and Easter Monday"""
    easter = easter_sunday(year)
    return {easter + timedelta(days=1), easter - timedelta(days=2)}


MOVED_HOLIDAYS: dict[date, date] = {
    date(1995, 5, 1): date(1995, 5, 8),  # early May → VE Day 50th
    date(2002, 5, 27): date(2002, 6, 4),
    date(2012, 5, 28): date(2012, 6, 4),
    date(2020, 5, 4): date(2020, 5, 8),
    date(2022, 5, 30): date(2022, 6, 2),
}

EXTRA_HOLIDAYS: set[date] = {
    date(2002, 6, 3),
    date(2011, 4, 29),
    date(2012, 6, 5),
    date(2022, 6, 3),
    date(2022, 9, 19),
    date(2023, 5, 8),
}


def uk_holidays(year: int) -> set[date]:
    """England & Wales bank holidays: buckets A–C with moves applied, plus one-offs."""
    regular = fixed_holidays(year) | weekday_holidays(year) | easter_holidays(year)
    moved = {MOVED_HOLIDAYS.get(d, d) for d in regular}
    extras = {d for d in EXTRA_HOLIDAYS if d.year == year}
    return moved | extras
