from typing import List, Optional

from graphical.utils import SummaryFunction
import pytest
from rich.console import Console
from rich.measure import Measurement

from rich_illuminations import Sparkline
from graphical.mark import BAR_BLOCK_V, BAR_SHADE, Mark, Tuple

from tests.utilities.asserts import assert_markup
from statistics import mean


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
        (0, (0, 10), " "),
        (10, (0, 10), "█"),
        (12, (0, 10), "█"),
        (-2, (0, 10), " "),
    ],
    ids=["lower", "upper", "over", "under"],
)
def test_bounds(value: float, value_range: Tuple[float, float], expected: str):
    chart = Sparkline(
        values=[value],
        value_range=value_range,
        marks=BAR_BLOCK_V,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "values, value_range, width, expected",
    [
        ([0, 2, 4, 6, 8], (0, 8), None, " ▂▄▆█"),
        ([0, 8, 1, 7], (0, 8), 2, "█▇"),
        ([0, 2, 4, 6, 8], (0, 8), 10, "  ▂▂▄▄▆▆██"),
    ],
    ids=["exact", "sample down", "sample up"],
)
def test_buckets(
    values: List[float],
    value_range: Tuple[float, float],
    width: Optional[int],
    expected: str,
):
    chart = Sparkline(
        values=values,
        value_range=value_range,
        width=width,
        marks=BAR_BLOCK_V,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "summary_function, expected",
    [
        (max, "█▇"),
        (min, " ▁"),
        (mean, "▄▄"),
    ],
    ids=["max", "min", "mean"],
)
def test_custom_summary_function(summary_function: SummaryFunction, expected: str):
    chart = Sparkline(
        values=[0, 8, 1, 7],
        value_range=(0, 8),
        width=2,
        marks=BAR_BLOCK_V,
        summary_function=summary_function,
    )
    assert_markup(chart, expected)


def test_value_mapping():
    chart = Sparkline(
        values=[2.75],
        value_range=(0, 8),
        marks=BAR_BLOCK_V,
    )
    assert_markup(chart, "▃")


def test_styling():
    chart = Sparkline(
        values=[8],
        value_range=(0, 8),
        marks=BAR_BLOCK_V,
        color="red",
        bgcolor="black",
    )
    assert_markup(chart, "[red on black]█[/]")


def test_measurement():
    chart = Sparkline(
        values=[0, 1, 2],
        value_range=(0, 2),
        width=6,
        marks=BAR_BLOCK_V,
    )
    console = Console()
    assert chart.__rich_measure__(console, console.options) == Measurement(6, 1)


def test_empty_values():
    chart = Sparkline(
        values=[],
        value_range=(0, 1),
        width=3,
        marks=BAR_BLOCK_V,
    )
    with pytest.raises(ValueError):
        assert_markup(chart, "   ")
