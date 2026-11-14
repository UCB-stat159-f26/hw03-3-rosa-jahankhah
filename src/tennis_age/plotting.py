import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_PLOT_COLUMNS = ["player_age", "age_difference", "result"]
RESULT_COLORS = {"W": "#2a9d8f", "L": "#e76f51"}
RESULT_LABELS = {"W": "Win", "L": "Loss"}


def _validate_plot_data(data):
    """Validate the plotting DataFrame without modifying it."""
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame.")
    if data.empty:
        raise ValueError("data must contain at least one match.")
    missing = [c for c in REQUIRED_PLOT_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}.")
    return data


def _prepare_plot_frame(data):
    """Copy usable win/loss rows with numeric age columns."""
    frame = data.loc[:, REQUIRED_PLOT_COLUMNS].copy()
    for column in ("player_age", "age_difference"):
        numeric = pd.to_numeric(frame[column], errors="coerce")
        if numeric.isna().any():
            raise ValueError(f"{column} must be numeric.")
        frame[column] = numeric
    frame = frame[frame["result"].isin(("W", "L"))]
    if frame.empty:
        raise ValueError("No usable match rows to plot.")
    return frame


def _scatter_result(ax, frame, result):
    """Draw one win or loss scatter series."""
    subset = frame[frame["result"] == result]
    if subset.empty:
        return
    ax.scatter(
        subset["player_age"],
        subset["age_difference"],
        c=RESULT_COLORS[result],
        label=RESULT_LABELS[result],
        alpha=0.7,
        s=28,
        edgecolors="none",
    )


def _style_age_gap_plot(ax):
    """Apply NYT-style labels, legend, and reference line."""
    ax.axhline(0, color="#666666", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Player age (years)")
    ax.set_ylabel("Age difference (player − opponent)")
    ax.set_title("Career match age gap")
    ax.legend(title="Result", frameon=True)
    ax.grid(True, alpha=0.25)
    return ax


def plot_age_gap(data):
    """Scatter plot of age difference versus player age."""
    frame = _prepare_plot_frame(_validate_plot_data(data))
    _, ax = plt.subplots(figsize=(10, 6))
    _scatter_result(ax, frame, "W")
    _scatter_result(ax, frame, "L")
    return _style_age_gap_plot(ax)
