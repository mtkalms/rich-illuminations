from typing import Sequence

from graphical.utils import Numeric
import pytest

from rich_illuminations import Horizon
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [-5 + d for d in range(11)],
            "[#4d9221] ▂▅▇[/][#7fbc41 on #4d9221]▂▄▆[/][#b8e186 on #7fbc41]▁▃▆█[/]",
        ),
        (
            [5 - d for d in range(11)],
            "[#b8e186 on #7fbc41]█▆▃▁[/][#7fbc41 on #4d9221]▆▄▂[/][#4d9221]▇▅▂ [/]",
        ),
    ],
    ids=["ascending", "descending"],
)
def test_data(data: Sequence[Numeric], expected: str):
    chart = Horizon(
        data=data, value_range=(-5, 5), colors=["#4d9221", "#7fbc41", "#b8e186"]
    )
    assert_markup(chart, expected)
