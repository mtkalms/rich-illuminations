from typing import Optional, Sequence, Tuple, Union
import math

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.utils import buckets, normalize, SummaryFunction, Numeric
from graphical.mark import Mark, BAR_BLOCK_V


class Horizon:
    """Horizon graph.

    Args:
        data: Sequence of data to render.
        value_range: Lower and upper boundary. Defaults to the range of data.
        colors: Colors used for the horizon layers. Defaults to shades of green.
        width: The width of the graph. Defaults to length of data.
        marks: Marks used for the horizon bars. Defaults to BAR_BLOCK_V.
        bgcolor: Background color. Defaults to "default".
        summary_function: Function to summarize the values in a cell. Defaults to max.
    """

    def __init__(
        self,
        data: Sequence[Numeric],
        *,
        value_range: Optional[Tuple[Numeric, Numeric]] = None,
        colors: Optional[Sequence[Optional[Union[Color, str]]]] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        summary_function: Optional[SummaryFunction] = None,
    ):
        self.data = data
        self.value_range = value_range or (min(self.data), max(self.data))
        self.colors = colors or ["#276419", "#4d9221", "#7fbc41", "#b8e186", "#e6f5d0"]
        self.width = width or len(data)
        self.marks = marks or BAR_BLOCK_V
        self.bgcolor = bgcolor
        self.summary_function = summary_function or max

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        levels = len(self.colors)
        colors = zip(self.colors, [self.bgcolor, *self.colors[:-1]])
        styles = [Style(color=color, bgcolor=bgcolor) for color, bgcolor in colors]
        segments = []
        for cell_value in buckets(self.data, self.width, self.summary_function):
            normalized = normalize(cell_value, self.value_range) * levels
            value, level = math.modf(normalized)
            if normalized > 0 and value == 0.0:
                level = levels - 1
                value = 1.0
            cell_char = self.marks.get(value)
            cell_style = styles[int(level)]
            segments.append(Segment(cell_char, style=cell_style))
        yield from Segment.simplify(segments)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


if __name__ == "__main__":  # pragma: no cover
    console = Console()
    console.print(
        Horizon(
            data=[(1 + math.sin(math.pi * d / 12)) * 7.5 for d in range(100)],
            value_range=(0, 15),
            colors=["#276419", "#4d9221", "#7fbc41", "#b8e186", "#e6f5d0"],
        )
    )
    console.print()
