#!/usr/bin/env python3
"""
Create the unfinished/lower part of unit_matrix from the corrected rows.

Reciprocal matchup rules:
    S -> E
    E -> S
    A/B/C -> D
    D -> "_"

The diagonal is always C.

The first 12 rows (Crawler ... Fire Badger) are treated as correct.
All rows below them are rebuilt from those rows.

Existing/broken rows below the corrected block are ignored.
"""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any


REVERSE = {
    "S": "E",
    "E": "S",
    "A": "D",
    "B": "D",
    "C": "D",
    "D": "_",
}


def load_matrix(path: str | Path) -> dict[str, list[Any]]:
    """Load unit_matrix from new_matrix.py."""
    namespace = runpy.run_path(str(path))
    matrix = namespace.get("unit_matrix")

    if not isinstance(matrix, dict):
        raise ValueError(
            f"{path} does not define a dict named 'unit_matrix'."
        )

    return matrix


def value_to_symbol(value: int) -> str:
    """Convert numeric value to S/A/B/C/D/E."""
    return {
        5: "S",
        4: "A",
        3: "B",
        2: "C",
        1: "D",
        0: "E",
    }[value]


def validate_trusted_rows(
    matrix: dict[str, list[Any]],
    trusted_count: int,
) -> int:
    """
    Validate only the trusted rows.

    Returns the correct matrix size (number of columns).
    """
    names = list(matrix)

    if trusted_count > len(names):
        raise ValueError(
            f"trusted_count={trusted_count}, but matrix only contains "
            f"{len(names)} rows."
        )

    trusted_names = names[:trusted_count]

    # Determine the real matrix size from the first trusted row.
    expected_size = len(matrix[trusted_names[0]])

    for row_name in trusted_names:
        row = matrix[row_name]

        if len(row) != expected_size:
            raise ValueError(
                f"Trusted row '{row_name}' has {len(row)} entries; "
                f"expected {expected_size}."
            )

        for value in row:
            if value not in range(6):
                raise ValueError(
                    f"Trusted row '{row_name}' contains invalid value "
                    f"{value!r}."
                )

    return expected_size


def build_matrix(
    matrix: dict[str, list[int]],
    trusted_count: int,
    matrix_size: int,
) -> tuple[list[str], dict[str, list[str]]]:
    """
    Rebuild all rows below the trusted block.

    For row i / column j:
        look at row j / column i
        and apply the reciprocal mapping.
    """
    names = list(matrix)
    trusted_names = names[:trusted_count]

    result: dict[str, list[str]] = {}

    # Keep the corrected rows unchanged.
    for name in trusted_names:
        result[name] = [
            value_to_symbol(value)
            for value in matrix[name]
        ]

    # Rebuild all rows below the corrected block.
    for i in range(trusted_count, len(names)):
        row_name = names[i]

        # Start with "_" everywhere.
        row = ["_"] * matrix_size

        # Diagonal is always C.
        row[i] = "C"

        # The only entries we can currently derive are those whose
        # reciprocal value exists in one of the trusted rows.
        for j in range(trusted_count):

            source_symbol = value_to_symbol(
                matrix[trusted_names[j]][i]
            )

            row[j] = REVERSE[source_symbol]

        result[row_name] = row

    return names, result


def format_matrix(
    names: list[str],
    matrix: dict[str, list[str]],
) -> str:
    """
    Format matrix so all '[' characters are vertically aligned.
    """
    name_width = max(len(name) for name in names)

    lines = [
        "S = 5 # unit wins, >95% HP left with nearly no damage",
        "A = 4 # unit wins, 60-95% HP left",
        "B = 3 # unit wins, 10-60% HP left",
        "C = 2 # unit wins, <10% HP left",
        "D = 1 # unit loose, Opponent is damaged",
        "E = 0 # unit loose, Opponent >95% HP",
        "unit_matrix = {",
    ]

    for name in names:
        entries = ", ".join(matrix[name])

        lines.append(
            f'    "{name.ljust(name_width)}": [{entries}],'
        )

    lines.append("}")

    return "\n".join(lines)


def main() -> None:
    INPUT_FILE = "new_matrix.py"

    # Number of rows that are already known to be correct.
    ALREADY_CORRECT_NUMBER = 12

    matrix = load_matrix(INPUT_FILE)

    # IMPORTANT:
    # Validate only the known-good rows.
    matrix_size = validate_trusted_rows(
        matrix,
        ALREADY_CORRECT_NUMBER,
    )

    names, completed = build_matrix(
        matrix,
        ALREADY_CORRECT_NUMBER,
        matrix_size,
    )

    output_text = format_matrix(
        names,
        completed,
    )

    print(output_text)


if __name__ == "__main__":
    main()