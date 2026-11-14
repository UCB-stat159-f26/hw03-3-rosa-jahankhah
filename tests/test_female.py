import pytest
from tennis_age.parsing import _female_match_row

SERENA_BIRTH = "19810926"

SAMPLE_ROW = [
    "19951030", "Canadian Open", "Carpet", "W", "L",
    "", "", "WC", "Q1", "6-1 6-1", "3",
    "Anne Miller", "149", "7", "", "R", "19770119",
]


def test_female_match_ages():
    match = _female_match_row(SAMPLE_ROW, SERENA_BIRTH)
    assert match["player_age"] == pytest.approx(14.09, abs=0.01)
    assert match["opponent_age"] == pytest.approx(18.78, abs=0.01)


def test_female_age_difference():
    match = _female_match_row(SAMPLE_ROW, SERENA_BIRTH)
    assert match["age_difference"] == pytest.approx(-4.68, abs=0.01)


def test_female_win():
    row = SAMPLE_ROW.copy()
    row[4] = "W"
    assert _female_match_row(row, SERENA_BIRTH)["result"] == "W"


def test_missing_opponent_birthdate():
    row = SAMPLE_ROW.copy()
    row[16] = ""
    assert _female_match_row(row, SERENA_BIRTH) is None


def test_short_match_record():
    with pytest.raises(ValueError, match="missing fields"):
        _female_match_row(["19951030"], SERENA_BIRTH)


def test_invalid_player_birthdate():
    with pytest.raises(ValueError, match="Invalid"):
        _female_match_row(SAMPLE_ROW, "invalid")
