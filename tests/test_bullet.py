import pytest

from rich_illuminations._bullet import Bullet
from tests.utilities.asserts import assert_markup


@pytest.mark.parametrize(
    "value, expected",
    [
        (210, "[black][on red]━━━━━[on orange1]━━━━━[on green]╸ │  [/]"),
        (250, "[black][on red]━━━━━[on orange1]━━━━━[on green]━━┥  [/]"),
        (260, "[black][on red]━━━━━[on orange1]━━━━━[on green]━━┿  [/]"),
        (300, "[black][on red]━━━━━[on orange1]━━━━━[on green]━━┿━━[/]"),
    ],
    ids=["below target", "on target", "over target", "on limit"],
)
def test_values(value: float, expected: str):
    chart = Bullet(
        value=value,
        target=250,
        width=15,
        limits=[0, 100, 200, 300],
        limit_colors=["red", "orange1", "green"],
    )
    assert_markup(chart, expected, preview=True)
