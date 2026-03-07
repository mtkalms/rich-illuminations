from typing import Optional, Sequence, Union

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.utils import buckets, SummaryFunction, Numeric
from graphical.mark import Mark, BAR_BLOCK_V


class WinLoss:
    def __init__(
        self,
        values: Sequence[Numeric],
        width: Optional[int] = None,
        marks: Mark = BAR_BLOCK_V,
        color: Optional[Union[Color, str]] = None,
        negcolor: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        summary_function: SummaryFunction = sum,
    ):
        self.values = values
        self.width = width or len(values)
        self.marks = marks
        self.color = color
        self.negcolor = negcolor
        self.bgcolor = bgcolor
        self.summary_function = summary_function

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        pos_style = Style(color=self.color, bgcolor=self.bgcolor)
        neg_style = Style(color=self.negcolor, bgcolor=self.bgcolor)
        for value in buckets(self.values, self.width, self.summary_function):
            if value > 0:
                yield Segment(self.marks.get(-0.5), style=pos_style)
            elif value < 0:
                yield Segment(self.marks.get(0.5), style=neg_style)
            else:
                yield Segment(" ", style=pos_style)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)
