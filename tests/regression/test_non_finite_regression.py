import pytest

from src.binary_integration import run_file_pipeline
from src.integration import run_pipeline


@pytest.fixture(params=[
    pytest.param(float("nan"), id="nan"),
    pytest.param(float("inf"), id="positive-infinity"),
    pytest.param(float("-inf"), id="negative-infinity"),
])
def non_finite_value(request):
    return request.param


def test_direct_pipeline_rejects_non_finite_value(non_finite_value):
    with pytest.raises(ValueError, match="должны быть конечными"):
        run_pipeline([[non_finite_value]])


def test_binary_pipeline_preserves_existing_file(tmp_path, non_finite_value):
    path = tmp_path / "matrix.bin"
    original = b"previous contents"
    path.write_bytes(original)

    with pytest.raises(ValueError, match="должны быть конечными"):
        run_file_pipeline([[non_finite_value]], path)

    assert path.read_bytes() == original
