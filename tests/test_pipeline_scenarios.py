import runpy

import pytest

from src import binary_integration, integration, safe_integration


def test_three_pipelines_agree_on_diagonal_counts(tmp_path):
    matrix = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
    ]
    expected_lines = [
        "Результаты анализа:",
        "Выше главной диагонали: 5",
        "Ниже главной диагонали: 1",
        "Выше побочной диагонали: 4",
        "Ниже побочной диагонали: 2",
    ]
    expected_file_lines = ["Отчёт для матрицы 4x4", *expected_lines]
    direct = integration.run_pipeline(matrix)
    binary = binary_integration.run_file_pipeline(
        matrix, tmp_path / "binary.bin"
    )
    safe = safe_integration.run_safe_pipeline(
        matrix, tmp_path / "safe.bin", timeout=10
    )

    assert direct.splitlines() == expected_lines
    assert binary.splitlines() == expected_file_lines
    assert safe.splitlines() == expected_file_lines


def test_invalid_matrix_is_rejected_before_file_creation(tmp_path):
    path = tmp_path / "invalid.bin"

    with pytest.raises(ValueError, match="квадратной"):
        binary_integration.run_file_pipeline([[1, 0], [0]], path)

    assert not path.exists()


@pytest.mark.parametrize(
    ("module", "expected_text"),
    [
        (integration, "Выше главной диагонали: 3"),
        (binary_integration, "Размер бинарного файла: 81 байт"),
    ],
)
def test_demo_entry_point_prints_result(module, expected_text, capsys):
    runpy.run_path(module.__file__, run_name="__main__")

    assert expected_text in capsys.readouterr().out


@pytest.mark.parametrize(
    ("module", "pipeline_name"),
    [
        (integration, "run_pipeline"),
        (binary_integration, "run_file_pipeline"),
    ],
)
def test_demo_prints_integration_error(
    module, pipeline_name, monkeypatch, capsys
):
    def fail_pipeline(*_args):
        raise ValueError("проверочная ошибка")

    monkeypatch.setattr(module, pipeline_name, fail_pipeline)
    module.main()

    assert capsys.readouterr().out.strip() == (
        "Ошибка интеграции: проверочная ошибка"
    )
