import pytest

from src.data_mapping import map_analysis_result


def test_maps_each_counter_to_the_corresponding_field():
    result = {
        "dim": 4,
        "zeros_above_main": 5,
        "zeros_below_main": 1,
        "zeros_above_secondary": 4,
        "zeros_below_secondary": 2,
    }

    assert map_analysis_result(result) == {
        "dimension": 4,
        "main_diag_upper": 5,
        "main_diag_lower": 1,
        "sec_diag_upper": 4,
        "sec_diag_lower": 2,
    }


def test_reports_missing_dimension():
    with pytest.raises(KeyError, match="dim"):
        map_analysis_result({})
