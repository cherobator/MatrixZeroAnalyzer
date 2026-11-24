from src.report import format_mapped_report, format_report


def test_formats_all_four_counts_in_order():
    assert format_report((5, 1, 4, 2)).splitlines() == [
        "Результаты анализа:",
        "Выше главной диагонали: 5",
        "Ниже главной диагонали: 1",
        "Выше побочной диагонали: 4",
        "Ниже побочной диагонали: 2",
    ]


def test_mapped_report_adds_matrix_dimensions():
    mapped = {
        "dimension": 4,
        "main_diag_upper": 5,
        "main_diag_lower": 1,
        "sec_diag_upper": 4,
        "sec_diag_lower": 2,
    }

    assert format_mapped_report(mapped) == (
        "Отчёт для матрицы 4x4\n" + format_report((5, 1, 4, 2))
    )
