import pytest

from rich_illuminations import Sparkline
from graphical.mark import BAR_BLOCK_V, BAR_SHADE, Mark, Tuple

from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "cells, width, expected",
    [
        (BAR_BLOCK_V, 9, "  ▁▂▃▄▅▆▇██"),
        (BAR_SHADE, 5, "  ░▒▓██"),
    ],
    ids=["AREA", "SHADE"],
)
def test_ascending(cells: Mark, width: int, expected: str):
    chart = Sparkline(
        values=[-1 + d for d in range(width + 2)],
        value_range=(0, width - 1),
        marks=cells,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "cells, width, expected",
    [
        (BAR_BLOCK_V, 9, "███▇▆▅▄▃▂▁ "),
        (BAR_SHADE, 5, "███▓▒░ "),
    ],
    ids=["AREA", "SHADE"],
)
def test_descending(cells: Mark, width: int, expected: str):
    chart = Sparkline(
        values=[width + 1 - d for d in range(width + 2)],
        value_range=(0, width - 1),
        marks=cells,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "value, value_range, expected",
    [
        (12, (0, 10), "█"),
        (-2, (0, 10), " "),
    ],
    ids=["over", "under"],
)
def test_out_of_bounds(value: float, value_range: Tuple[float, float], expected: str):
    chart = Sparkline(
        values=[value],
        value_range=value_range,
        marks=BAR_BLOCK_V,
    )
    assert_markup(chart, expected)
