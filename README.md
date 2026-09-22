# Mechabellum Unit Counters

A lightweight [Streamlit](https://streamlit.io/) app that ranks Mechabellum units and selected tech variants against an enemy composition.

Select the units on the opposing board, optionally give the most important threats more weight, and the app groups its recommendations into tiers from S to D/E.

## Features

- Visual selector for 28 Mechabellum units
- Counter suggestions for both base units and selected tech variants
- Optional weights for prioritizing particular enemy units
- Tiered recommendations based on the combined matchup score
- Configurable input and output grid sizes for different screen widths
- Fully local data and images; no API key or external service is required

## Getting started

### Prerequisites

- Python 3
- `pip`

### Installation

```bash
git clone https://github.com/mpeschina/MechabellumCounters.git
cd MechabellumCounters
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install the two runtime dependencies:

```bash
python -m pip install streamlit Pillow
```

Run the app from the repository root:

```bash
python -m streamlit run streamlit_app.py
```

Streamlit will print the local address in the terminal, usually `http://localhost:8501`.

## How to use it

1. Check every unit present in the enemy composition.
2. Enable **Show Weight Sliders** in the sidebar if some enemy units should influence the result more strongly.
3. Assign weights from 1 to 5 to the selected units. A higher weight gives that matchup more influence.
4. Review the counter suggestions under **Best Counter Units by Tier**.
5. Use the sidebar's column controls to adapt the grids to your screen.

Bold text beneath a result image identifies a recommended tech variant. Results without a tech label refer to the base unit.

## Scoring model

The app stores curated matchup ratings in `streamlit_app.py`. Base-unit recommendations use a weighted average across all selected enemy units. Tech-specific recommendations use the selected matchups for which an override is defined. The resulting score determines the displayed tier.

| Score | Matchup interpretation |
| ---: | --- |
| 5 | Counter wins with more than 95% health and almost no damage taken |
| 4 | Counter wins with roughly 60–95% health remaining |
| 3 | Counter wins with roughly 10–60% health remaining |
| 2 | Counter wins with less than 10% health remaining |
| 1 | Counter loses but damages the opponent |
| 0 | Counter loses while the opponent retains more than 95% health |

These ratings are practical recommendations, not live game data. Balance changes can make them outdated, and real results will also depend on positioning, levels, upgrades, tech choices, and the rest of each army.

## Project structure

```text
MechabellumCounters/
├── images/             # Unit artwork used by the interface
├── streamlit_app.py    # UI, matchup data, scoring, and tier calculation
├── LICENSE
└── README.md
```

## Updating matchup data

The relevant data structures are near the middle of `streamlit_app.py`:

- `unit_matrix` contains the base-unit matchup scores. Its columns follow the order of the dictionary's unit keys.
- `unit_overrides` contains matchup changes for particular unit techs.
- `S`, `A`, `B`, `C`, `D`, and `E` map the matchup grades to numeric scores.

When adding a unit, also add its image to `images/`, register it in `unit_images`, and keep every row of `unit_matrix` aligned with the same unit order.

## Contributing

Corrections to matchup ratings, new units, and usability improvements are welcome. Please open an issue or pull request and include the game version plus the reasoning or test setup behind balance-data changes.

## License

This repository is licensed under the [GNU General Public License v3.0](LICENSE).

Mechabellum and its associated names and artwork belong to their respective owners. This is an unofficial community project and is not affiliated with or endorsed by the game's developers or publishers.
