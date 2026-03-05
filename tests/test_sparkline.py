import pytest

from rich_illuminations.sparkline import Sparkline
from graphical.mark import BAR_BLOCK_V, BAR_SHADE, Mark

from .util import render


class Test_Sparkline:
    @pytest.mark.parametrize(
        "cells, width, expected",
        [
            (BAR_BLOCK_V, 9, "  ▁▂▃▄▅▆▇██"),
            (BAR_SHADE, 5, "  ░▒▓██"),
        ],
        ids=["AREA", "SHADE"],
    )
    def test_ascending(self, cells: Mark, width: int, expected: str):
        chart = Sparkline(
            values=[-1 + d for d in range(width + 2)],
            value_range=(0, width - 1),
            marks=cells,
        )
        assert render(chart) == expected

    @pytest.mark.parametrize(
        "cells, width, expected",
        [
            (BAR_BLOCK_V, 9, "███▇▆▅▄▃▂▁ "),
            (BAR_SHADE, 5, "███▓▒░ "),
        ],
        ids=["AREA", "SHADE"],
    )
    def test_descending(self, cells: Mark, width: int, expected: str):
        chart = Sparkline(
            values=[width + 1 - d for d in range(width + 2)],
            value_range=(0, width - 1),
            marks=cells,
        )
        assert render(chart) == expected
