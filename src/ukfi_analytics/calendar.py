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
