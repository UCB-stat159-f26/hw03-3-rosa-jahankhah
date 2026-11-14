import json
import re
from datetime import datetime


def _parse_match_records(js_text):
    """Extract match records from Tennis Abstract JS."""
    if not isinstance(js_text, str):
        raise ValueError("Career data must be text.")

    match = re.search(r"\bvar\s+morematchmx\s*=", js_text)
    if match is None:
        raise ValueError("Could not find morematchmx career data.")

    try:
        rows, _ = json.JSONDecoder().raw_decode(
            js_text[match.end():].lstrip()
        )
    except json.JSONDecodeError as error:
        raise ValueError("Invalid career match data.") from error

    if not isinstance(rows, list) or any(
        not isinstance(row, list) for row in rows
    ):
        raise ValueError("Career data must contain match rows.")

    return rows


def _age_at_match(birth_date, match_date):
    """Calculate age in years on the match date."""
    try:
        birth = datetime.strptime(birth_date, "%Y%m%d")
        match = datetime.strptime(match_date, "%Y%m%d")
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid birth or match date.") from error

    if birth > match:
        raise ValueError("Birth date cannot be after match date.")

    return (match - birth).days / 365.2425


def _female_match_row(row, player_birth_date):
    """Clean a female player's individual match record."""
    if len(row) < 17:
        raise ValueError("Match record has missing fields.")

    if not row[16] or row[4] not in ("W", "L"):
        return None

    match_date = row[0]
    player_age = _age_at_match(player_birth_date, match_date)
    opponent_age = _age_at_match(row[16], match_date)

    return {
        "match_date": match_date,
        "opponent": row[11],
        "player_age": player_age,
        "opponent_age": opponent_age,
        "age_difference": player_age - opponent_age,
        "result": row[4],
    }
