"""Модуль подсчёта нулевых элементов относительно диагоналей матрицы."""


def count_zeros(matrix):
    """Считает нули: выше/ниже главной и выше/ниже побочной диагоналей."""
    n = len(matrix)
    above_main = 0
    below_main = 0
    above_sec = 0
    below_sec = 0

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                if j > i:
                    above_main += 1
                elif i > j:
                    below_main += 1

                if i + j < n - 1:
                    above_sec += 1
                elif i + j > n - 1:
                    below_sec += 1

    return above_main, below_main, above_sec, below_sec


def analyze_payload(payload):
    """Принимает структуру данных ввода и возвращает словарь результатов."""
    matrix = payload["matrix_data"]
    am, bm, asec, bsec = count_zeros(matrix)
    return {
        "dim": payload["matrix_size"],
        "zeros_above_main": am,
        "zeros_below_main": bm,
        "zeros_above_secondary": asec,
        "zeros_below_secondary": bsec,
    }
