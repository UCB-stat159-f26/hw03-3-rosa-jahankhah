# Tennis Age Package

## Project Overview

`tennis-age-package` is a Python package for UC Berkeley STAT 159 HW3. It downloads career match data from [Tennis Abstract](https://www.tennisabstract.com/), cleans it into a pandas DataFrame, and creates a scatter plot of each match’s age gap over a player’s career.

The package is designed to work for many players—not just one fixed dataset—so the same two public functions can analyze Serena Williams, Rafael Nadal, or another player with available Tennis Abstract career data.

Public API:

- `get_player_matches(player_name)` — download, parse, and clean career matches
- `plot_age_gap(data)` — scatter plot of age difference versus player age

## Installation

### From GitHub

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-rosa-jahankhah.git
```

### Local development

```bash
git clone https://github.com/UCB-stat159-f26/hw03-3-rosa-jahankhah.git
cd hw03-3-rosa-jahankhah
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Requires Python 3.10+.

## Usage

```python
from tennis_age import get_player_matches, plot_age_gap

# Flexible name formats are supported
serena = get_player_matches("Serena Williams")
rafa = get_player_matches("Rafael Nadal")

# Also valid: "serena williams", "SerenaWilliams"

ax_serena = plot_age_gap(serena)
ax_serena.set_title("Serena Williams career match age gap")
ax_serena.figure.savefig("serena_age_gap.png", dpi=150)

ax_rafa = plot_age_gap(rafa)
ax_rafa.set_title("Rafael Nadal career match age gap")
ax_rafa.figure.savefig("rafa_age_gap.png", dpi=150)
```

`plot_age_gap` returns a matplotlib `Axes`, so you can change the title, adjust layout, or save the figure as shown above.

## DataFrame Columns

`get_player_matches()` returns a DataFrame with these columns:

| Column | Description |
|--------|-------------|
| `match_date` | Match date as `YYYYMMDD` text |
| `opponent` | Opponent’s name |
| `player_age` | Player’s age in years on the match date (numeric) |
| `opponent_age` | Opponent’s age in years on the match date (numeric) |
| `age_difference` | `player_age - opponent_age` (numeric) |
| `result` | Match result: `"W"` (win) or `"L"` (loss) |

Rows with missing or unusable age information are excluded. Exact duplicate rows are removed.

## Visualization

`plot_age_gap(data)` creates a career age-gap scatter plot similar in spirit to the NYT-style visualization from HW2 (without point annotations):

- **X-axis:** player age in years
- **Y-axis:** age difference (`player_age - opponent_age`)
- **Win color:** teal (`#2a9d8f`)
- **Loss color:** coral (`#e76f51`)
- A dashed horizontal line at `y = 0` marks matches against same-age opponents
- Negative values mean the player was younger than the opponent; positive values mean older

## Package Design

Source layout under `src/tennis_age/`:

| Module | Role |
|--------|------|
| `__init__.py` | Exports the public API |
| `players.py` | Name normalization, downloads, birth-date retrieval, `get_player_matches` |
| `parsing.py` | Career JS parsing and male/female match cleaning |
| `plotting.py` | Scatter plot validation, styling, and `plot_age_gap` |

### Male vs female match data

Tennis Abstract career files differ by tour:

- **Female players:** opponent field includes a birth date (`YYYYMMDD`). Opponent age is computed from that birth date and the match date.
- **Male players:** opponent field already includes age as a numeric value.

The package detects which layout a row uses from the data itself. It does not hardcode player names or genders.

## Testing

Install development dependencies, then run:

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Automated tests use mocked Tennis Abstract responses so they do **not** contact the live website. They cover name normalization, downloads, parsing, male and female row cleaning, birth-date retrieval, the public DataFrame API, plotting, and package imports.

## Error Handling

The package raises clear errors for common failure cases:

- **Invalid or empty player names** — `ValueError` (for example, empty strings or players not found on Tennis Abstract)
- **Missing birth date or unusable career data** — `ValueError` explaining what could not be found or parsed
- **No usable matches after cleaning** — `ValueError`
- **Network or HTTP download failures** — `RuntimeError`
- **Invalid plotting input** — `TypeError` / `ValueError` for non-DataFrames, empty frames, missing columns, or non-numeric ages

## Personal Reflections

In this homework, I learned more about how to build a Python package and make my code reusable for different datasets. In HW2, I was mainly working with Serena Williams's data and creating a visualization, but in this assignment, I had to make the code work for different tennis players.

One interesting challenge was understanding how Tennis Abstract stores data differently for male and female players. For female players, I needed to calculate the opponent's age using their birth date, while for male players, the age was already provided. I learned that even when two datasets look similar, small differences in their structure can affect the results.

I also learned more about writing tests and why they are important. Instead of testing everything manually, I used pytest and mock data to check different cases, including invalid names, missing values, and errors. This helped me make sure that my functions were working without depending on the website every time.

Another important part was using Git and making commits during the development process. I tried to separate my work into smaller steps and test each part before moving to the next one. I think this made it easier to understand my code and find problems.

Overall, this assignment helped me understand the difference between writing code for one specific project and building a package that other people can install and use. I also got more comfortable organizing Python files, writing smaller functions, and connecting different parts of a project together.

## AI Usage Disclosure

This project used generative AI tools during development. Full details—including tools, how they were used, representative prompts, and verification steps—are in [AI_USAGE.md](AI_USAGE.md).
