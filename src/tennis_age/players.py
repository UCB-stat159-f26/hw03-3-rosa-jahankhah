import re
from datetime import datetime

import pandas as pd
import requests

from tennis_age.parsing import (
    _clean_match_records,
    _parse_match_records,
)

EXPECTED_COLUMNS = [
    "match_date",
    "opponent",
    "player_age",
    "opponent_age",
    "age_difference",
    "result",
]


def _normalize_player_name(name):
    """Convert a player name to Tennis Abstract format."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Player name must be a non-empty string.")
    name = name.strip()
    if re.search(r"[\s_-]", name):
        return "".join(
            part.capitalize()
            for part in re.split(r"[\s_-]+", name)
            if part
        )
    return name[0].upper() + name[1:]


def _download_text(url, player_name):
    """Download text from Tennis Abstract, with shared error handling."""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 404:
            raise ValueError(f"Player not found: {player_name}")
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Could not download player data: {error}") from error
    return response.text


def _fetch_career_js(player_name):
    """Download a player's career match JavaScript file."""
    player_id = _normalize_player_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{player_id}Career.js"
    return _download_text(url, player_name)


def _fetch_player_page(player_name):
    """Download a player's Tennis Abstract profile page."""
    player_id = _normalize_player_name(player_name)
    url = f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={player_id}"
    return _download_text(url, player_name)


def _parse_birth_date(page_text):
    """Extract a validated YYYYMMDD birth date from player page text."""
    if not isinstance(page_text, str):
        raise ValueError("Player page must be text.")
    match = re.search(r"\bvar\s+dob\s*=\s*(\d{8})\s*;", page_text)
    if match is None:
        raise ValueError("Could not find player birth date.")
    birth_date = match.group(1)
    try:
        datetime.strptime(birth_date, "%Y%m%d")
    except ValueError as error:
        raise ValueError("Invalid player birth date.") from error
    return birth_date


def _player_birth_date(player_name):
    """Retrieve a player's birth date from Tennis Abstract."""
    return _parse_birth_date(_fetch_player_page(player_name))


def _matches_dataframe(records):
    """Build a cleaned pandas DataFrame from match records."""
    if not records:
        raise ValueError("No usable match records found.")
    frame = pd.DataFrame(records, columns=EXPECTED_COLUMNS)
    frame = frame.drop_duplicates().reset_index(drop=True)
    for column in ("player_age", "opponent_age", "age_difference"):
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    return frame


def get_player_matches(player_name):
    """Return a cleaned career-match DataFrame for a tennis player."""
    birth_date = _player_birth_date(player_name)
    rows = _parse_match_records(_fetch_career_js(player_name))
    return _matches_dataframe(_clean_match_records(rows, birth_date))
