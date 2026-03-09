from typing import Optional, Sequence, Tuple, Union

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.utils import buckets, SummaryFunction, Numeric
from graphical.mark import Mark, BAR_BLOCK_V


class WinLoss:
    """Special sparkline showing values as either wins (positive) or losses (negative).

    Args:
        data: Sequence of data to render.
        width: The width of the chart. Defaults to length of data.
        marks: Marks used for the winloss bars. Defaults to None.
        colors: Pair of colors used for negative and positive values.
        bgcolor: Background color. Defaults to "default".
        summary_function: Function to summarize the values in a cell. Defaults to sum.
    """

    def __init__(
        self,
        data: Sequence[Numeric],
        *,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        colors: Optional[Tuple[Union[Color, str], Union[Color, str]]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        summary_function: Optional[SummaryFunction] = None,
    ):
        self.data = data
        self.width = width or len(data)
        self.marks = marks or BAR_BLOCK_V
        self.colors = colors or (None, None)
        self.bgcolor = bgcolor
        self.summary_function = summary_function or sum

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        pos_style = Style(color=self.colors[1], bgcolor=self.bgcolor)
        neg_style = Style(color=self.colors[0], bgcolor=self.bgcolor)
        segments = []
        for value in buckets(self.data, self.width, self.summary_function):
            if value > 0:
                segments.append(Segment(self.marks.get(-0.5), style=pos_style))
            elif value < 0:
                segments.append(Segment(self.marks.get(0.5), style=neg_style))
            else:
                segments.append(Segment(" ", style=pos_style))
        yield from Segment.simplify(segments)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)
