"""Tennis player career age analysis.

Public API:
    get_player_matches — download and clean career match data
    plot_age_gap — scatter plot of age difference versus player age
"""

from tennis_age.players import get_player_matches
from tennis_age.plotting import plot_age_gap

__all__ = ["get_player_matches", "plot_age_gap"]
