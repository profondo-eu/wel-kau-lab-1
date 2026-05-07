#!/usr/bin/env python3
"""Generate circuit diagrams for Lab 2 (Time-domain & Spectral Analysis)."""

import schemdraw
import schemdraw.elements as elm
import os

OUT = "img"
os.makedirs(OUT, exist_ok=True)


def save(d, name):
    path = os.path.join(OUT, name)
    d.save(path)
    print(f"  saved {path}")


# ── 1. RC circuit (main example) ────────────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += (V1 := elm.SourceV().up().label("$V_1 = 5V$\n(skok w t=0)", loc="left").reverse())
    d += elm.Line().right(3)
    d += elm.Dot().label("1", loc="right")
    d += elm.Resistor().down().label("$R = 1\\,k\\Omega$", loc="right")
    d += elm.Dot().label("2", loc="right")
    d += elm.Capacitor().down().label("$C = 1\\,\\mu F$", loc="right")
    d += elm.Ground()
    d += elm.Line().left(3).tox(V1.start)
    d += elm.Line().up().toy(V1.start)
save(d, "lab2_01_obwod_rc.svg")


# ── 2. Companion model: capacitor alone ─────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("a", loc="top")
    d += elm.Capacitor().down(3).label("C", loc="right")
    d += elm.Dot(open=True).label("b", loc="bottom")
save(d, "lab2_02a_kondensator.svg")


# ── 2b. Companion model: equivalent R + I_source ────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("a", loc="top")
    A = d.here
    d += elm.Line().right(1.5)
    J = d.here
    d += elm.Resistor().down(3).label("$G_{eq}$", loc="right")
    B1 = d.here
    d.move_from(J)
    d += elm.Line().right(3)
    d += elm.SourceI().down(3).label("$I_{eq}$", loc="right")
    B2 = d.here
    d += elm.Line().left(3).tox(B1)
    d += elm.Dot(open=True).label("b", loc="bottom")
save(d, "lab2_02b_model_stowarzyszony.svg")


# ── 3. RC circuit for .IC/.NODESET comparison ───────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł 1", loc="top")
    J = d.here
    d += elm.Resistor().down(3).label("$R$", loc="right")
    d += elm.Ground()
    d.move_from(J)
    d += elm.Line().right(3)
    d += elm.Capacitor().down(3).label("$C$", loc="right")
    d += elm.Ground()
save(d, "lab2_03_rc_warunki_poczatkowe.svg")


print("\n✓ Lab 2: all circuits generated")
