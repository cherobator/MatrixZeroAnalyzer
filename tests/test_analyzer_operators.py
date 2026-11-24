from src.matrix_zero_analyzer import analyze_payload, count_zeros


def test_zero_at_intersection_of_diagonals():
    assert count_zeros([[0]]) == (0, 0, 0, 0)


def test_matrix_without_zero_elements():
    assert count_zeros([[1, 2], [3, 4]]) == (0, 0, 0, 0)


def test_analyze_payload_returns_each_diagonal_count():
    payload = {
        "matrix_size": 4,
        "matrix_data": [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
        ],
    }

    assert analyze_payload(payload) == {
        "dim": 4,
        "zeros_above_main": 5,
        "zeros_below_main": 1,
        "zeros_above_secondary": 4,
        "zeros_below_secondary": 2,
    }
