def main():  # pragma: no cover
    import math
    from graphical.mark import BAR_HEAVY_V
    from rich.console import Console
    from rich.table import Table
    from rich.style import Style
    from rich_illuminations import Bar, Bullet, Horizon, Sparkline, Stack, WinLoss

    console = Console()
    table = Table(show_header=False, padding=(1, 1), border_style=Style(color="purple"))

    visual = Bar(
        data=210,
        width=100,
        value_range=(0, 300),
        color="red",
    )
    table.add_row("Bar", visual)
    visual = Bullet(
        data=210,
        target=250,
        width=100,
        limits=[0, 100, 200, 300],
        limit_colors=["red", "orange1", "green"],
    )
    table.add_row("Bullet", visual)
    data = [(1 + math.sin(math.pi * d / 12)) * 7.5 for d in range(100)]
    visual = Horizon(
        data=data,
        value_range=(0, 15),
        width=100,
    )
    table.add_row("Horizon", visual)
    visual = Sparkline(
        data=data,
        value_range=(0, 15),
        width=100,
        color="red",
    )
    table.add_row("Sparkline", visual)
    visual = Stack(
        data=(100, 50, 20, 10),
        width=100,
    )
    table.add_row("Stack", visual)
    data = [math.sin(math.pi * d / 12) * 7.5 for d in range(100)]
    visual = WinLoss(
        data=data,
        width=100,
        marks=BAR_HEAVY_V,
        colors=("red", "green"),
    )
    table.add_row("WinLoss", visual)

    console.print(table)


if __name__ == "__main__":  # pragma: no cover
    main()
