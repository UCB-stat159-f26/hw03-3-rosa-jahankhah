import matplotlib

matplotlib.use("Agg")

from unittest.mock import patch

import pandas as pd
import pytest
from matplotlib.axes import Axes

import tennis_age
from tennis_age import get_player_matches, plot_age_gap

SAMPLE_JS = (
    'var morematchmx = ['
    '["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", '
    '"6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119"]'
    '];'
)


def _mock_downloads(birth_date="19810926", career_js=SAMPLE_JS):
    return patch.multiple(
        "tennis_age.players",
        _player_birth_date=lambda name: birth_date,
        _fetch_career_js=lambda name: career_js,
    )


def test_public_imports_from_package():
    assert callable(tennis_age.get_player_matches)
    assert callable(tennis_age.plot_age_gap)
    assert get_player_matches is tennis_age.get_player_matches
    assert plot_age_gap is tennis_age.plot_age_gap
    assert "get_player_matches" in tennis_age.__all__
    assert "plot_age_gap" in tennis_age.__all__


def test_public_functions_are_documented():
    assert get_player_matches.__doc__
    assert plot_age_gap.__doc__
    assert "DataFrame" in get_player_matches.__doc__
    assert "Axes" in plot_age_gap.__doc__ or "matplotlib" in plot_age_gap.__doc__


def test_public_data_returns_dataframe():
    with _mock_downloads():
        frame = get_player_matches("Serena Williams")
    assert isinstance(frame, pd.DataFrame)
    assert {"player_age", "age_difference", "result"} <= set(frame.columns)
    assert len(frame) == 1


def test_public_data_feeds_plotting_function():
    with _mock_downloads():
        frame = get_player_matches("Serena Williams")
    ax = plot_age_gap(frame)
    assert isinstance(ax, Axes)
    assert len(ax.collections) >= 1


def test_invalid_public_data_input():
    with pytest.raises(ValueError, match="non-empty string"):
        get_player_matches("")


def test_invalid_public_plot_input():
    with pytest.raises(TypeError, match="pandas DataFrame"):
        plot_age_gap("not a dataframe")
