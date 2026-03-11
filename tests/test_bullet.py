import pytest

from rich_illuminations import Bullet
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "data, expected",
    [
        (210, "[black][on red]━━━━━[on orange1]━━━━━[on green]╸ │  [/]"),
        (250, "[black][on red]━━━━━[on orange1]━━━━━[on green]━━┥  [/]"),
        (260, "[black][on red]━━━━━[on orange1]━━━━━[on green]━━┿  [/]"),
        (300, "[black][on red]━━━━━[on orange1]━━━━━[on green]━━┿━━[/]"),
    ],
    ids=["below target", "on target", "over target", "on limit"],
)
def test_data(data: float, expected: str):
    chart = Bullet(
        data=data,
        target=250,
        width=15,
        limits=[0, 100, 200, 300],
        limit_colors=["red", "orange1", "green"],
    )
    assert_markup(chart, expected)
