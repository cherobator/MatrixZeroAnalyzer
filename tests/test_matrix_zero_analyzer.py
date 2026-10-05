from src.matrix_zero_analyzer import count_zeros
from src.report import format_report


def test_normal_matrix():
    matrix = [[0, 0, 1], [2, 0, 0], [0, 3, 0]]
    assert count_zeros(matrix) == (2, 1, 2, 2)


def test_matrix_without_zeros():
    matrix = [[1, 2], [3, 4]]
    assert count_zeros(matrix) == (0, 0, 0, 0)


def test_all_zeros():
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert count_zeros(matrix) == (3, 3, 3, 3)


def test_one_by_one():
    assert count_zeros([[0]]) == (0, 0, 0, 0)


def test_report_format():
    text = format_report((1, 2, 3, 4))
    assert "Выше главной диагонали: 1" in text
    assert "Ниже побочной диагонали: 4" in text