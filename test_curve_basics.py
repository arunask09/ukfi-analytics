import pandas as pd
import pytest

from scratch_curve_basics import DF

# TODO: fill in all 6 pillars from your BoE curve: (tenor, expected DF to 6 dp)
PILLARS = [(0.5, 0.979513),(1.0,0.957241),(2.0,0.912835),(5.0,0.787415),(10.0,0.595115),
           (30.0,0.179245)]


@pytest.fixture
def zero_curve():
    tenors = [0.5, 1, 2, 5, 10, 30]
    zero_rates_pct = [4.14, 4.37, 4.56, 4.78, 5.19, 5.73]
    return pd.Series(zero_rates_pct, index=tenors) * 0.01

def test_zero_curve_has_six_pillars(zero_curve):
    assert len(zero_curve) == 6
    assert (zero_curve < 0.20).all() and ( zero_curve > 0 ).all()




@pytest.mark.parametrize("tenor, expected_df", PILLARS)
def test_df_matches_golden(tenor: float, expected_df: float) -> None:

    assert DF.loc[tenor] == pytest.approx(expected_df, abs=1e-6)

# def test_df_value_on_exact_match() -> None:
#     df_1y=0.957241
#     df_30y=0.179245
   
#     assert DF.loc[1.0] == pytest.approx(df_1y)
#     assert DF.loc[30.0] == pytest.approx(df_30y, rel=1e-4)