import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd


BASE_URL = "https://www.tennisabstract.com"



def _parse_js(text):
    array_text = text.split("=", 1)[1].strip().rstrip(";").strip()
    return json.loads(array_text)


def _calculate_age(birth_date, match_date):
    return (match_date - birth_date).days / 365.2425


def _build_row(match, player_dob, match_date, opponent_age):
    if match_date < player_dob or opponent_age < 0:
        return None
    player_age = _calculate_age(player_dob, match_date)
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


# def _clean_match(match, player_dob):
#     if not match[0] or not match[16]:
#         return None
#     try:
#         match_date = pd.to_datetime(match[0], format="%Y%m%d")
#         opponent_dob = pd.to_datetime(match[16], format="%Y%m%d")
#     except (ValueError, TypeError, IndexError):
#         return None
#     if match_date < player_dob or opponent_dob > match_date:
#         return None
#     player_age = _calculate_age(player_dob, match_date)
#     opponent_age = _calculate_age(opponent_dob, match_date)
#     return {
#         "date": match_date,
#         "tournament": match[1],
#         "surface": match[2],
#         "result": match[4],
#         "opponent": match[11],
#         "player_age": round(player_age, 2),
#         "opponent_age": round(opponent_age, 2),
#         "age_difference": round(player_age - opponent_age, 2),
#     }


def _clean_match(match, player_dob):
    try:
        match_date = pd.to_datetime(match[0], format="%Y%m%d")
        opponent_dob = pd.to_datetime(match[16], format="%Y%m%d")
    except (ValueError, TypeError, IndexError):
        return None
    if opponent_dob > match_date:
        return None
    opponent_age = _calculate_age(opponent_dob, match_date)
    return _build_row(match, player_dob, match_date, opponent_age)

def _clean_female_data(matches, player_dob):
    rows = [_clean_match(match, player_dob) for match in matches]
    return pd.DataFrame(row for row in rows if row is not None)


def _clean_male_match(match, player_dob):
    try:
        match_date = pd.to_datetime(match[0], format="%Y%m%d")
        opponent_age = float(match[16])
    except (ValueError, TypeError, IndexError):
        return None
    return _build_row(match, player_dob, match_date, opponent_age)


def _player_slug(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Please provide a player's name.")
    words = re.findall(r"[A-Za-z]+", name)
    if not words:
        raise ValueError("Please provide a valid player's name.")
    return "".join(word[0].upper() + word[1:] for word in words)


def _download(url):
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/javascript,*/*;q=0.1",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise ValueError(
            f"Could not retrieve Tennis Abstract data: {exc}"
        ) from exc


def _get_player_dob(slug):
    url = f"{BASE_URL}/jsmatches/{slug}.js"
    text = _download(url)
    match = re.search(r"\bvar\s+dob\s*=\s*['\"]?(\d{8})", text)
    if not match:
        raise ValueError(f"Could not find a birth date for {slug}.")
    return pd.to_datetime(match.group(1), format="%Y%m%d")

def get_player_data(name):
    slug = _player_slug(name)
    career_url = f"{BASE_URL}/jsmatches/{slug}Career.js"
    matches = _parse_js(_download(career_url))
    if not matches:
        raise ValueError(f"No career matches found for {name!r}.")
    is_women = len(matches[0]) <= 30
    player_dob = _get_player_dob(slug)
    cleaner = _clean_female_data if is_women else _clean_male_data
    data = cleaner(matches, player_dob)
    if data.empty:
        raise ValueError(f"No usable career matches found for {name!r}.")
    return data


def _clean_male_data(matches, player_dob):
    rows = [_clean_male_match(match, player_dob) for match in matches]
    return pd.DataFrame(row for row in rows if row is not None)