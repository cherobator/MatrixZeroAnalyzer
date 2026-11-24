import pytest

from src import binary_transport


def test_binary_roundtrip_preserves_values(tmp_path):
    path = tmp_path / "matrix.bin"
    payload = {
        "protocol_version": "1.0",
        "matrix_size": 2,
        "matrix_data": [[-0.25, 1.5], [0.0, -8.0]],
    }

    binary_transport.write_payload(path, payload)

    assert path.read_bytes()[:4] == b"MZA1"
    assert binary_transport.read_payload(path) == payload


def test_write_rejects_matrix_above_size_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(binary_transport, "MAX_SIZE", 1)
    path = tmp_path / "matrix.bin"
    payload = {
        "protocol_version": "1.0",
        "matrix_size": 2,
        "matrix_data": [[0, 1], [2, 3]],
    }

    with pytest.raises(ValueError, match="Превышен допустимый размер"):
        binary_transport.write_payload(path, payload)

    assert not path.exists()
