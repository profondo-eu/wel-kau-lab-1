#!/usr/bin/env python3
"""Generate plots for Lab 1."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import os

OUT = "img"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "figure.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
})


# ── 1. Diode I-V characteristic ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(6, 4))
Is = 1e-14
Vt = 0.026
V = np.linspace(-0.2, 0.8, 500)
I = Is * (np.exp(V / Vt) - 1)
I_mA = I * 1e3
I_mA = np.clip(I_mA, -1, 50)

ax.plot(V, I_mA, "b-", linewidth=2)
ax.set_xlabel("$V_D$ [V]")
ax.set_ylabel("$I_D$ [mA]")
ax.set_title("Charakterystyka I-V diody")
ax.set_xlim(-0.2, 0.85)
ax.set_ylim(-2, 50)
ax.axhline(0, color="k", linewidth=0.5)
ax.axvline(0, color="k", linewidth=0.5)
ax.annotate("$I_D = I_S \\cdot (e^{V_D/V_T} - 1)$",
            xy=(0.5, 20), fontsize=12, color="blue",
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab1_dioda_iv.svg"))
plt.close()
print("  saved lab1_dioda_iv.svg")


# ── 2. Linearization / tangent line ─────────────────────────────────────────

fig, ax = plt.subplots(figsize=(6, 4))
V0 = 0.6
I0 = Is * (np.exp(V0 / Vt) - 1)
gd = Is / Vt * np.exp(V0 / Vt)

V_tang = np.linspace(0.45, 0.75, 100)
I_tang = I0 + gd * (V_tang - V0)

ax.plot(V, I_mA, "b-", linewidth=2, label="krzywa I-V")
ax.plot(V_tang, I_tang * 1e3, "r--", linewidth=2, label=f"styczna w $V_0={V0}$V")
ax.plot(V0, I0 * 1e3, "ro", markersize=10, zorder=5, label="punkt pracy")
ax.set_xlabel("$V_D$ [V]")
ax.set_ylabel("$I_D$ [mA]")
ax.set_title("Linearyzacja — model zastępczy diody")
ax.set_xlim(0.3, 0.8)
ax.set_ylim(-5, 50)
ax.legend(loc="upper left")
ax.annotate(f"$g_d$ = nachylenie stycznej\n= {gd:.1f} S",
            xy=(V0 + 0.02, I0 * 1e3 + 5), fontsize=11,
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow"))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab1_linearyzacja.svg"))
plt.close()
print("  saved lab1_linearyzacja.svg")


# ── 3. Newton-Raphson graphical ──────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(6, 4))

def f(x):
    return x**3 - 2*x - 5

def fp(x):
    return 3*x**2 - 2

x = np.linspace(1, 3.5, 200)
ax.plot(x, f(x), "b-", linewidth=2, label="$f(x) = x^3 - 2x - 5$")
ax.axhline(0, color="k", linewidth=0.5)

xn = 3.0
colors = ["#e41a1c", "#ff7f00", "#4daf4a"]
for i in range(3):
    yn = f(xn)
    ypn = fp(xn)
    xn1 = xn - yn / ypn
    xt = np.linspace(xn - 0.8, xn + 0.5, 50)
    yt = yn + ypn * (xt - xn)
    ax.plot(xt, yt, "--", color=colors[i], linewidth=1.5, alpha=0.7)
    ax.plot(xn, yn, "o", color=colors[i], markersize=8, zorder=5)
    ax.annotate(f"$x_{i}$={xn:.3f}", xy=(xn, -3 - i * 3), fontsize=10, color=colors[i],
                ha="center")
    xn = xn1

ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Metoda Newtona-Raphsona — wizualizacja")
ax.set_ylim(-15, 25)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab1_newton_raphson.svg"))
plt.close()
print("  saved lab1_newton_raphson.svg")


# ── 4. N-R convergence (quadratic) ──────────────────────────────────────────

fig, ax = plt.subplots(figsize=(6, 3.5))
iters = np.arange(1, 7)
errors = [1, 0.1, 0.01, 1e-4, 1e-8, 1e-16]
ax.semilogy(iters, errors, "ro-", markersize=8, linewidth=2)
ax.set_xlabel("Numer iteracji")
ax.set_ylabel("Błąd (skala log)")
ax.set_title("Zbieżność kwadratowa N-R")
ax.set_ylim(1e-18, 10)
for i, e in enumerate(errors):
    ax.annotate(f"{e:.0e}", xy=(iters[i] + 0.15, e), fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab1_zbieznosc_NR.svg"))
plt.close()
print("  saved lab1_zbieznosc_NR.svg")


# ── 5. .NODESET vs .IC comparison ───────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

t = np.linspace(0, 5e-6, 200)
tau = 1e-3 * 1e-9  # R=1kΩ, C=1nF → τ=1μs

# .NODESET → V=0 (DC without source gives 0)
ax1.axhline(0, color="blue", linewidth=2)
ax1.set_xlabel("t [μs]")
ax1.set_ylabel("V(1) [V]")
ax1.set_title(".NODESET V(1)=5V")
ax1.set_ylim(-0.5, 6)
ax1.set_xlim(0, 5)
ax1.annotate("V = 0V (brak źródła → DC = 0)", xy=(1, 0.5), fontsize=11,
             color="blue", bbox=dict(boxstyle="round", fc="lightyellow"))

# .IC → exponential decay from 5V
V_ic = 5 * np.exp(-t / tau)
ax2.plot(t * 1e6, V_ic, "r-", linewidth=2)
ax2.set_xlabel("t [μs]")
ax2.set_title(".IC V(1)=5V")
ax2.set_xlim(0, 5)
ax2.annotate("rozładowanie\neksponencjalne", xy=(1.5, 3), fontsize=11,
             color="red", bbox=dict(boxstyle="round", fc="lightyellow"))

fig.suptitle("Porównanie .NODESET vs .IC", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab1_nodeset_vs_ic.svg"))
plt.close()
print("  saved lab1_nodeset_vs_ic.svg")


print("\n✓ Lab 1: all plots generated")
