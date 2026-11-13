import pandas as pd

from unittest.mock import patch


from tennis_package.data import (
    _clean_female_data,
    _clean_male_data,
    _parse_js,
    get_player_data,
)


FEMALE_JS = '''var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"]];'''


def test_clean_female_match():
    matches = _parse_js(FEMALE_JS)
    data = _clean_female_data(matches, pd.Timestamp("1981-09-26"))

    assert len(data) == 1
    assert data.loc[0, "opponent"] == "Anne Miller"
    assert data.loc[0, "result"] == "L"
    assert data.loc[0, "opponent_age"] > 18


from tennis_package.data import (
    _clean_female_data,
    _clean_male_data,
    _parse_js,
)


MALE_JS = '''var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601"]];'''


def test_clean_male_match():
    matches = _parse_js(MALE_JS)
    data = _clean_male_data(matches, pd.Timestamp("1981-09-26"))

    assert len(data) == 1
    assert data.loc[0, "opponent"] == "Guillermo Platel"
    assert data.loc[0, "result"] == "L"
    assert data.loc[0, "opponent_age"] == 22.26


def test_get_player_data_uses_mocked_downloads():
    with patch(
        "tennis_package.data._download",
        side_effect=[FEMALE_JS, "var dob=19810926;"],
    ) as download:
        data = get_player_data("Serena Williams")

    assert len(data) == 1
    assert data.loc[0, "opponent"] == "Anne Miller"
    assert download.call_count == 2