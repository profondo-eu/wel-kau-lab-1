#!/usr/bin/env python3
"""Generate circuit diagrams for Lab 1 (DC Analysis)."""

import schemdraw
import schemdraw.elements as elm
import os

OUT = "img"
os.makedirs(OUT, exist_ok=True)


def save(d, name):
    path = os.path.join(OUT, name)
    d.save(path)
    print(f"  saved {path}")


# ── 1. Resistor stamp: R between nodes i and j ──────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł i", loc="left")
    d += elm.Resistor().right().label("R = 1/G", loc="top")
    d += elm.Dot(open=True).label("węzeł j", loc="right")
save(d, "lab1_01_rezystor_ij.svg")


# ── 2. Resistor to ground ───────────────────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł i", loc="left")
    d += elm.Resistor().down().label("R", loc="right")
    d += elm.Ground()
save(d, "lab1_02_rezystor_masa.svg")


# ── 3. Current source stamp ─────────────────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł a", loc="left")
    d += elm.SourceI().right().label("$I_s$", loc="top")
    d += elm.Dot(open=True).label("węzeł b", loc="right")
save(d, "lab1_03_zrodlo_pradowe.svg")


# ── 4. Voltage source stamp ─────────────────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł i (+)", loc="left")
    d += elm.SourceV().right().label("$V_s$", loc="top").reverse()
    d += elm.Dot(open=True).label("węzeł j (−)", loc="right")
save(d, "lab1_04_zrodlo_napieciowe.svg")


# ── 5. Example 1: Voltage divider V1-R1-R2 ─────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += (V1 := elm.SourceV().up().label("$V_1 = 10V$", loc="left").reverse())
    d += elm.Line().right(3)
    d += elm.Dot().label("1", loc="right")
    d += elm.Resistor().down().label("$R_1 = 1\\,k\\Omega$", loc="right")
    d += elm.Dot().label("2", loc="right")
    d += elm.Resistor().down().label("$R_2 = 2\\,k\\Omega$", loc="right")
    d += elm.Ground()
    d += elm.Line().left(3).tox(V1.start)
    d += elm.Line().up().toy(V1.start)
save(d, "lab1_05_dzielnik.svg")


# ── 6. Example 2: Two voltage sources (parallel conflict) ──────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += (V1 := elm.SourceV().up().label("$V_1 = 5V$", loc="left").reverse())
    d += elm.Line().right(2)
    d += elm.Dot().label("1", loc="top")
    J1 = d.here
    d += elm.Line().right(2)
    d += (V2 := elm.SourceV().down().label("$V_2 = 3V$", loc="right"))
    d += elm.Ground()
    d += elm.Line().left(4).tox(V1.start)
    d += elm.Line().up().toy(V1.start)
    d.move_from(J1)
    d += elm.Resistor().down().label("$R_1 = 1\\,k\\Omega$", loc="right")
    d += elm.Dot().label("2", loc="right")
    d += elm.Resistor().down().label("$R_2 = 2\\,k\\Omega$", loc="right")
    d += elm.Ground()
save(d, "lab1_06_dwa_zrodla.svg")


# ── 7. Example 3: Current source circuit ────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += (IS := elm.SourceI().up().label("$I_s = 2\\,mA$", loc="left"))
    d += elm.Dot().label("1", loc="top")
    J1 = d.here
    d += elm.Resistor().right(4).label("$R_1 = 1\\,k\\Omega$", loc="top")
    d += elm.Dot().label("2", loc="top")
    J2 = d.here
    d += elm.Resistor().down().label("$R_3 = 3\\,k\\Omega$", loc="right")
    d += elm.Ground()
    G = d.here
    d += elm.Line().left(4).tox(IS.start)
    d += elm.Line().up().toy(IS.start)
    d.move_from(J1)
    d += elm.Resistor().down().label("$R_2 = 2\\,k\\Omega$", loc="right")
    d += elm.Line().down().toy(G)
save(d, "lab1_07_zrodlo_pradowe_obwod.svg")


# ── 8. Example 4: Diode circuit ─────────────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += (V1 := elm.SourceV().up().label("$V_1 = 5V$", loc="left").reverse())
    d += elm.Line().right(3)
    d += elm.Dot().label("1", loc="right")
    d += elm.Resistor().down().label("$R = 1\\,k\\Omega$", loc="right")
    d += elm.Dot().label("2", loc="right")
    d += elm.Diode().down().label("$D$", loc="right")
    d += elm.Ground()
    d += elm.Line().left(3).tox(V1.start)
    d += elm.Line().up().toy(V1.start)
save(d, "lab1_08_obwod_dioda.svg")


# ── 9. Diode companion model (linearized) ───────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("anoda (a)", loc="left")
    A = d.here
    d += elm.Line().right(1.5)
    J = d.here
    d += elm.Resistor().down(3).label("$g_d$", loc="right")
    B1 = d.here
    d.move_from(J)
    d += elm.Line().right(3)
    J2 = d.here
    d += elm.SourceI().down(3).label("$I_{eq}$", loc="right")
    B2 = d.here
    d += elm.Line().left(3).tox(B1)
    d += elm.Line().down(0.5)
    d += elm.Dot(open=True).label("katoda (k)", loc="left")
save(d, "lab1_09_model_zastepczy_diody.svg")


# ── 10. RC circuit for .NODESET/.IC ─────────────────────────────────────────

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł 1", loc="top")
    J = d.here
    d += elm.Resistor().down(3).label("$R = 1\\,k\\Omega$", loc="right")
    d += elm.Ground()
    d.move_from(J)
    d += elm.Line().right(3)
    d += elm.Capacitor().down(3).label("$C = 1\\,nF$", loc="right")
    d += elm.Ground()
save(d, "lab1_10_rc_nodeset_ic.svg")


print("\n✓ Lab 1: all circuits generated")
