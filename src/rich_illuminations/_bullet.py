from typing import Optional, Sequence, Union
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.measure import Measurement
from rich.style import Style

from graphical.mark import BAR_HEAVY_H, Mark


Numeric = Union[int, float]


class Bullet:
    def __init__(
        self,
        value: Numeric,
        target: Numeric,
        width: int,
        limits: Sequence[Numeric],
        *,
        color: Optional[Union[Color, str]] = None,
        limit_colors: Optional[Sequence[Union[Color, str]]] = None,
    ):
        self.value = value
        self.target = target
        self.limits = limits
        self.width = width
        self.color = color or "black"
        self.limit_colors = limit_colors or ["red", "orange1", "green"]

    def _in_cell_space(self, value: Numeric):
        step = (self.limits[-1] - self.limits[0]) / self.width
        return (value - self.limits[0]) / step

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        marks_bar = BAR_HEAVY_H
        marks_target = Mark("│┥┿", "│┝┿")
        limits = [self._in_cell_space(d) for d in self.limits]
        target = self._in_cell_space(self.target)
        value = self._in_cell_space(self.value)
        color = self.color
        segments = []
        for cell in range(self.width):
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
        return Measurement(self.width, 1)


if __name__ == "__main__":  # pragma: no cover
    console = Console()
    for v in [210, 250, 260, 280, 300]:
        console.print(
            Bullet(
                value=v,
                target=250,
                width=15,
                limits=[0, 100, 200, 300],
                limit_colors=["red", "orange1", "green"],
            )
        )
        console.print(v)
        console.print()
