import pytest

from src.input_module import create_matrix_payload


def test_create_matrix_payload_normalizes_numbers():
    result = create_matrix_payload([[1, 0], [0, -2.5]])

    assert result == {
        "protocol_version": "1.0",
        "matrix_size": 2,
        "matrix_data": [[1.0, 0.0], [0.0, -2.5]],
    }
    assert all(
        isinstance(value, float)
        for row in result["matrix_data"]
        for value in row
    )


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        pytest.param([], "непустым списком", id="empty"),
        pytest.param([[1, 0], [0]], "квадратной", id="not-square"),
        pytest.param([["0"]], "должны быть числами", id="string"),
        pytest.param([[True]], "должны быть числами", id="bool"),
    ],
)
def test_create_matrix_payload_rejects_invalid_input(matrix, message):
    with pytest.raises(ValueError, match=message):
        create_matrix_payload(matrix)
