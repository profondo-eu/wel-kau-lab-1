#!/usr/bin/env python3
"""Re-generate ALL graphics as PNG (not SVG) for GitHub compatibility."""

import schemdraw
import schemdraw.elements as elm
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "img"
os.makedirs(OUT, exist_ok=True)

DPI = 150

plt.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "figure.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "savefig.dpi": DPI,
})


def save_d(d, name):
    path = os.path.join(OUT, name)
    d.save(path, dpi=DPI)
    print(f"  {path}")


def save_f(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {path}")


# ═══════════════════════════════════════════════════════════════════════════
# LAB 1 — CIRCUIT SCHEMATICS
# ═══════════════════════════════════════════════════════════════════════════

print("── Lab 1: circuit schematics ──")

# 1. Resistor i-j
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł i", loc="left")
    d += elm.Resistor().right().label("R = 1/G", loc="top")
    d += elm.Dot(open=True).label("węzeł j", loc="right")
save_d(d, "lab1_01_rezystor_ij.png")

# 2. Resistor to ground
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł i", loc="left")
    d += elm.Resistor().down().label("R", loc="right")
    d += elm.Ground()
save_d(d, "lab1_02_rezystor_masa.png")

# 3. Current source
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł a", loc="left")
    d += elm.SourceI().right().label("$I_s$", loc="top")
    d += elm.Dot(open=True).label("węzeł b", loc="right")
save_d(d, "lab1_03_zrodlo_pradowe.png")

# 4. Voltage source
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("węzeł i (+)", loc="left")
    d += elm.SourceV().right().label("$V_s$", loc="top").reverse()
    d += elm.Dot(open=True).label("węzeł j (−)", loc="right")
save_d(d, "lab1_04_zrodlo_napieciowe.png")

# 5. Voltage divider
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
save_d(d, "lab1_05_dzielnik.png")

# 6. Two voltage sources (conflict)
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
save_d(d, "lab1_06_dwa_zrodla.png")

# 7. Current source circuit
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
save_d(d, "lab1_07_zrodlo_pradowe_obwod.png")

# 8. Diode circuit
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
save_d(d, "lab1_08_obwod_dioda.png")

# 9. Diode companion model
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("anoda (a)", loc="left")
    d += elm.Line().right(1.5)
    J = d.here
    d += elm.Resistor().down(3).label("$g_d$", loc="right")
    B1 = d.here
    d.move_from(J)
    d += elm.Line().right(3)
    d += elm.SourceI().down(3).label("$I_{eq}$", loc="right")
    B2 = d.here
    d += elm.Line().left(3).tox(B1)
    d += elm.Line().down(0.5)
    d += elm.Dot(open=True).label("katoda (k)", loc="left")
save_d(d, "lab1_09_model_zastepczy_diody.png")

# 10. RC for .NODESET/.IC
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
save_d(d, "lab1_10_rc_nodeset_ic.png")


# ═══════════════════════════════════════════════════════════════════════════
# LAB 1 — PLOTS
# ═══════════════════════════════════════════════════════════════════════════

print("── Lab 1: plots ──")

# Diode I-V
Is = 1e-14; Vt = 0.026
V = np.linspace(-0.2, 0.8, 500)
I_mA = np.clip(Is * (np.exp(V / Vt) - 1) * 1e3, -1, 50)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(V, I_mA, "b-", linewidth=2)
ax.set_xlabel("$V_D$ [V]"); ax.set_ylabel("$I_D$ [mA]")
ax.set_title("Charakterystyka I-V diody")
ax.set_xlim(-0.2, 0.85); ax.set_ylim(-2, 50)
ax.axhline(0, color="k", linewidth=0.5); ax.axvline(0, color="k", linewidth=0.5)
ax.annotate("$I_D = I_S \\cdot (e^{V_D/V_T} - 1)$", xy=(0.5, 20), fontsize=12,
            color="blue", bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"))
fig.tight_layout()
save_f(fig, "lab1_dioda_iv.png")

# Linearization
V0 = 0.6
I0 = Is * (np.exp(V0 / Vt) - 1)
gd = Is / Vt * np.exp(V0 / Vt)
V_tang = np.linspace(0.45, 0.75, 100)
I_tang = I0 + gd * (V_tang - V0)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(V, I_mA, "b-", linewidth=2, label="krzywa I-V")
ax.plot(V_tang, I_tang * 1e3, "r--", linewidth=2, label=f"styczna w $V_0={V0}$V")
ax.plot(V0, I0 * 1e3, "ro", markersize=10, zorder=5, label="punkt pracy")
ax.set_xlabel("$V_D$ [V]"); ax.set_ylabel("$I_D$ [mA]")
ax.set_title("Linearyzacja — model zastępczy diody")
ax.set_xlim(0.3, 0.8); ax.set_ylim(-5, 50)
ax.legend(loc="upper left")
ax.annotate(f"$g_d$ = nachylenie stycznej\n= {gd:.1f} S", xy=(V0+0.02, I0*1e3+5),
            fontsize=11, bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"))
fig.tight_layout()
save_f(fig, "lab1_linearyzacja.png")

# Newton-Raphson graphical
def f(x): return x**3 - 2*x - 5
def fp(x): return 3*x**2 - 2
fig, ax = plt.subplots(figsize=(6, 4))
x_r = np.linspace(1, 3.5, 200)
ax.plot(x_r, f(x_r), "b-", linewidth=2, label="$f(x) = x^3 - 2x - 5$")
ax.axhline(0, color="k", linewidth=0.5)
xn = 3.0
colors = ["#e41a1c", "#ff7f00", "#4daf4a"]
for i in range(3):
    yn = f(xn); ypn = fp(xn); xn1 = xn - yn/ypn
    xt = np.linspace(xn-0.8, xn+0.5, 50)
    ax.plot(xt, yn+ypn*(xt-xn), "--", color=colors[i], linewidth=1.5, alpha=0.7)
    ax.plot(xn, yn, "o", color=colors[i], markersize=8, zorder=5)
    ax.annotate(f"$x_{i}$={xn:.3f}", xy=(xn, -3-i*3), fontsize=10, color=colors[i], ha="center")
    xn = xn1
ax.set_xlabel("x"); ax.set_ylabel("f(x)")
ax.set_title("Metoda Newtona-Raphsona — wizualizacja"); ax.set_ylim(-15, 25); ax.legend()
fig.tight_layout()
save_f(fig, "lab1_newton_raphson.png")

# N-R convergence
fig, ax = plt.subplots(figsize=(6, 3.5))
iters = np.arange(1, 7); errors = [1, 0.1, 0.01, 1e-4, 1e-8, 1e-16]
ax.semilogy(iters, errors, "ro-", markersize=8, linewidth=2)
ax.set_xlabel("Numer iteracji"); ax.set_ylabel("Błąd (skala log)")
ax.set_title("Zbieżność kwadratowa N-R"); ax.set_ylim(1e-18, 10)
for i, e in enumerate(errors):
    ax.annotate(f"{e:.0e}", xy=(iters[i]+0.15, e), fontsize=10)
fig.tight_layout()
save_f(fig, "lab1_zbieznosc_NR.png")

# .NODESET vs .IC
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
t_ns = np.linspace(0, 5e-6, 200); tau_ns = 1e-6
ax1.axhline(0, color="blue", linewidth=2.5)
ax1.set_xlabel("t [μs]"); ax1.set_ylabel("V(1) [V]")
ax1.set_title(".NODESET V(1)=5V"); ax1.set_ylim(-0.5, 6); ax1.set_xlim(0, 5)
ax1.annotate("V = 0V (brak źródła → DC = 0)", xy=(1, 0.5), fontsize=11,
             color="blue", bbox=dict(boxstyle="round", fc="lightyellow"))
ax2.plot(t_ns*1e6, 5*np.exp(-t_ns/tau_ns), "r-", linewidth=2.5)
ax2.set_xlabel("t [μs]"); ax2.set_title(".IC V(1)=5V"); ax2.set_xlim(0, 5)
ax2.annotate("rozładowanie\neksponencjalne", xy=(1.5, 3), fontsize=12,
             color="red", bbox=dict(boxstyle="round", fc="lightyellow"))
fig.suptitle("Porównanie .NODESET vs .IC", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab1_nodeset_vs_ic.png")


# ═══════════════════════════════════════════════════════════════════════════
# LAB 2 — CIRCUIT SCHEMATICS
# ═══════════════════════════════════════════════════════════════════════════

print("── Lab 2: circuit schematics ──")

# RC main example
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
save_d(d, "lab2_01_obwod_rc.png")

# Capacitor alone
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("a", loc="top")
    d += elm.Capacitor().down(3).label("C", loc="right")
    d += elm.Dot(open=True).label("b", loc="bottom")
save_d(d, "lab2_02a_kondensator.png")

# Companion model
with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=14, unit=4)
    d += elm.Dot(open=True).label("a", loc="top")
    d += elm.Line().right(1.5)
    J = d.here
    d += elm.Resistor().down(3).label("$G_{eq}$", loc="right")
    B1 = d.here
    d.move_from(J)
    d += elm.Line().right(3)
    d += elm.SourceI().down(3).label("$I_{eq}$", loc="right")
    d += elm.Line().left(3).tox(B1)
    d += elm.Dot(open=True).label("b", loc="bottom")
save_d(d, "lab2_02b_model_stowarzyszony.png")

# RC for initial conditions
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
save_d(d, "lab2_03_rc_warunki_poczatkowe.png")


# ═══════════════════════════════════════════════════════════════════════════
# LAB 2 — PLOTS
# ═══════════════════════════════════════════════════════════════════════════

print("── Lab 2: plots ──")

# FE instability
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
tau = 1.0
t_exact = np.linspace(0, 5, 200); v_exact = 5*np.exp(-t_exact/tau)
h_ok = 0.3; t_ok = np.arange(0, 5, h_ok)
v_fe_ok = np.zeros_like(t_ok); v_fe_ok[0] = 5.0
for i in range(len(t_ok)-1): v_fe_ok[i+1] = v_fe_ok[i]*(1-h_ok/tau)
ax1.plot(t_exact, v_exact, "b-", lw=2, label="dokładne")
ax1.plot(t_ok, v_fe_ok, "ro-", ms=6, label=f"FE (h={h_ok})")
ax1.set_title(f"Stabilny (h={h_ok})"); ax1.set_xlabel("t"); ax1.set_ylabel("v(t)")
ax1.legend(); ax1.set_ylim(-2, 6)
h_bad = 2.5; t_bad = np.arange(0, 12, h_bad)
v_fe_bad = np.zeros_like(t_bad); v_fe_bad[0] = 5.0
for i in range(len(t_bad)-1): v_fe_bad[i+1] = v_fe_bad[i]*(1-h_bad/tau)
ax2.plot(np.linspace(0,12,200), 5*np.exp(-np.linspace(0,12,200)/tau), "b-", lw=2, label="dokładne")
ax2.plot(t_bad, v_fe_bad, "rx-", ms=8, lw=2, label=f"FE (h={h_bad}) — NIESTABILNY!")
ax2.set_title(f"NIESTABILNY (h={h_bad})"); ax2.set_xlabel("t"); ax2.legend(); ax2.set_ylim(-15, 15)
ax2.axhline(0, color="k", lw=0.5)
fig.suptitle("Forward Euler: dlaczego SPICE go NIE UŻYWA", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_fe_niestabilnosc.png")

# Method comparison
fig, ax = plt.subplots(figsize=(8, 5))
tau = 1.0; h = 0.5; N = 12
t_fe = np.arange(0, (N+1)*h, h)
v_fe = np.zeros(N+1); v_fe[0]=5.0
v_be = np.zeros(N+1); v_be[0]=5.0
v_tr = np.zeros(N+1); v_tr[0]=5.0
for i in range(N):
    v_fe[i+1] = v_fe[i]*(1-h/tau)
    v_be[i+1] = v_be[i]/(1+h/tau)
    v_tr[i+1] = v_tr[i]*(1-h/(2*tau))/(1+h/(2*tau))
t_ex = np.linspace(0, N*h, 500)
ax.plot(t_ex, 5*np.exp(-t_ex/tau), "k-", lw=2.5, label="dokładne", zorder=5)
ax.plot(t_fe, v_fe, "rs--", ms=6, label="Forward Euler")
ax.plot(t_fe, v_be, "g^--", ms=6, label="Backward Euler")
ax.plot(t_fe, v_tr, "bo--", ms=6, label="Trapezów (domyślna)")
ax.set_xlabel("t [s]"); ax.set_ylabel("v(t) [V]")
ax.set_title(f"Porównanie metod (h={h}s, τ={tau}s)"); ax.legend(); ax.set_ylim(-0.5, 5.5)
fig.tight_layout()
save_f(fig, "lab2_porownanie_metod.png")

# Trapezoidal oscillations
fig, ax = plt.subplots(figsize=(7, 4))
h_s = 1.0; tau_s = 0.01; N_s = 12; alpha_s = h_s/(2*tau_s)
v_tr_s = np.zeros(N_s+1); v_tr_s[0]=5.0
v_be_s = np.zeros(N_s+1); v_be_s[0]=5.0
for i in range(N_s):
    v_tr_s[i+1] = v_tr_s[i]*(1-alpha_s)/(1+alpha_s)
    v_be_s[i+1] = v_be_s[i]/(1+h_s/tau_s)
t_s = np.arange(0, (N_s+1)*h_s, h_s)
ax.plot(np.linspace(0,N_s*h_s,500), 5*np.exp(-np.linspace(0,N_s*h_s,500)/tau_s), "k-", lw=2, label="dokładne (→0)")
ax.plot(t_s, v_tr_s, "ro-", ms=6, lw=1.5, label="Trapezów — OSCYLACJE!")
ax.plot(t_s, v_be_s, "gs-", ms=6, lw=1.5, label="Backward Euler — OK")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("t"); ax.set_ylabel("v(t)")
ax.set_title("Oscylacje trapezów (równanie sztywne)"); ax.legend(loc="upper right")
fig.tight_layout()
save_f(fig, "lab2_trap_oscylacje.png")

# RC trapezoidal step
fig, ax = plt.subplots(figsize=(7, 4.5))
N_rc = 11; v_rc = np.zeros(N_rc); v_rc[0]=0
for i in range(N_rc-1): v_rc[i+1] = 0.6*v_rc[i] + 2.0
t_rc = np.arange(N_rc)*0.5
t_ex_rc = np.linspace(0, 5, 500)
ax.plot(t_ex_rc, 5*(1-np.exp(-t_ex_rc*1e-3/1e-3)), "b-", lw=2, label="dokładne: $5(1-e^{-t/\\tau})$")
ax.plot(t_rc, v_rc, "ro-", ms=8, lw=1.5, label="metoda trapezów (h=0.5ms)")
ax.axhline(5, color="gray", ls=":", lw=1, label="asymptota 5V")
ax.set_xlabel("t [ms]"); ax.set_ylabel("$V_2$ [V]")
ax.set_title("Obwód RC — metoda trapezów vs dokładne"); ax.legend()
ax.set_xlim(0, 5); ax.set_ylim(-0.3, 5.5)
fig.tight_layout()
save_f(fig, "lab2_rc_trapezy.png")

# Variable step
fig, ax = plt.subplots(figsize=(8, 4))
t_v = np.linspace(0, 10, 1000)
v_v = np.where(t_v<3, 0, np.where(t_v<3.5, 5*np.sin(2*np.pi*4*(t_v-3)),
      np.where(t_v<7, 5, np.where(t_v<7.5, 5*np.cos(2*np.pi*4*(t_v-7)), 0))))
ax.plot(t_v, v_v, "b-", lw=2)
all_tp = np.concatenate([np.array([0,0.5,1,1.5,2,2.5]), np.linspace(3,3.5,20),
                         np.array([3.6,4,4.5,5,5.5,6,6.5]), np.linspace(7,7.5,20),
                         np.array([7.6,8,8.5,9,9.5,10])])
for ti in all_tp: ax.axvline(ti, color="red", alpha=0.3, lw=0.5)
ax.plot(all_tp, np.zeros_like(all_tp), "r|", ms=10)
ax.set_xlabel("t"); ax.set_ylabel("V(t)")
ax.set_title("Algorytm zmiennokrokowy — gęstość punktów")
ax.annotate("DUŻY krok", xy=(1.2,-1.5), fontsize=11, color="green", ha="center",
            bbox=dict(boxstyle="round", fc="lightgreen", alpha=0.7))
ax.annotate("MAŁY krok", xy=(3.25,-1.5), fontsize=11, color="red", ha="center",
            bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.7))
ax.annotate("DUŻY krok", xy=(5.5,-1.5), fontsize=11, color="green", ha="center",
            bbox=dict(boxstyle="round", fc="lightgreen", alpha=0.7))
fig.tight_layout()
save_f(fig, "lab2_zmiennokrokowy.png")

# .NODESET vs .IC
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
t_ic = np.linspace(0, 5e-6, 200)
ax1.axhline(0, color="blue", lw=2.5)
ax1.set_xlabel("t [μs]"); ax1.set_ylabel("V(1) [V]")
ax1.set_title(".NODESET V(1)=5V"); ax1.set_ylim(-0.5, 6); ax1.set_xlim(0, 5)
ax1.annotate("V = 0V\n(DC bez źródła → 0)", xy=(1.5, 1), fontsize=12,
             color="blue", bbox=dict(boxstyle="round", fc="lightyellow"))
ax2.plot(t_ic*1e6, 5*np.exp(-t_ic/1e-6), "r-", lw=2.5)
ax2.set_xlabel("t [μs]"); ax2.set_title(".IC V(1)=5V"); ax2.set_xlim(0, 5)
ax2.annotate("rozładowanie\neksponencjalne", xy=(1.5, 3), fontsize=12,
             color="red", bbox=dict(boxstyle="round", fc="lightyellow"))
fig.suptitle("Porównanie .NODESET vs .IC  (obwód RC bez źródła)", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_nodeset_vs_ic.png")

# Sampling / Nyquist
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
f_sig = 3; t_c = np.linspace(0, 1, 1000); v_c = np.sin(2*np.pi*f_sig*t_c)
fs_g = 12; t_g = np.arange(0, 1, 1/fs_g)
ax1.plot(t_c, v_c, "b-", lw=1.5, alpha=0.5, label="ciągły")
ax1.stem(t_g, np.sin(2*np.pi*f_sig*t_g), linefmt="r-", markerfmt="ro", basefmt="k-",
         label=f"$f_s$={fs_g} Hz")
ax1.set_title(f"Dobre ($f_s={fs_g}$ > $2f={2*f_sig}$)"); ax1.set_xlabel("t [s]"); ax1.legend()
fs_b = 4; t_b = np.arange(0, 1, 1/fs_b)
ax2.plot(t_c, v_c, "b-", lw=1.5, alpha=0.3, label="oryginał 3 Hz")
ax2.stem(t_b, np.sin(2*np.pi*f_sig*t_b), linefmt="r-", markerfmt="rx", basefmt="k-",
         label=f"$f_s$={fs_b} Hz")
ax2.plot(t_c, -np.sin(2*np.pi*1*t_c), "r--", lw=1.5, alpha=0.7, label="alias 1 Hz")
ax2.set_title(f"ALIASING ($f_s={fs_b}$ < $2f={2*f_sig}$)"); ax2.set_xlabel("t [s]"); ax2.legend()
fig.suptitle("Twierdzenie Nyquista", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_probkowanie_nyquist.png")

# Aliasing freq domain
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
f_a = np.linspace(-15, 15, 1000); fs_a = 10
def spec(f, fc=3): return np.maximum(0, 1-np.abs(f)/fc)
for k in range(-2, 3):
    ax1.fill_between(f_a, spec(f_a-k*fs_a), alpha=0.3 if k==0 else 0.15,
                     color="blue" if k==0 else "gray")
ax1.axvline(-fs_a/2, color="red", ls="--", label="$\\pm f_s/2$")
ax1.axvline(fs_a/2, color="red", ls="--")
ax1.set_title(f"Brak aliasingu ($f_{{max}}$=3 < $f_s$/2={fs_a/2})"); ax1.set_ylabel("|X(f)|"); ax1.legend()
for k in range(-2, 3):
    ax2.fill_between(f_a, spec(f_a-k*fs_a, fc=7), alpha=0.3 if k==0 else 0.15,
                     color="blue" if k==0 else "gray")
ov = np.minimum(spec(f_a, fc=7), spec(f_a-fs_a, fc=7))
ax2.fill_between(f_a, ov, color="red", alpha=0.5, label="aliasing!")
ov2 = np.minimum(spec(f_a, fc=7), spec(f_a+fs_a, fc=7))
ax2.fill_between(f_a, ov2, color="red", alpha=0.5)
ax2.axvline(-fs_a/2, color="red", ls="--"); ax2.axvline(fs_a/2, color="red", ls="--")
ax2.set_title(f"ALIASING ($f_{{max}}$=7 > $f_s$/2={fs_a/2})"); ax2.set_xlabel("f [Hz]")
ax2.set_ylabel("|X(f)|"); ax2.legend()
fig.suptitle("Aliasing w dziedzinie częstotliwości", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_aliasing.png")

# DFT example
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
N_d = 10; fs_d = 1000; n_d = np.arange(N_d)
x_d = 2 + 3*np.cos(2*np.pi*100*n_d/fs_d)
ax1.stem(n_d, x_d, linefmt="b-", markerfmt="bo", basefmt="k-")
ax1.set_xlabel("n"); ax1.set_ylabel("x(n)")
ax1.set_title("Sygnał: $x = 2 + 3\\cos(2\\pi \\cdot 100 \\cdot t)$")
X_d = np.fft.fft(x_d); freqs_d = np.arange(N_d)*fs_d/N_d
amp_d = np.abs(X_d); amp_sc = np.copy(amp_d)
amp_sc[0] = amp_d[0]/N_d; amp_sc[1:] = amp_d[1:]*2/N_d
ax2.bar(freqs_d[:N_d//2+1], amp_sc[:N_d//2+1], width=30, color="steelblue", edgecolor="black")
ax2.set_xlabel("f [Hz]"); ax2.set_ylabel("Amplituda [V]")
ax2.set_title("Widmo DFT (skalowane)")
for i in range(N_d//2+1):
    if amp_sc[i]>0.1:
        ax2.annotate(f"{amp_sc[i]:.1f}V", xy=(freqs_d[i], amp_sc[i]+0.1), ha="center",
                     fontsize=11, fontweight="bold")
fig.suptitle("Przykład DFT: DC=2V + 3V@100Hz", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_dft_przyklad.png")

# Spectral leakage
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
N_l = 64; fs_l = 1000; n_l = np.arange(N_l); freqs_l = np.arange(N_l//2)*fs_l/N_l
f_ex = 5*fs_l/N_l
x1_l = 3*np.cos(2*np.pi*f_ex*n_l/fs_l); X1_l = np.fft.fft(x1_l)
ax1.bar(freqs_l, np.abs(X1_l[:N_l//2])*2/N_l, width=fs_l/N_l*0.7, color="steelblue", edgecolor="black")
ax1.set_xlabel("f [Hz]"); ax1.set_ylabel("Amplituda")
ax1.set_title(f"Brak przecieku ($f = {f_ex:.1f}$ Hz)"); ax1.set_xlim(0, 250)
f_lk = 5.37*fs_l/N_l
x2_l = 3*np.cos(2*np.pi*f_lk*n_l/fs_l); X2_l = np.fft.fft(x2_l)
ax2.bar(freqs_l, np.abs(X2_l[:N_l//2])*2/N_l, width=fs_l/N_l*0.7, color="orangered", edgecolor="black")
ax2.set_xlabel("f [Hz]"); ax2.set_title(f"PRZECIEK ($f = {f_lk:.1f}$ Hz)"); ax2.set_xlim(0, 250)
fig.suptitle("Przeciek widmowy (spectral leakage)", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_przeciek_widmowy.png")

# Windowing
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
n_w = np.arange(N_l)
rect = np.ones(N_l); hann = 0.5*(1-np.cos(2*np.pi*n_w/(N_l-1)))
hamming = 0.54 - 0.46*np.cos(2*np.pi*n_w/(N_l-1))
ax1.plot(n_w, rect, "b-", lw=2, label="Prostokątne")
ax1.plot(n_w, hann, "r-", lw=2, label="Hanninga")
ax1.plot(n_w, hamming, "g--", lw=2, label="Hamminga")
ax1.set_xlabel("n"); ax1.set_ylabel("w(n)"); ax1.set_title("Funkcje okna"); ax1.legend()
x_lk = 3*np.cos(2*np.pi*f_lk*n_w/fs_l)
X_rect = np.fft.fft(x_lk*rect); X_hann = np.fft.fft(x_lk*hann)
ax2.bar(freqs_l-3, np.abs(X_rect[:N_l//2])*2/N_l, width=fs_l/N_l*0.35,
        color="steelblue", edgecolor="black", alpha=0.7, label="Prostokątne")
ax2.bar(freqs_l+3, np.abs(X_hann[:N_l//2])*2/sum(hann)*N_l/2, width=fs_l/N_l*0.35,
        color="orangered", edgecolor="black", alpha=0.7, label="Hanninga")
ax2.set_xlabel("f [Hz]"); ax2.set_ylabel("Amplituda")
ax2.set_title(f"Efekt okienkowania ($f = {f_lk:.1f}$ Hz)"); ax2.set_xlim(0, 250); ax2.legend()
fig.suptitle("Okienkowanie — redukcja przecieku", fontsize=14, fontweight="bold")
fig.tight_layout()
save_f(fig, "lab2_okienkowanie.png")


print("\n✅ All PNG files generated!")
