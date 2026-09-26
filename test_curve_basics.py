import numpy as np
import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from scratch_curve_basics import DF, linear_interp, pchip_interp


def df_linear(t: float) -> float:
    return float(np.exp(-linear_interp(t) * t))


# TODO: fill in all 6 pillars from your BoE curve: (tenor, expected DF to 6 dp)
PILLARS = [(0.5, 0.979513),(1.0,0.957241),(2.0,0.912835),(5.0,0.787415),(10.0,0.595115),
           (30.0,0.179245)]

@given(tenor=st.floats(min_value=0.5, max_value=30.0))
def test_df_between_0_and_1(tenor: float) -> None:
    discount_factor = df_linear(tenor)
    # discount_factor = np.exp(-linear_interp(tenor) * tenor) 
    assert (discount_factor > 0 ) and (discount_factor <= 1)


@given(
        tenor_a=st.floats(min_value=0.5, max_value=30.0),
        tenor_b=st.floats(min_value=0.5, max_value=30.0)
)
def test_df_decreasing(tenor_a: float, tenor_b: float) -> None:
    short_t, long_t = sorted((tenor_a, tenor_b))
    df_short = df_linear(short_t)
    df_long = df_linear(long_t)
    # df_short = np.exp(-linear_interp(short_t) * short_t)
    # df_long = np.exp(-linear_interp(long_t) * long_t)
    assert df_short >= df_long



@pytest.fixture(scope="module")
def zero_curve():
    tenors = [0.5, 1, 2, 5, 10, 30]
    zero_rates_pct = [4.14, 4.37, 4.56, 4.78, 5.19, 5.73]
    return pd.Series(zero_rates_pct, index=tenors) * 0.01


@given(tenor=st.floats(min_value=0.5, max_value=30.0))
def test_pchip_within_pillar_range(zero_curve: pd.Series, tenor: float) -> None:
    rate = float(pchip_interp(tenor))
    assert zero_curve.min() <= rate <= zero_curve.max()


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