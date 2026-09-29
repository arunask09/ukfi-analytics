from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from ukfi_analytics.curves import DF, cubic_interp, linear_interp, tenors, zero_rate

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def main() -> None:
    print(zero_rate)
    print(DF)
    print(linear_interp(7.5))
    print(cubic_interp(7.5))

    grid = np.linspace(min(tenors), max(tenors), 200)
    linear_vals = linear_interp(grid)
    cubic_vals = cubic_interp(grid)

    OUT_DIR.mkdir(exist_ok=True)

    plt.plot(grid, linear_vals, label="linear")
    plt.plot(grid, cubic_vals, label="cubic spline")
    plt.scatter(tenors, zero_rate, color="black", label="pillars", zorder=5)
    plt.xlabel("tenor (years)")
    plt.ylabel("zero rate")
    plt.legend()
    plt.savefig(OUT_DIR / "curve_interp.png")

    fig = go.Figure()
    fig.add_scatter(x=grid, y=linear_vals, mode="lines", name="linear")
    fig.add_scatter(x=grid, y=cubic_vals, mode="lines", name="cubic spline")
    fig.add_scatter(x=tenors, y=zero_rate, mode="markers", name="pillars")
    fig.write_html(OUT_DIR / "curve_interp_plotly.html")


if __name__ == "__main__":
    main()
