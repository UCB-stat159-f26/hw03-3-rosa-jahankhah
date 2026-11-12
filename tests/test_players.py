import pytest
from tennis_age.players import _normalize_player_name


@pytest.mark.parametrize("name, expected", [
    ("serena williams", "SerenaWilliams"),
    ("Serena Williams", "SerenaWilliams"),
    ("SerenaWilliams", "SerenaWilliams"),
    ("Rafael Nadal", "RafaelNadal"),
])
def test_normalize_player_name(name, expected):
    assert _normalize_player_name(name) == expected


def test_empty_player_name():
    with pytest.raises(ValueError):
        _normalize_player_name("")
