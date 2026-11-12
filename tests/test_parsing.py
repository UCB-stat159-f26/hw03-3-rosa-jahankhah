import pytest
from tennis_age.parsing import _parse_match_records


@pytest.mark.parametrize("js, expected", [
    ('var morematchmx = [["19951030", "Canadian Open"]];', "19951030"),
    ('var morematchmx = [["20010910", "Spain F10"]];', "20010910"),
])
def test_parse_match_records(js, expected):
    rows = _parse_match_records(js)
    assert rows[0][0] == expected


def test_extra_javascript():
    js = 'var morematchmx = [["20200101"]]; var other = 1;'
    assert len(_parse_match_records(js)) == 1


def test_missing_data():
    with pytest.raises(ValueError, match="Could not find"):
        _parse_match_records("var other = [];")


def test_invalid_data():
    with pytest.raises(ValueError, match="Invalid"):
        _parse_match_records("var morematchmx = [invalid];")


def test_invalid_rows():
    with pytest.raises(ValueError, match="match rows"):
        _parse_match_records('var morematchmx = ["invalid"];')
