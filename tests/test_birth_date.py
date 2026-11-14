from unittest.mock import Mock, patch

import pytest
import requests

from tennis_age.players import _parse_birth_date, _player_birth_date


@patch("tennis_age.players.requests.get")
def test_serena_birth_date(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        text="var peaklast = 20170508; var dob = 19810926; var ht = 175;",
    )
    assert _player_birth_date("Serena Williams") == "19810926"
    mock_get.assert_called_once_with(
        "https://www.tennisabstract.com/cgi-bin/player.cgi?p=SerenaWilliams",
        timeout=15,
        headers={
            "User-Agent": "tennis-age-package/0.1 (STAT159 academic use)",
        },
    )


@patch("tennis_age.players.requests.get")
def test_nadal_birth_date(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        text="var peaklast = 20200120; var dob = 19860603; var ht = 185;",
    )
    assert _player_birth_date("Rafael Nadal") == "19860603"


@patch("tennis_age.players.requests.get")
def test_missing_birth_date(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        text="var peaklast = 20170508; var ht = 175;",
    )
    with pytest.raises(ValueError, match="Could not find player birth date"):
        _player_birth_date("Unknown Player")


@patch("tennis_age.players.requests.get")
def test_malformed_birth_date(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        text="var dob = notadate; var ht = 175;",
    )
    with pytest.raises(ValueError, match="Could not find player birth date"):
        _player_birth_date("Serena Williams")


def test_invalid_calendar_birth_date():
    with pytest.raises(ValueError, match="Invalid player birth date"):
        _parse_birth_date("var dob = 19811399;")


@patch("tennis_age.players.requests.get")
def test_player_not_found(mock_get):
    mock_get.return_value = Mock(status_code=404)
    with pytest.raises(ValueError, match="Player not found"):
        _player_birth_date("GastonSanchez")


@patch("tennis_age.players.requests.get")
def test_network_error(mock_get):
    mock_get.side_effect = requests.ConnectionError("Network unavailable")
    with pytest.raises(RuntimeError, match="Could not download"):
        _player_birth_date("Serena Williams")
