from typing import Optional, Sequence, Tuple, Union

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical._buckets import buckets, SummaryFunction
from graphical._normalize import normalize
from graphical.mark import Mark, BAR_BLOCK_V

Numeric = Union[int, float]


class Horizon:
    def __init__(
        self,
        values: Sequence[Numeric],
        value_range: Tuple[Numeric, Numeric],
        colors: Sequence[Optional[Union[Color, str]]],
        width: Optional[int] = None,
        marks: Mark = BAR_BLOCK_V,
        bgcolor: Optional[Union[Color, str]] = None,
        summary_function: SummaryFunction = max,
    ):
        self.values = values
        self.value_range = value_range
        self.colors = colors
        self.width = width or len(values)
        self.marks = marks
        self.bgcolor = bgcolor
        self.summary_function = summary_function

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        levels = len(self.colors)
        colors = zip(self.colors, [self.bgcolor, *self.colors[:-1]])
        styles = [Style(color=color, bgcolor=bgcolor) for color, bgcolor in colors]
        for cell_value in buckets(self.values, self.width, self.summary_function):
            normalized = normalize(cell_value, self.value_range) * levels
            value, level = math.modf(normalized)
            if normalized > 0 and value == 0.0:
                level = levels - 1
                value = 1.0
            cell_char = self.marks.get(value)
            cell_style = styles[int(level)]
            yield Segment(cell_char, style=cell_style)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, 1)


if __name__ == "__main__":
    import math

    console = Console()
    console.print(
        Horizon(
            values=[(1 + math.sin(math.pi * d / 12)) * 7.5 for d in range(100)],
            value_range=(0, 15),
            colors=["#276419", "#4d9221", "#7fbc41", "#b8e186", "#e6f5d0"],
        )
    )
    console.print()
