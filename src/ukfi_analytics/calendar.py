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
