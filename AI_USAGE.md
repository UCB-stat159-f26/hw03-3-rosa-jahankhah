# AI Usage Disclosure

This file describes how I used AI tools while working on STAT 159 HW3 (Python package for tennis career age analysis). I am documenting this for transparency, following the course AI Tools policy.

## AI Tools Used

### ChatGPT (OpenAI, GPT-6)

I used ChatGPT to understand the assignment, break the work into smaller steps, get ideas for functions and tests, and prepare documentation. ChatGPT helped me plan the overall package structure before I implemented things in Cursor.

> Note: Please confirm the exact ChatGPT model label shown in your OpenAI interface if “GPT-6” needs to be updated for grading.

### Cursor AI Agent

I used the Cursor AI Agent heavily during implementation. In this project, the agent helped write Python functions, create pytest tests, debug failing cases, check Serena Williams and Rafael Nadal results, update documentation, and create/push Git commits.

Cursor model / version used in this workspace:

- Product identity available in-session: **Cursor Auto / Composer agent**
- Exact billed model name/version: **[FILL IN — I could not independently verify the exact Cursor model version string from this session]**

## How I Used AI

I used AI as an active coding assistant throughout most of HW3, not only for small edits. In particular, AI helped with:

- Understanding HW3 requirements and how a Python package should be organized (`pyproject.toml`, `src/tennis_age/`, tests)
- Downloading and parsing Tennis Abstract career JavaScript files
- Processing female and male match records differently (birth dates vs opponent ages)
- Calculating player ages and age differences
- Building the public `get_player_matches()` DataFrame function
- Creating the `plot_age_gap()` scatter plot
- Writing and running automated tests with mocked (offline) responses
- Debugging edge cases such as missing values, invalid names, and network-style errors
- Writing README documentation and polishing personal reflections wording earlier in the process
- Organizing the work into meaningful Git commits

Much of the package code and many tests were drafted or revised with AI assistance. I reviewed the results, ran tests, and checked real Serena/Nadal outputs myself so I could understand and defend the submitted work.

## Main Prompts

These are representative prompts I used while developing the package:

- "Implement male player match processing and add automated tests."
- "Automatically retrieve player birth dates without hardcoding players."
- "Create a public function that returns a clean pandas DataFrame."
- "Implement the age difference scatter plot and test it."
- "Review the package for edge cases and verify the tests."

Additional prompts from my Cursor conversation history for this repository include step-by-step requests such as creating `pyproject.toml` and `.gitignore`, adding player-name normalization and download/parsing helpers, implementing female match age calculations, and completing later commits for the public API, plotting, README documentation, and this AI disclosure file. Early prompts were often short instructions to paste starter code; later prompts were longer “continue HW3 / complete Commit N” requests that asked the agent to implement, test, commit, and push each stage.

## Verification

I did not rely on AI output alone. I verified the work by:

- Running `python -m pytest -q` (currently 60 automated tests, all offline/mocked for website access)
- Checking live Serena Williams and Rafael Nadal data through `get_player_matches()`
- Saving and visually inspecting scatter plots for both players
- Confirming invalid names and bad inputs raise clear errors

I understand that under the course policy I remain responsible for explaining any AI-assisted code or text included in this submission.
