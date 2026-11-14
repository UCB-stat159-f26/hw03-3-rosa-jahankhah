import pytest
from tennis_age.parsing import _male_match_row

NADAL_BIRTH = "19860603"

SAMPLE_ROW = [
    "20010910", "Spain F10", "Hard", "S", "L",
    "", "", "WC", "R32", "2-6 7-5 6-2", "3",
    "Guillermo Platel", "731", "", "", "R", "22.264202601",
]


def test_nadal_match_ages():
    match = _male_match_row(SAMPLE_ROW, NADAL_BIRTH)
    assert match["player_age"] == pytest.approx(15.27, abs=0.01)
    assert match["opponent_age"] == pytest.approx(22.264202601, abs=1e-9)


def test_nadal_age_difference():
    match = _male_match_row(SAMPLE_ROW, NADAL_BIRTH)
    assert match["age_difference"] == pytest.approx(15.27 - 22.264202601, abs=0.01)


def test_nadal_opponent_name():
    match = _male_match_row(SAMPLE_ROW, NADAL_BIRTH)
    assert match["opponent"] == "Guillermo Platel"
    assert match["match_date"] == "20010910"


def test_male_win():
    row = SAMPLE_ROW.copy()
    row[4] = "W"
    assert _male_match_row(row, NADAL_BIRTH)["result"] == "W"


def test_missing_opponent_age():
    row = SAMPLE_ROW.copy()
    row[16] = ""
    assert _male_match_row(row, NADAL_BIRTH) is None


def test_short_match_record():
    with pytest.raises(ValueError, match="missing fields"):
        _male_match_row(["20010910"], NADAL_BIRTH)


def test_invalid_player_birthdate():
    with pytest.raises(ValueError, match="Invalid"):
        _male_match_row(SAMPLE_ROW, "invalid")


def test_invalid_opponent_age():
    row = SAMPLE_ROW.copy()
    row[16] = "not-an-age"
    with pytest.raises(ValueError, match="Invalid opponent age"):
        _male_match_row(row, NADAL_BIRTH)
