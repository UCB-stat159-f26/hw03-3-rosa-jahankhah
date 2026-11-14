import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba

from tennis_age.plotting import RESULT_COLORS, plot_age_gap

SAMPLE = pd.DataFrame(
    {
        "match_date": ["19951030", "19970307", "19970804", "19970805"],
        "opponent": ["A", "B", "C", "D"],
        "player_age": [14.1, 15.4, 15.8, 16.0],
        "opponent_age": [18.8, 26.8, 18.4, 20.0],
        "age_difference": [-4.7, -11.4, -2.6, -4.0],
        "result": ["L", "L", "W", "W"],
    }
)


def test_returns_matplotlib_axes():
    ax = plot_age_gap(SAMPLE)
    assert isinstance(ax, Axes)
    plt.close(ax.figure)


def test_x_axis_values():
    ax = plot_age_gap(SAMPLE)
    plotted = sorted(
        float(xy[0]) for coll in ax.collections for xy in coll.get_offsets()
    )
    assert plotted == sorted(SAMPLE["player_age"].tolist())
    plt.close(ax.figure)


def test_y_axis_values():
    ax = plot_age_gap(SAMPLE)
    plotted = sorted(
        float(xy[1]) for coll in ax.collections for xy in coll.get_offsets()
    )
    assert plotted == sorted(SAMPLE["age_difference"].tolist())
    plt.close(ax.figure)


def test_win_loss_color_separation():
    ax = plot_age_gap(SAMPLE)
    colors = {}
    for coll in ax.collections:
        colors[coll.get_label()] = tuple(coll.get_facecolors()[0])
    assert colors["Win"] == to_rgba(RESULT_COLORS["W"], alpha=0.7)
    assert colors["Loss"] == to_rgba(RESULT_COLORS["L"], alpha=0.7)
    assert colors["Win"] != colors["Loss"]
    plt.close(ax.figure)


def test_legend_labels():
    ax = plot_age_gap(SAMPLE)
    legend = ax.get_legend()
    assert legend is not None
    labels = [text.get_text() for text in legend.get_texts()]
    assert labels == ["Win", "Loss"]
    plt.close(ax.figure)


def test_axis_labels_and_title():
    ax = plot_age_gap(SAMPLE)
    assert ax.get_xlabel() == "Player age (years)"
    assert "Age difference" in ax.get_ylabel()
    assert "age gap" in ax.get_title().lower()
    plt.close(ax.figure)


def test_empty_dataframe():
    with pytest.raises(ValueError, match="at least one match"):
        plot_age_gap(SAMPLE.iloc[0:0])


def test_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        plot_age_gap(SAMPLE.drop(columns=["age_difference"]))


def test_invalid_input_type():
    with pytest.raises(TypeError, match="pandas DataFrame"):
        plot_age_gap([1, 2, 3])


def test_does_not_modify_input():
    original = SAMPLE.copy()
    ax = plot_age_gap(SAMPLE)
    pd.testing.assert_frame_equal(SAMPLE, original)
    plt.close(ax.figure)
