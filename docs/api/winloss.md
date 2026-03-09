---
title: "WinLoss"
---

```rich
from rich_illuminations import WinLoss
from rich.table import Table
from graphical.mark import BAR_LIGHT_V, BAR_HEAVY_V
from rich.box import HORIZONTALS
from math import sin, cos

data = [sin(x) * cos(x/5) for x in range(50)]
colors = ["green", "red"]

table = Table(box=None, padding=(1,1), show_header=False, show_edge=False, show_lines=False)
table.add_row("Default", WinLoss(data=data, colors=colors))
table.add_row("BAR_LIGHT_V", WinLoss(data=data, colors=colors, marks=BAR_LIGHT_V))
table.add_row("BAR_HEAVY_V", WinLoss(data=data, colors=colors, marks=BAR_HEAVY_V))

output = table
```

::: rich_illuminations.WinLoss
