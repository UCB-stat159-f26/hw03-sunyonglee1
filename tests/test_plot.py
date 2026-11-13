import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from tennis_package import plot_age_matches


def test_plot_age_matches():
    data = pd.DataFrame({
        "player_age": [20, 21],
        "age_difference": [3, -2],
        "result": ["W", "L"],
    })

    figure = plot_age_matches(data)
    axis = figure.axes[0]

    assert axis.get_xlabel() == "Player age"
    assert axis.get_ylabel() == "Age difference (player − opponent)"
    assert len(axis.get_legend().get_texts()) == 2
    plt.close(figure)