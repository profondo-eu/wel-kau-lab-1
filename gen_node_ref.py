#!/usr/bin/env python3
"""Generate node reference diagram (R1 || R2 with ground)."""

import schemdraw
import schemdraw.elements as elm
import os

OUT = "img"
DPI = 150

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)

    d += elm.Dot(open=True).label("węzeł 1", loc="top")
    J = d.here

    # R1 going down on the left
    d += elm.Resistor().down(3).label("$R_1$", loc="left")
    d += elm.Ground()
    G = d.here

    # R2 going down on the right
    d.move_from(J)
    d += elm.Line().right(3)
    d += elm.Resistor().down(3).label("$R_2$", loc="right")
    d += elm.Ground()

d.save(os.path.join(OUT, "lab1_wezel_odniesienia.png"), dpi=DPI)
print("saved lab1_wezel_odniesienia.png")
