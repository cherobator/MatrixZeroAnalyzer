"""Модуль формирования текстового отчёта по результатам анализа."""


def format_report(counts):
    """Форматирует кортеж из 4 счётчиков в итоговый текстовый отчёт."""
    above_main, below_main, above_sec, below_sec = counts
    lines = [
        "Результаты анализа:",
        f"Выше главной диагонали: {above_main}",
        f"Ниже главной диагонали: {below_main}",
        f"Выше побочной диагонали: {above_sec}",
        f"Ниже побочной диагонали: {below_sec}",
    ]
    return "\n".join(lines)


def format_mapped_report(mapped_dto):
    """Формирует отчёт из сопоставленных данных."""
    counts = (
        mapped_dto["main_diag_upper"],
        mapped_dto["main_diag_lower"],
        mapped_dto["sec_diag_upper"],
        mapped_dto["sec_diag_lower"],
    )
    n = mapped_dto["dimension"]
    header = f"Отчёт для матрицы {n}x{n}"
    return header + "\n" + format_report(counts)
