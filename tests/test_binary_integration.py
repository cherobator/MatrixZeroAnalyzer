"""Проверки бинарного обмена и полной цепочки модулей."""

import struct

import pytest

from src.binary_integration import run_file_pipeline
from src.binary_transport import read_payload, write_payload
from src.data_mapping import map_analysis_result
from src.input_module import create_matrix_payload


def test_binary_roundtrip(tmp_path):
    original = create_matrix_payload([[1.5, 0], [-2.25, 1]])
    path = tmp_path / "matrix.bin"

    write_payload(path, original)

    assert path.stat().st_size == 41
    assert read_payload(path) == original


def test_full_file_pipeline(tmp_path):
    matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    path = tmp_path / "matrix.bin"

    report = run_file_pipeline(matrix, path)

    assert path.stat().st_size == 81
    assert report == (
        "Отчёт для матрицы 3x3\n"
        "Результаты анализа:\n"
        "Выше главной диагонали: 3\n"
        "Ниже главной диагонали: 3\n"
        "Выше побочной диагонали: 2\n"
        "Ниже побочной диагонали: 2"
    )


def test_mapping_preserves_field_meaning():
    result = {
        "dim": 4,
        "zeros_above_main": 1,
        "zeros_below_main": 2,
        "zeros_above_secondary": 3,
        "zeros_below_secondary": 4,
    }

    assert map_analysis_result(result) == {
        "dimension": 4,
        "main_diag_upper": 1,
        "main_diag_lower": 2,
        "sec_diag_upper": 3,
        "sec_diag_lower": 4,
    }


@pytest.mark.parametrize(
    "content",
    [
        b"",
        b"MZA",
        struct.pack("<4sBI", b"BAD!", 1, 1),
        struct.pack("<4sBI", b"MZA1", 2, 1),
        struct.pack("<4sBI", b"MZA1", 1, 0),
        struct.pack("<4sBI", b"MZA1", 1, 1001),
        struct.pack("<4sBI", b"MZA1", 1, 1) + b"\x00" * 7,
        struct.pack("<4sBI", b"MZA1", 1, 1) + b"\x00" * 9,
    ],
)
def test_rejects_corrupted_file(tmp_path, content):
    path = tmp_path / "broken.bin"
    path.write_bytes(content)

    with pytest.raises(ValueError):
        read_payload(path)


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_payload(tmp_path / "missing.bin")


@pytest.mark.parametrize(
    "field, value",
    [
        ("protocol_version", "2.0"),
        ("matrix_size", 5),
    ],
)
def test_rejects_inconsistent_payload(tmp_path, field, value):
    payload = create_matrix_payload([[1]])
    payload[field] = value

    with pytest.raises(ValueError):
        write_payload(tmp_path / "matrix.bin", payload)
