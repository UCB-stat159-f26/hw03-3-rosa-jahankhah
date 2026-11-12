import re


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
