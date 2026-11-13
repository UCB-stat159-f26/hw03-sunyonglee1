import json
import pandas as pd


def _parse_js(text):
    array_text = text.split("=", 1)[1].strip().rstrip(";").strip()
    return json.loads(array_text)


def _calculate_age(birth_date, match_date):
    return (match_date - birth_date).days / 365.2425


def _clean_match(match, player_dob):
    if not match[0] or not match[16]:
        return None
    try:
        match_date = pd.to_datetime(match[0], format="%Y%m%d")
        opponent_dob = pd.to_datetime(match[16], format="%Y%m%d")
    except (ValueError, TypeError, IndexError):
        return None
    if match_date < player_dob or opponent_dob > match_date:
        return None
    player_age = _calculate_age(player_dob, match_date)
    opponent_age = _calculate_age(opponent_dob, match_date)
    return {
        "date": match_date,
        "tournament": match[1],
        "surface": match[2],
        "result": match[4],
        "opponent": match[11],
        "player_age": round(player_age, 2),
        "opponent_age": round(opponent_age, 2),
        "age_difference": round(player_age - opponent_age, 2),
    }

def _clean_female_data(matches, player_dob):
    rows = [_clean_match(match, player_dob) for match in matches]
    return pd.DataFrame(row for row in rows if row is not None)
