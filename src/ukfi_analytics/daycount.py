from datetime import date


def act_365f(start: date, end: date) -> float:
    gap = end - start
    return gap.days / 365

def act_360(start: date, end: date) -> float:
    gap = end - start
    return gap.days / 360

def thirty_e_360(start: date, end: date) -> float:
    years_gap = end.year - start.year
    months_gap = end.month - start.month
    d1 = start.day
    d2 = end.day
    d1 = min(d1, 30)
    d2 = min(d2, 30)
    day_gap = d2 - d1
    return ((360 * (years_gap) + 30 * (months_gap) + (day_gap)) / 360)

def thirty_360_bond_basis(start: date, end: date) -> float:
    year_gap = end.year - start.year
    month_gap = end.month - start.month
    d1 = start.day
    d2 = end.day
    d1 = min(d1, 30) #To swap if d1 is 31st
    d2 = 30 if d1 == 30 and d2 == 31 else d2
    day_gap = d2 - d1
    return ((360 * (year_gap) + 30 * (month_gap) + day_gap) / 360)
