from datetime import date


def act_365f(start: date, end: date) -> float:
    gap = end - start
    return gap.days / 365