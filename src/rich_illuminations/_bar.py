from typing import Literal, Optional, Tuple, Union
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.measure import Measurement

from graphical.mark import BAR_BLOCK_H, BAR_HEAVY_H, BAR_LIGHT_H, Mark
from graphical.bar import Bar as BaseBar
from rich.segment import Segment
from rich.style import Style

Numeric = Union[int, float]
BarMark = Literal["block", "heavy", "light"]


class Bar:
    """Bar graph.

    Args:
        data (Numeric): The value.
        value_range: Lower and upper boundary.
        width (int): The width of the graph. Defaults to 100.
        marks (Union[BarMark, Mark]], optional): Marks used for the bar. Defaults to "block".
        color (Union[Color, str], optional): Color of the bar. Defaults to "default".
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
        show_label (bool, optional): Show value as label. Default to False.
    """

    def __init__(
        self,
        data: Numeric,
        value_range: Tuple[Numeric, Numeric],
        *,
        width: Optional[int] = None,
        marks: Optional[Union[BarMark, Mark]] = None,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        show_label: bool = False,
    ):
        self.data = data
        self.value_range = value_range
        self.width = width or 100
        self.marks = self.__marks(marks or "block")
        self.color = color
        self.bgcolor = bgcolor
        self.show_label = show_label

    def __marks(self, mark: Union[BarMark, Mark]) -> Mark:
        if mark == "block":
            return BAR_BLOCK_H
        if mark == "heavy":
            return BAR_HEAVY_H
        if mark == "light":
            return BAR_LIGHT_H
        return mark

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = min(self.width, options.max_width)
        tag_width = max(len(f"{d}") for d in self.value_range)
        bar_width = width
        if self.show_label:
            bar_width -= tag_width + 1
        yield from BaseBar(
            value=self.data,
            value_range=self.value_range,
            width=bar_width,
            marks=self.marks,
            color=self.color,
            bgcolor=self.bgcolor,
            orientation="horizontal",
        )
        if self.show_label:
            yield Segment(
                f" {self.data:>{tag_width}}",
                Style(color=self.color, bgcolor=self.bgcolor),
            )

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(5, self.width)


if __name__ == "__main__":  # pragma: no cover
    console = Console()
    for v in [-10, 150, 260, -280, 300]:
        console.print(
            Bar(
                data=v, width=150, value_range=(-150, 300), color="red", show_label=True
            )
        )
        console.print()
