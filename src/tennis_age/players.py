import re

import requests


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


def _fetch_career_js(player_name):
    """Download a player's career match JavaScript file."""
    player_id = _normalize_player_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{player_id}Career.js"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 404:
            raise ValueError(f"Player not found: {player_name}")
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Could not download player data: {error}") from error
    return response.text
