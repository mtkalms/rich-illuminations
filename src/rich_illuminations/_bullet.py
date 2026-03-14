from typing import Optional, Sequence, Union
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style

from graphical.mark import BAR_HEAVY_H, Mark


Numeric = Union[int, float]


class Bullet:
    """Bullet graph.

    Args:
        data (Numeric): The value.
        target (Numeric): The target value.
        width (int): The width of the graph.
        limits (Sequence[Numeric]): Boundaries of the qualitative ranges.
        color (Optional[Union[Color, str]], optional): Color of bar and mark. Defaults to "black".
        limit_colors (Optional[Sequence[Union[Color, str]]], optional): Colors used for the quality ranges. Defaults to ["red", "orange1", "green"].
    """

    def __init__(
        self,
        data: Numeric,
        target: Numeric,
        width: int,
        limits: Sequence[Numeric],
        *,
        color: Optional[Union[Color, str]] = None,
        limit_colors: Optional[Sequence[Union[Color, str]]] = None,
    ):
        self.data = data
        self.target = target
        self.limits = limits
        self.width = width
        self.color = color or "black"
        self.limit_colors = limit_colors or ["red", "orange1", "green"]

    def _in_cell_space(self, value: Numeric, width: Numeric):
        step = (self.limits[-1] - self.limits[0]) / width
        return (value - self.limits[0]) / step

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = min(self.width, options.max_width)
        marks_bar = BAR_HEAVY_H
        marks_target = Mark("│┥┿", "│┝┿")
        limits = [self._in_cell_space(d, width) for d in self.limits]
        target = self._in_cell_space(self.target, width)
        value = self._in_cell_space(self.data, width)
        color = self.color
        segments = []
        for cell in range(width):
            if cell < target <= (cell + 1):
                marks = marks_target
            else:
                marks = marks_bar
            if value >= (cell + 1):
                cell_value = 1.0
            elif cell > value:
                cell_value = 0.0
            else:
                if value == target:
                    cell_value = 0.5
                else:
                    cell_value = value - cell
            bgcolor = None
            for idx, limit in enumerate(limits):
                if int(limit) >= (cell + 1):
                    bgcolor = self.limit_colors[(idx - 1) % len(self.limit_colors)]
                    break
            segments.append(
                Segment(marks.get(cell_value), Style(color=color, bgcolor=bgcolor))
            )
        yield from Segment.simplify(segments)

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(5, self.width)


if __name__ == "__main__":  # pragma: no cover
    console = Console()
    for v in [210, 250, 260, 280, 300]:
        console.print(
            Bullet(
                data=v,
                target=250,
                width=15,
                limits=[0, 100, 200, 300],
                limit_colors=["red", "orange1", "green"],
            )
        )
        console.print(v)
        console.print()
