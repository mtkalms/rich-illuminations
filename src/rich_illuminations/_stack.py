from typing import Literal, Optional, Sequence, Tuple, Union
from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.measure import Measurement

from graphical.mark import BAR_BLOCK_H, BAR_HEAVY_H, BAR_LIGHT_H, Mark
from graphical.bar import StackedBar as StackedBar

Numeric = Union[int, float]
BarMark = Literal["block", "heavy", "light"]

class Stack:
    """Stacked bar graph.

    Args:
        data (Sequence[Numeric]): The values in order of stacking.
        value_range: Lower and upper boundary. Defaults to range of data.
        width (int): The width of the graph. Defaults to 100.
        marks (Union[BarMark, Mark]], optional): Marks used for the bars. Defaults to "block".
        colors (Sequence[Union[Color, str]], optional): Colors of the bars. 
        bgcolor (Union[Color, str], optional): Background color. Defaults to "default".
    """

    def __init__(
        self,
        data: Sequence[Numeric],
        *,
        value_range: Optional[Tuple[Numeric, Numeric]] = None,
        width: Optional[int] = None,
        marks: Optional[Union[BarMark, Mark]] = None,
        colors: Optional[Sequence[Union[Color, str]]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
    ):
        self.data = data
        self.value_range = value_range or (min(sum(data), 0), max(0, sum(data)))
        self.width = width or 100
        self.marks = self.__marks(marks or "block")
        self.colors = colors or ["blue", "orange1", "green", "red", "purple"]
        self.bgcolor = bgcolor

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
        yield from StackedBar(
            values=self.data,
            value_range=self.value_range,
            width=self.width,
            marks=self.marks,
            colors=self.colors,
            bgcolor=self.bgcolor,
            orientation="horizontal"
        )
       
    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(self.width, self.width)


if __name__ == "__main__":  # pragma: no cover
    console = Console()
    for v in [[10, 2, 3, 4, 12], [5, 7, 4, 3, 2]]:
        console.print(
            Stack(
                data=v,
                width=150,
                value_range=(0, 50)
            )
        )
        console.print(f" {v}")
        console.print()
