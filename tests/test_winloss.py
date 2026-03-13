import pytest

from graphical.mark import BAR_BLOCK_V, BAR_HEAVY_V, BAR_LIGHT_V, Mark
from rich.console import Console
from rich.measure import Measurement
from rich_illuminations import WinLoss
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "cells, width, expected",
    [
        (None, 9, "▄▄▄▄ ▀▀▀▀"),
        (BAR_BLOCK_V, 9, "▄▄▄▄ ▀▀▀▀"),
        (BAR_LIGHT_V, 9, "╷╷╷╷ ╵╵╵╵"),
        (BAR_HEAVY_V, 9, "╻╻╻╻ ╹╹╹╹"),
    ],
    ids=["Default", "BLOCK", "LIGHT", "HEAVY"],
)
def test_ascending(cells: Mark, width: int, expected: str):
    chart = WinLoss(
        data=[-(width // 2) + d for d in range(width)],
        marks=cells,
    )
    assert_markup(chart, expected)


@pytest.mark.parametrize(
    "cells, width, expected",
    [
        (None, 9, "▀▀▀▀ ▄▄▄▄"),
        (BAR_BLOCK_V, 9, "▀▀▀▀ ▄▄▄▄"),
        (BAR_LIGHT_V, 9, "╵╵╵╵ ╷╷╷╷"),
        (BAR_HEAVY_V, 9, "╹╹╹╹ ╻╻╻╻"),
    ],
    ids=["Default", "BLOCK", "LIGHT", "HEAVY"],
)
def test_descending(cells: Mark, width: int, expected: str):
    chart = WinLoss(
        data=[width // 2 - d for d in range(width)],
        marks=cells,
    )
    assert_markup(chart, expected)


def test_measurement():
    chart = WinLoss(
        data=[0, 1, 2],
        width=6,
    )
    console = Console()
    assert chart.__rich_measure__(console, console.options) == Measurement(5, 6)
