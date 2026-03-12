---
title: "Horizon"
---

```rich
from math import sin, cos, exp
from rich_illuminations import Horizon

data = [
    (
        1.7 * sin(i / 8.5)
        + 1.1 * cos(i / 4.8)
        + 1.8 * sin(i / 2.6)
        + 4.6 * exp(-((i - 45) ** 2) / 40)
        - 1.2
    )
    for i in range(72)
]

output = Horizon(
    data=data,
)
```

::: rich_illuminations.Horizon
