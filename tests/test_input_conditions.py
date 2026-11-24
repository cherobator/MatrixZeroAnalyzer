import pytest

from src.input_module import create_matrix_payload


def test_row_is_list_and_has_correct_length():
    assert create_matrix_payload([[7]])["matrix_data"] == [[7.0]]


@pytest.mark.parametrize(
    "row",
    [
        pytest.param([], id="list-wrong-length"),
        pytest.param((7,), id="tuple-correct-length"),
        pytest.param((), id="tuple-wrong-length"),
    ],
)
def test_rejects_invalid_row_combinations(row):
    with pytest.raises(ValueError, match="квадратной"):
        create_matrix_payload([row])
