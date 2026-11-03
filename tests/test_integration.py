"""Проверки взаимодействия модулей ввода, анализа и вывода."""

import pytest

from src.integration import run_pipeline


@pytest.mark.parametrize(
    "matrix, expected",
    [
        ([[0]], (0, 0, 0, 0)),
        ([[5]], (0, 0, 0, 0)),
        ([[0, 0], [0, 0]], (1, 1, 1, 1)),
        ([[1, 2], [3, 4]], (0, 0, 0, 0)),
        (
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            (3, 3, 2, 2),
        ),
    ],
)
def test_pipeline_valid_matrix(matrix, expected):
    report = run_pipeline(matrix)
    lines = report.splitlines()

    assert lines[0] == "Результаты анализа:"
    actual = tuple(int(line.rsplit(": ", 1)[1]) for line in lines[1:])
    assert actual == expected


@pytest.mark.parametrize(
    "matrix",
    [
        [],
        [[1, 0], [0]],
        [[1, "text"], [0, 1]],
        [[True]],
    ],
)
def test_pipeline_rejects_invalid_matrix(matrix):
    with pytest.raises(ValueError):
        run_pipeline(matrix)
