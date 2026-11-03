"""Проверки защищённого запуска и исключительных ситуаций."""

import pytest

from src import safe_integration as safe


def test_safe_pipeline_success(tmp_path):
    report = safe.run_safe_pipeline(
        [[1, 0], [0, 1]],
        tmp_path / "matrix.bin",
    )
    assert report == (
        "Отчёт для матрицы 2x2\n"
        "Результаты анализа:\n"
        "Выше главной диагонали: 1\n"
        "Ниже главной диагонали: 1\n"
        "Выше побочной диагонали: 0\n"
        "Ниже побочной диагонали: 0"
    )


@pytest.mark.parametrize("matrix", [[], [[1, 0], [0]]])
def test_safe_pipeline_invalid_data(tmp_path, matrix):
    with pytest.raises(ValueError, match="Ошибка обработки"):
        safe.run_safe_pipeline(matrix, tmp_path / "matrix.bin")


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_invalid_timeout(tmp_path, timeout):
    with pytest.raises(ValueError, match="Таймаут"):
        safe.run_safe_pipeline([[1]], tmp_path / "matrix.bin", timeout)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_input(tmp_path, value):
    with pytest.raises(ValueError):
        safe.run_safe_pipeline([[value]], tmp_path / "matrix.bin")


def test_module_unavailable(tmp_path, monkeypatch):
    worker = safe.WORKER.replace(
        "from src.binary_integration import run_file_pipeline",
        "from src.nonexistent_module import run_file_pipeline",
    )
    monkeypatch.setattr(safe, "WORKER", worker)

    with pytest.raises(RuntimeError, match="Модуль недоступен"):
        safe.run_safe_pipeline([[1]], tmp_path / "matrix.bin")


def test_worker_timeout(tmp_path, monkeypatch):
    monkeypatch.setattr(
        safe,
        "WORKER",
        "import time; time.sleep(10)",
    )

    with pytest.raises(TimeoutError, match="Превышено время"):
        safe.run_safe_pipeline(
            [[1]],
            tmp_path / "matrix.bin",
            timeout=0.1,
        )


def test_invalid_worker_response(tmp_path, monkeypatch):
    monkeypatch.setattr(safe, "WORKER", "print('invalid json')")

    with pytest.raises(RuntimeError, match="некорректный ответ"):
        safe.run_safe_pipeline([[1]], tmp_path / "matrix.bin")


def test_worker_start_failure(tmp_path, monkeypatch):
    def fail_to_start(*args, **kwargs):
        raise OSError("Запуск процесса недоступен")

    monkeypatch.setattr(safe.subprocess, "run", fail_to_start)

    with pytest.raises(RuntimeError, match="Не удалось запустить"):
        safe.run_safe_pipeline([[1]], tmp_path / "matrix.bin")
