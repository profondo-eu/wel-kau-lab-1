#!/usr/bin/env python3
"""Generate circuit diagram for the stamp-combining example (Iźr + R1-R4)."""

import schemdraw
import schemdraw.elements as elm
import os

OUT = "img"
DPI = 150

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)

    # Current source: GND → node 1 (arrow up)
    d += (Is := elm.SourceI().up().label("$I_{źr} = 6\\,mA$", loc="left"))
    d += elm.Dot().label("1", loc="top")
    J1 = d.here

    # R1: node 1 → node 2
    d += elm.Resistor().right(4).label("$R_1 = 2\\,k\\Omega$", loc="top")
    d += elm.Dot().label("2", loc="top")
    J2 = d.here

    # R3: node 2 → node 3
    d += elm.Resistor().right(4).label("$R_3 = 2\\,k\\Omega$", loc="top")
    d += elm.Dot().label("3", loc="top")
    J3 = d.here

    # R4: node 3 → GND
    d += elm.Resistor().down().label("$R_4 = 2\\,k\\Omega$", loc="right")
    d += elm.Ground()
    G = d.here

    # Bottom line from GND back to Is start
    d += elm.Line().left(8).tox(Is.start)
    d += elm.Line().up().toy(Is.start)

    # R2: node 2 → GND
    d.move_from(J2)
    d += elm.Resistor().down().label("$R_2 = 2\\,k\\Omega$", loc="right")
    d += elm.Line().down().toy(G)

d.save(os.path.join(OUT, "lab1_00_przyklad_szablony.png"), dpi=DPI)
print("saved lab1_00_przyklad_szablony.png")
