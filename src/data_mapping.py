"""Сопоставление полей анализа и текстового отчёта."""


def map_analysis_result(result):
    """Преобразует результат анализа в структуру модуля вывода."""
    return {
        "dimension": result["dim"],
        "main_diag_upper": result["zeros_above_main"],
        "main_diag_lower": result["zeros_below_main"],
        "sec_diag_upper": result["zeros_above_secondary"],
        "sec_diag_lower": result["zeros_below_secondary"],
    }
