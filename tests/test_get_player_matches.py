from unittest.mock import patch

import pandas as pd
import pytest

from tennis_age import get_player_matches

FEMALE_JS = (
    'var morematchmx = ['
    '["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", '
    '"6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", '
    '"USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"],'
    '["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", '
    '"6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", '
    '"19700503", "", "FRA", "0", "", "", "", "", "", "", '
    '"1997-W-WT-USA-02A-1997-006"],'
    '["19970804", "Manhattan Beach", "Hard", "W", "W", "", "", "WC", "Q3", '
    '"7-6 4-6 6-3", "3", "Magui Serna", "54", "6", "", "L", "19790301", '
    '"167", "ESP", "0", "", "", "", "", "", "", '
    '"1997-W-WT-USA-07A-1997-026"],'
    '["19970804", "Manhattan Beach", "Hard", "W", "L", "", "", "WC", "Q3", '
    '"7-6 4-6 6-3", "3", "Missing Birth", "54", "6", "", "L", "", '
    '"167", "ESP", "0", "", "", "", "", "", "", "skip-me"]'
    '];'
)

MALE_JS = (
    'var morematchmx = ['
    '["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", '
    '"2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", '
    '"22.264202601", "", "ESP", "0", "", "", "", "", "", "", "", "", "", '
    '"", "", "", "", "", "", "", "", "", "", "", "", "", "", "", '
    '"2001-M-FU-ESP-10A-2001-002", "", "1", "1"],'
    '["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", '
    '"6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", '
    '"18.7597535934", "", "ESP", "0", "", "", "", "", "", "", "", "", "", '
    '"", "", "", "", "", "", "", "", "", "", "", "", "", "", "", '
    '"2001-784-015", "", "1", "1"],'
    '["20010917", "Seville CH", "Clay", "C", "L", "", "", "WC", "R16", '
    '"3-6 6-1 6-3", "3", "No Age", "161", "2", "", "R", "", "178", "ITA", '
    '"0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", '
    '"", "", "", "", "2", "", "", "", "2001-784-024", "", "2", "2"]'
    '];'
)

EMPTY_JS = 'var morematchmx = [];'


def _mock_player(birth_date, career_js):
    return patch.multiple(
        "tennis_age.players",
        _player_birth_date=lambda name: birth_date,
        _fetch_career_js=lambda name: career_js,
    )


def test_serena_dataframe():
    with _mock_player("19810926", FEMALE_JS):
        frame = get_player_matches("Serena Williams")
    assert list(frame.columns) == [
        "match_date", "opponent", "player_age",
        "opponent_age", "age_difference", "result",
    ]
    assert len(frame) == 3
    assert frame.iloc[0]["opponent"] == "Anne Miller"
    assert frame.iloc[0]["player_age"] == pytest.approx(14.09, abs=0.01)
    assert frame.iloc[0]["opponent_age"] == pytest.approx(18.78, abs=0.01)
    assert frame.iloc[0]["age_difference"] == pytest.approx(-4.68, abs=0.01)
    assert frame.iloc[2]["result"] == "W"


def test_nadal_dataframe():
    with _mock_player("19860603", MALE_JS):
        frame = get_player_matches("Rafael Nadal")
    assert len(frame) == 2
    assert frame.iloc[0]["opponent"] == "Guillermo Platel"
    assert frame.iloc[0]["player_age"] == pytest.approx(15.27, abs=0.01)
    assert frame.iloc[0]["opponent_age"] == pytest.approx(22.264202601)
    assert frame.iloc[1]["result"] == "W"


@pytest.mark.parametrize("name", [
    "serena williams",
    "Serena Williams",
    "SerenaWilliams",
])
def test_name_formats(name):
    with _mock_player("19810926", FEMALE_JS):
        frame = get_player_matches(name)
    assert len(frame) == 3


def test_numeric_age_columns():
    with _mock_player("19860603", MALE_JS):
        frame = get_player_matches("Rafael Nadal")
    for column in ("player_age", "opponent_age", "age_difference"):
        assert pd.api.types.is_numeric_dtype(frame[column])
    assert (
        frame["age_difference"] == frame["player_age"] - frame["opponent_age"]
    ).all()


def test_excludes_missing_and_malformed_rows():
    with _mock_player("19810926", FEMALE_JS):
        frame = get_player_matches("Serena Williams")
    assert "Missing Birth" not in set(frame["opponent"])


@patch(
    "tennis_age.players._player_birth_date",
    side_effect=ValueError("Player not found: GastonSanchez"),
)
def test_invalid_player_name(mock_birth):
    with pytest.raises(ValueError, match="Player not found"):
        get_player_matches("GastonSanchez")


def test_no_usable_matches():
    with _mock_player("19810926", EMPTY_JS):
        with pytest.raises(ValueError, match="No usable match records"):
            get_player_matches("Serena Williams")
