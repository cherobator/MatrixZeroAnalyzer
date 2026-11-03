"""Модуль ввода и первичной валидации квадратной матрицы."""


def create_matrix_payload(matrix, version="1.0"):
    """Формирует пакет входных данных с проверкой размерности n x n."""
    if not isinstance(matrix, list) or len(matrix) == 0:
        raise ValueError("Матрица должна быть непустым списком списков.")

    n = len(matrix)
    normalized = []
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError("Матрица должна быть квадратной (n x n).")
        normalized_row = []
        for item in row:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise ValueError("Элементы матрицы должны быть числами.")
            normalized_row.append(float(item))
        normalized.append(normalized_row)

    return {
        "protocol_version": version,
        "matrix_size": n,
        "matrix_data": normalized,
    }
