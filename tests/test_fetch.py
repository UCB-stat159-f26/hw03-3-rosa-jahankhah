from unittest.mock import Mock, patch

import pytest
import requests

from tennis_age.players import _fetch_career_js


@patch("tennis_age.players.requests.get")
def test_fetch_serena(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        text="var morematchmx = [];",
    )
    result = _fetch_career_js("Serena Williams")
    assert result == "var morematchmx = [];"
    mock_get.assert_called_once_with(
        "https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js",
        timeout=15,
    )


@patch("tennis_age.players.requests.get")
def test_invalid_player(mock_get):
    mock_get.return_value = Mock(status_code=404)
    with pytest.raises(ValueError, match="Player not found"):
        _fetch_career_js("GastonSanchez")


@patch("tennis_age.players.requests.get")
def test_network_error(mock_get):
    mock_get.side_effect = requests.ConnectionError("Network unavailable")
    with pytest.raises(RuntimeError, match="Could not download"):
        _fetch_career_js("Serena Williams")
