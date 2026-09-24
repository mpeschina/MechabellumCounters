"""Just a helper script to re-order the unit matrix according to the desired order. 

Edit UNIT_ORDER below, then run this file from anywhere with:
    python scripts/reorganize_unit_matrix.py

It prints a replacement UNIT_MATRIX block. This can be pasted into unit_data.py.
"""

from pathlib import Path
import sys


# Make the repository root importable when this script is run from scripts/.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from unit_data import UNIT_MATRIX  # noqa: E402


# Configuration: put units in the exact order wanted in the finished matrix.
# Fire Badger is deliberately placed immediately after Mustang as an example.
UNIT_ORDER = [
    "Crawler",
    "Fang",
    "Hound",
    "Void Eye",
    "Marksman",
    "Vortex",
    "Arclight",
    "Wasp",
    "Mustang",
    "Sledgehammer",
    "Steelballs",
    "Fire Badger",
    "Stormcaller",
    "Phoenix",
    "Phantom Ray",
    "Tarantula",
    "Sabertooth",
    "Rhino",
    "Hacker",
    "Wraith",
    "Farseer",
    "Scorpion",
    "Typhoon",
    "Centurion",
    "Vulcan",
    "Fortress",
    "Melting Point",
    "Sandworm",
    "Raiden",
    "Overlord",
    "War Factory",
    "Abyss",
    "Mountain",
]

RATING_NAMES = {5: "S", 4: "A", 3: "B", 2: "C", 1: "D", 0: "E"}


def reorder_matrix(matrix: dict[str, list[int]], order: list[str]) -> dict[str, list[int]]:
    """Return *matrix* with both axes rearranged to match *order*."""
    original_order = list(matrix)

    if len(order) != len(set(order)):
        raise ValueError("UNIT_ORDER contains a unit more than once.")
    if set(order) != set(original_order):
        missing = set(original_order) - set(order)
        unknown = set(order) - set(original_order)
        raise ValueError(f"UNIT_ORDER must contain every unit once. Missing: {missing}; unknown: {unknown}")
    if any(len(row) != len(original_order) for row in matrix.values()):
        raise ValueError("Matrix must be square and use its dictionary order for columns.")

    old_column = {unit: index for index, unit in enumerate(original_order)}
    return {
        row_unit: [matrix[row_unit][old_column[column_unit]] for column_unit in order]
        for row_unit in order
    }


def format_matrix(matrix: dict[str, list[int]], variable_name: str = "UNIT_MATRIX") -> str:
    """Format a matrix in the same Python-dictionary style used by unit_data.py."""
    lines = [f"{variable_name} = {{"]
    longest_unit_name = max(len(unit) for unit in matrix)
    for unit, ratings in matrix.items():
        rating_text = ", ".join(RATING_NAMES[rating] for rating in ratings)
        # The extra space after the colon keeps every opening '[' in one column.
        padding = " " * (longest_unit_name - len(unit) + 1)
        lines.append(f'    "{unit}":{padding}[{rating_text}],')
    lines.append("}")
    return "\n".join(lines)


def run_manual_test() -> None:
    """Manual 10x10 testcase: move Unit 9 directly after Unit 1 on both axes."""
    test_matrix = {
        f"Unit {row}": [row * 10 + column for column in range(10)]
        for row in range(10)
    }
    test_order = ["Unit 0", "Unit 1", "Unit 9", "Unit 2", "Unit 3", "Unit 4", "Unit 5", "Unit 6", "Unit 7", "Unit 8"]
    reordered = reorder_matrix(test_matrix, test_order)

    # Each value is row * 10 + column, so this checks that rows AND columns moved.
    assert reordered["Unit 9"] == [90, 91, 99, 92, 93, 94, 95, 96, 97, 98]
    assert reordered["Unit 2"] == [20, 21, 29, 22, 23, 24, 25, 26, 27, 28]


if __name__ == "__main__":
    run_manual_test()
    print(format_matrix(reorder_matrix(UNIT_MATRIX, UNIT_ORDER)))
