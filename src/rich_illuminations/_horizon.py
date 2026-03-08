from typing import Optional, Sequence, Tuple, Union

from rich.color import Color
from rich.console import ConsoleOptions, RenderResult, Console
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from graphical.utils import buckets, normalize, SummaryFunction, Numeric
from graphical.mark import Mark, BAR_BLOCK_V


class Horizon:
    def __init__(
        self,
        values: Sequence[Numeric],
        *,
        value_range: Optional[Tuple[Numeric, Numeric]] = None,
        colors: Optional[Sequence[Optional[Union[Color, str]]]] = None,
        width: Optional[int] = None,
        marks: Optional[Mark] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        summary_function: Optional[SummaryFunction] = None,
    ):
        self.values = values
        self.value_range = value_range or (min(self.values), max(self.values))
        self.colors = colors or ["#276419", "#4d9221", "#7fbc41", "#b8e186", "#e6f5d0"]
        self.width = width or len(values)
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
        for cell_value in buckets(self.values, self.width, self.summary_function):
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
        return Measurement(self.width, 1)


if __name__ == "__main__":  # pragma: no cover
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
