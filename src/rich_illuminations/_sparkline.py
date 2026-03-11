from typing import Optional, Sequence, Tuple, Union

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.utils import buckets, SummaryFunction, normalize, Numeric
from graphical.mark import Mark, BAR_BLOCK_V


class Sparkline:
    """Sparkline.

    Args:
        data: Sequence of data to render.
        value_range: Lower and upper boundary. Defaults to the range of data.
        width: The width of the graph. Defaults to length of data.
        marks: Marks used for the horizon bars. Defaults to BAR_BLOCK_V.
        color: Color for the sparkline bars. Defaults to "default".
        bgcolor: Background color. Defaults to "default".
        summary_function: Function to summarize the values in a cell. Defaults to max.
    """

    def __init__(
        self,
        data: Sequence[Numeric],
        *,
        value_range: Optional[Tuple[Numeric, Numeric]] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        summary_function: Optional[SummaryFunction] = None,
    ):
        self.data = data
        self.value_range = value_range or (min(self.data), max(self.data))
        self.width = width or len(data)
        self.marks = marks or BAR_BLOCK_V
        self.color = color
        self.bgcolor = bgcolor
        self.summary_function = summary_function or max

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = Style(color=self.color, bgcolor=self.bgcolor)
        segments = []
        for cell_value in buckets(self.data, self.width, self.summary_function):
            normalized = normalize(cell_value, self.value_range)
            cell_char = self.marks.get(normalized)
            segments.append(Segment(cell_char, style=style))
        yield from Segment.simplify(segments)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)
