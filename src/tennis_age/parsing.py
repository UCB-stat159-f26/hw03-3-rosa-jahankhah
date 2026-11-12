import json
import re


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
