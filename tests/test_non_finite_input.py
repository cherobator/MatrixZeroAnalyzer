import pytest

from src.input_module import create_matrix_payload


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
    ],
)
def test_rejects_non_finite_matrix_elements(value):
    with pytest.raises(ValueError):
        create_matrix_payload([[value]])
