"""Интеграция модулей ввода, анализа и вывода."""

from src.input_module import create_matrix_payload
from src.matrix_zero_analyzer import analyze_payload
from src.report import format_report


def run_pipeline(matrix):
    """Передаёт матрицу через все три модуля."""
    payload = create_matrix_payload(matrix)
    result = analyze_payload(payload)
    counts = (
        result["zeros_above_main"],
        result["zeros_below_main"],
        result["zeros_above_secondary"],
        result["zeros_below_secondary"],
    )
    return format_report(counts)


def main():
    """Запускает демонстрационный пример."""
    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    try:
        print(run_pipeline(matrix))
    except (ValueError, TypeError, KeyError) as error:
        print(f"Ошибка интеграции: {error}")


if __name__ == "__main__":
    main()
