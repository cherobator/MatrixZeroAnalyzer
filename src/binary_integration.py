"""Интеграция модулей с обменом через бинарный файл."""

from pathlib import Path
from tempfile import TemporaryDirectory

from src.binary_transport import read_payload, write_payload
from src.data_mapping import map_analysis_result
from src.input_module import create_matrix_payload
from src.matrix_zero_analyzer import analyze_payload
from src.report import format_mapped_report


def run_file_pipeline(matrix, path):
    """Передаёт матрицу через файл и формирует отчёт."""
    payload = create_matrix_payload(matrix)
    write_payload(path, payload)
    restored = read_payload(path)
    result = analyze_payload(restored)
    mapped = map_analysis_result(result)
    return format_mapped_report(mapped)


def main():
    """Демонстрирует полный цикл бинарного обмена."""
    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    try:
        with TemporaryDirectory() as folder:
            path = Path(folder) / "matrix.bin"
            report = run_file_pipeline(matrix, path)
            print(f"Размер бинарного файла: {path.stat().st_size} байт")
            print(report)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Ошибка интеграции: {error}")


if __name__ == "__main__":
    main()
