#!/usr/bin/env python3
"""Generate plots for Lab 2."""

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


# ── 1. Forward Euler instability ─────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Stable case — small h
tau = 1.0
h_ok = 0.3
t_ok = np.arange(0, 5, h_ok)
v_fe_ok = np.zeros_like(t_ok)
v_fe_ok[0] = 5.0
for i in range(len(t_ok) - 1):
    v_fe_ok[i + 1] = v_fe_ok[i] + h_ok * (-v_fe_ok[i] / tau)

t_exact = np.linspace(0, 5, 200)
v_exact = 5 * np.exp(-t_exact / tau)

ax1.plot(t_exact, v_exact, "b-", linewidth=2, label="dokładne")
ax1.plot(t_ok, v_fe_ok, "ro-", markersize=6, label=f"FE (h={h_ok})")
ax1.set_title(f"Forward Euler — stabilny (h={h_ok})")
ax1.set_xlabel("t")
ax1.set_ylabel("v(t)")
ax1.legend()
ax1.set_ylim(-2, 6)

# Unstable case — large h
h_bad = 2.5
t_bad = np.arange(0, 12, h_bad)
v_fe_bad = np.zeros_like(t_bad)
v_fe_bad[0] = 5.0
for i in range(len(t_bad) - 1):
    v_fe_bad[i + 1] = v_fe_bad[i] + h_bad * (-v_fe_bad[i] / tau)

t_exact2 = np.linspace(0, 12, 200)
v_exact2 = 5 * np.exp(-t_exact2 / tau)

ax2.plot(t_exact2, v_exact2, "b-", linewidth=2, label="dokładne")
ax2.plot(t_bad, v_fe_bad, "rx-", markersize=8, linewidth=2, label=f"FE (h={h_bad}) — NIESTABILNY!")
ax2.set_title(f"Forward Euler — NIESTABILNY (h={h_bad})")
ax2.set_xlabel("t")
ax2.legend()
ax2.set_ylim(-15, 15)
ax2.axhline(0, color="k", linewidth=0.5)

fig.suptitle("Dlaczego SPICE nie używa Forward Euler", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_fe_niestabilnosc.svg"))
plt.close()
print("  saved lab2_fe_niestabilnosc.svg")


# ── 2. Comparison: FE vs BE vs Trapezoidal ──────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

tau = 1.0
h = 0.5
N = 12
t_exact = np.linspace(0, N * h, 500)
v_exact = 5 * np.exp(-t_exact / tau)

# Forward Euler
t_fe = np.arange(0, (N + 1) * h, h)
v_fe = np.zeros(N + 1)
v_fe[0] = 5.0
for i in range(N):
    v_fe[i + 1] = v_fe[i] * (1 - h / tau)

# Backward Euler
v_be = np.zeros(N + 1)
v_be[0] = 5.0
for i in range(N):
    v_be[i + 1] = v_be[i] / (1 + h / tau)

# Trapezoidal
v_tr = np.zeros(N + 1)
v_tr[0] = 5.0
for i in range(N):
    v_tr[i + 1] = v_tr[i] * (1 - h / (2 * tau)) / (1 + h / (2 * tau))

ax.plot(t_exact, v_exact, "k-", linewidth=2.5, label="dokładne", zorder=5)
ax.plot(t_fe[:N + 1], v_fe, "rs--", markersize=6, label="Forward Euler")
ax.plot(t_fe[:N + 1], v_be, "g^--", markersize=6, label="Backward Euler")
ax.plot(t_fe[:N + 1], v_tr, "bo--", markersize=6, label="Trapezów (domyślna)")
ax.set_xlabel("t [s]")
ax.set_ylabel("v(t) [V]")
ax.set_title(f"Porównanie metod całkowania (h = {h}s, τ = {tau}s)")
ax.legend()
ax.set_ylim(-0.5, 5.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_porownanie_metod.svg"))
plt.close()
print("  saved lab2_porownanie_metod.svg")


# ── 3. Trapezoidal oscillations at step ─────────────────────────────────────

fig, ax = plt.subplots(figsize=(7, 4))

# Simulate a stiff system where trapezoidal oscillates
h = 1.0
tau = 0.01  # very stiff
N = 12

v_tr = np.zeros(N + 1)
v_tr[0] = 5.0
alpha = h / (2 * tau)
for i in range(N):
    v_tr[i + 1] = v_tr[i] * (1 - alpha) / (1 + alpha)

v_be = np.zeros(N + 1)
v_be[0] = 5.0
for i in range(N):
    v_be[i + 1] = v_be[i] / (1 + h / tau)

t = np.arange(0, (N + 1) * h, h)
t_exact = np.linspace(0, N * h, 500)
v_exact = 5 * np.exp(-t_exact / tau)

ax.plot(t_exact, v_exact, "k-", linewidth=2, label="dokładne (→ 0 natychmiast)")
ax.plot(t, v_tr, "ro-", markersize=6, linewidth=1.5, label="Trapezów — OSCYLACJE!")
ax.plot(t, v_be, "gs-", markersize=6, linewidth=1.5, label="Backward Euler — OK")
ax.axhline(0, color="k", linewidth=0.5)
ax.set_xlabel("t")
ax.set_ylabel("v(t)")
ax.set_title("Oscylacje metody trapezów (równanie sztywne, h/τ >> 1)")
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_trap_oscylacje.svg"))
plt.close()
print("  saved lab2_trap_oscylacje.svg")


# ── 4. RC step response — trapezoidal method example ────────────────────────

fig, ax = plt.subplots(figsize=(7, 4.5))

tau_rc = 1e-3  # RC = 1ms
h_rc = 0.5e-3  # h = 0.5ms
alpha_rc = h_rc / (2 * tau_rc)  # = 0.25

# Trapezoidal for RC step: V2(n) = 0.6*V2(n-1) + 2.0
N_rc = 11
v_tr_rc = np.zeros(N_rc)
v_tr_rc[0] = 0
for i in range(N_rc - 1):
    v_tr_rc[i + 1] = 0.6 * v_tr_rc[i] + 2.0

t_rc = np.arange(N_rc) * h_rc * 1e3  # in ms
t_exact_rc = np.linspace(0, 5, 500)
v_exact_rc = 5 * (1 - np.exp(-t_exact_rc * 1e-3 / tau_rc))

ax.plot(t_exact_rc, v_exact_rc, "b-", linewidth=2, label="dokładne: $5(1-e^{-t/\\tau})$")
ax.plot(t_rc, v_tr_rc, "ro-", markersize=8, linewidth=1.5, label="metoda trapezów (h=0.5ms)")
ax.axhline(5, color="gray", linestyle=":", linewidth=1, label="asymptota 5V")
ax.set_xlabel("t [ms]")
ax.set_ylabel("$V_2$ [V]")
ax.set_title("Obwód RC — metoda trapezów vs rozwiązanie dokładne")
ax.legend()
ax.set_xlim(0, 5)
ax.set_ylim(-0.3, 5.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_rc_trapezy.svg"))
plt.close()
print("  saved lab2_rc_trapezy.svg")


# ── 5. Variable time step visualization ──────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 4))

t = np.linspace(0, 10, 1000)
# Signal with slow and fast parts
v = np.where(t < 3, 0, np.where(t < 3.5, 5 * np.sin(2 * np.pi * 4 * (t - 3)),
     np.where(t < 7, 5, np.where(t < 7.5, 5 * np.cos(2 * np.pi * 4 * (t - 7)), 0))))

ax.plot(t, v, "b-", linewidth=2)

# Sparse points in slow regions
t_slow1 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5])
t_fast = np.linspace(3.0, 3.5, 20)
t_mid = np.array([3.6, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5])
t_fast2 = np.linspace(7.0, 7.5, 20)
t_slow2 = np.array([7.6, 8.0, 8.5, 9.0, 9.5, 10.0])

all_t = np.concatenate([t_slow1, t_fast, t_mid, t_fast2, t_slow2])
for ti in all_t:
    ax.axvline(ti, color="red", alpha=0.3, linewidth=0.5)
ax.plot(all_t, np.zeros_like(all_t), "r|", markersize=10)

ax.set_xlabel("t")
ax.set_ylabel("V(t)")
ax.set_title("Algorytm zmiennokrokowy — gęstość punktów obliczeniowych")
ax.annotate("DUŻY krok\n(wolna zmiana)", xy=(1.2, -1.5), fontsize=11, color="green",
            ha="center", bbox=dict(boxstyle="round", fc="lightgreen", alpha=0.7))
ax.annotate("MAŁY krok\n(szybka zmiana)", xy=(3.25, -1.5), fontsize=11, color="red",
            ha="center", bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.7))
ax.annotate("DUŻY krok", xy=(5.5, -1.5), fontsize=11, color="green",
            ha="center", bbox=dict(boxstyle="round", fc="lightgreen", alpha=0.7))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_zmiennokrokowy.svg"))
plt.close()
print("  saved lab2_zmiennokrokowy.svg")


# ── 6. .IC vs .NODESET ──────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

tau_ns = 1e-6  # 1μs
t_ns = np.linspace(0, 5e-6, 200)

ax1.axhline(0, color="blue", linewidth=2.5)
ax1.set_xlabel("t [μs]")
ax1.set_ylabel("V(1) [V]")
ax1.set_title(".NODESET V(1)=5V")
ax1.set_ylim(-0.5, 6)
ax1.set_xlim(0, 5)
ax1.annotate("V = 0V\n(DC bez źródła → 0)", xy=(1.5, 1), fontsize=12,
             color="blue", bbox=dict(boxstyle="round", fc="lightyellow"))

V_ic = 5 * np.exp(-t_ns / tau_ns)
ax2.plot(t_ns * 1e6, V_ic, "r-", linewidth=2.5)
ax2.set_xlabel("t [μs]")
ax2.set_title(".IC V(1)=5V")
ax2.set_xlim(0, 5)
ax2.annotate("rozładowanie\neksponencjalne", xy=(1.5, 3), fontsize=12,
             color="red", bbox=dict(boxstyle="round", fc="lightyellow"))

fig.suptitle("Porównanie .NODESET vs .IC  (obwód RC bez źródła)", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_nodeset_vs_ic.svg"))
plt.close()
print("  saved lab2_nodeset_vs_ic.svg")


# ── 7. Sampling & Nyquist ───────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

f_sig = 3  # Hz
t_cont = np.linspace(0, 1, 1000)
v_cont = np.sin(2 * np.pi * f_sig * t_cont)

# Good sampling: fs = 12 Hz
fs_good = 12
t_good = np.arange(0, 1, 1 / fs_good)
v_good = np.sin(2 * np.pi * f_sig * t_good)

ax1.plot(t_cont, v_cont, "b-", linewidth=1.5, alpha=0.5, label="ciągły")
ax1.stem(t_good, v_good, linefmt="r-", markerfmt="ro", basefmt="k-", label=f"$f_s$={fs_good} Hz")
ax1.set_title(f"Dobre próbkowanie ($f_s={fs_good}$ > $2f={2*f_sig}$)")
ax1.set_xlabel("t [s]")
ax1.legend(loc="upper right")

# Bad sampling: fs = 4 Hz (barely above 2*f but let's show aliasing with fs < 2f)
fs_bad = 4
t_bad = np.arange(0, 1, 1 / fs_bad)
v_bad = np.sin(2 * np.pi * f_sig * t_bad)
# Reconstructed aliased signal
f_alias = fs_bad - f_sig  # = 1 Hz
v_alias = np.sin(2 * np.pi * f_alias * t_cont + np.angle(np.exp(-1j * 2 * np.pi * f_sig * 0)))

ax2.plot(t_cont, v_cont, "b-", linewidth=1.5, alpha=0.3, label="oryginał 3 Hz")
ax2.stem(t_bad, v_bad, linefmt="r-", markerfmt="rx", basefmt="k-", label=f"$f_s$={fs_bad} Hz")
ax2.plot(t_cont, -np.sin(2 * np.pi * 1 * t_cont), "r--", linewidth=1.5, alpha=0.7,
         label=f"alias {f_alias} Hz")
ax2.set_title(f"ALIASING ($f_s={fs_bad}$ < $2f={2*f_sig}$)")
ax2.set_xlabel("t [s]")
ax2.legend(loc="upper right")

fig.suptitle("Twierdzenie Nyquista — próbkowanie", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_probkowanie_nyquist.svg"))
plt.close()
print("  saved lab2_probkowanie_nyquist.svg")


# ── 8. Aliasing in frequency domain ─────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

f = np.linspace(-15, 15, 1000)
fs = 10

# Original spectrum — triangle
def spectrum(f, fc=3):
    return np.maximum(0, 1 - np.abs(f) / fc)

# Good case: fs = 10, fmax = 3 (3 < 5 = fs/2)
for k in range(-2, 3):
    ax1.fill_between(f, spectrum(f - k * fs), alpha=0.3 if k == 0 else 0.15,
                     color="blue" if k == 0 else "gray")
    ax1.plot(f, spectrum(f - k * fs), "b-" if k == 0 else "gray",
             linewidth=1.5 if k == 0 else 1)
ax1.axvline(-fs / 2, color="red", linestyle="--", label="$\\pm f_s/2$")
ax1.axvline(fs / 2, color="red", linestyle="--")
ax1.set_title(f"Brak aliasingu: $f_{{max}}=3$ Hz < $f_s/2={fs/2}$ Hz")
ax1.set_ylabel("|X(f)|")
ax1.legend()
ax1.set_xlim(-15, 15)

# Bad case: fmax = 7 > fs/2 = 5
for k in range(-2, 3):
    ax2.fill_between(f, spectrum(f - k * fs, fc=7), alpha=0.3 if k == 0 else 0.15,
                     color="blue" if k == 0 else "gray")
    ax2.plot(f, spectrum(f - k * fs, fc=7), "b-" if k == 0 else "gray",
             linewidth=1.5 if k == 0 else 1)
# Highlight overlap
overlap = np.minimum(spectrum(f, fc=7), spectrum(f - fs, fc=7))
ax2.fill_between(f, overlap, color="red", alpha=0.5, label="aliasing!")
overlap2 = np.minimum(spectrum(f, fc=7), spectrum(f + fs, fc=7))
ax2.fill_between(f, overlap2, color="red", alpha=0.5)
ax2.axvline(-fs / 2, color="red", linestyle="--", label="$\\pm f_s/2$")
ax2.axvline(fs / 2, color="red", linestyle="--")
ax2.set_title(f"ALIASING: $f_{{max}}=7$ Hz > $f_s/2={fs/2}$ Hz")
ax2.set_xlabel("f [Hz]")
ax2.set_ylabel("|X(f)|")
ax2.legend()
ax2.set_xlim(-15, 15)

fig.suptitle("Aliasing w dziedzinie częstotliwości", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_aliasing.svg"))
plt.close()
print("  saved lab2_aliasing.svg")


# ── 9. DFT example ──────────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

N = 10
fs = 1000
n = np.arange(N)
t_n = n / fs
x = 2 + 3 * np.cos(2 * np.pi * 100 * t_n)

ax1.stem(n, x, linefmt="b-", markerfmt="bo", basefmt="k-")
ax1.set_xlabel("n (numer próbki)")
ax1.set_ylabel("x(n)")
ax1.set_title("Sygnał: $x = 2 + 3\\cos(2\\pi \\cdot 100 \\cdot t)$")

X = np.fft.fft(x)
freqs = np.arange(N) * fs / N
amp = np.abs(X)
amp_scaled = np.copy(amp)
amp_scaled[0] = amp[0] / N
amp_scaled[1:] = amp[1:] * 2 / N

ax2.bar(freqs[:N // 2 + 1], amp_scaled[:N // 2 + 1], width=30, color="steelblue",
        edgecolor="black")
ax2.set_xlabel("f [Hz]")
ax2.set_ylabel("Amplituda [V]")
ax2.set_title("Widmo DFT (skalowane)")
for i in range(N // 2 + 1):
    if amp_scaled[i] > 0.1:
        ax2.annotate(f"{amp_scaled[i]:.1f}V", xy=(freqs[i], amp_scaled[i] + 0.1),
                     ha="center", fontsize=11, fontweight="bold")

fig.suptitle("Przykład DFT: DC=2V + 3V@100Hz", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_dft_przyklad.svg"))
plt.close()
print("  saved lab2_dft_przyklad.svg")


# ── 10. Spectral leakage ────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

N = 64
fs = 1000
n = np.arange(N)

# No leakage: f = exactly on a bin
f_exact = 5 * fs / N  # = 78.125 Hz → bin 5
x1 = 3 * np.cos(2 * np.pi * f_exact * n / fs)
X1 = np.fft.fft(x1)
freqs = np.arange(N // 2) * fs / N

ax1.bar(freqs, np.abs(X1[:N // 2]) * 2 / N, width=fs / N * 0.7, color="steelblue",
        edgecolor="black")
ax1.set_xlabel("f [Hz]")
ax1.set_ylabel("Amplituda")
ax1.set_title(f"Brak przecieku ($f = {f_exact:.1f}$ Hz = bin DFT)")
ax1.set_xlim(0, 250)

# With leakage: f between bins
f_leak = 5.37 * fs / N  # doesn't land on a bin
x2 = 3 * np.cos(2 * np.pi * f_leak * n / fs)
X2 = np.fft.fft(x2)

ax2.bar(freqs, np.abs(X2[:N // 2]) * 2 / N, width=fs / N * 0.7, color="orangered",
        edgecolor="black")
ax2.set_xlabel("f [Hz]")
ax2.set_title(f"PRZECIEK ($f = {f_leak:.1f}$ Hz ≠ bin DFT)")
ax2.set_xlim(0, 250)

fig.suptitle("Przeciek widmowy (spectral leakage)", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_przeciek_widmowy.svg"))
plt.close()
print("  saved lab2_przeciek_widmowy.svg")


# ── 11. Windowing ────────────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

N = 64
n = np.arange(N)

# Windows
rect = np.ones(N)
hann = 0.5 * (1 - np.cos(2 * np.pi * n / (N - 1)))
hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))

ax1.plot(n, rect, "b-", linewidth=2, label="Prostokątne")
ax1.plot(n, hann, "r-", linewidth=2, label="Hanninga")
ax1.plot(n, hamming, "g--", linewidth=2, label="Hamminga")
ax1.set_xlabel("n")
ax1.set_ylabel("w(n)")
ax1.set_title("Funkcje okna")
ax1.legend()

# Spectrum with leakage signal — rectangular vs Hann
f_leak = 5.37 * fs / N
x_leak = 3 * np.cos(2 * np.pi * f_leak * n / fs)
X_rect = np.fft.fft(x_leak * rect)
X_hann = np.fft.fft(x_leak * hann)
freqs = np.arange(N // 2) * fs / N

ax2.bar(freqs - 3, np.abs(X_rect[:N // 2]) * 2 / N, width=fs / N * 0.35,
        color="steelblue", edgecolor="black", alpha=0.7, label="Prostokątne")
ax2.bar(freqs + 3, np.abs(X_hann[:N // 2]) * 2 / sum(hann) * N / 2, width=fs / N * 0.35,
        color="orangered", edgecolor="black", alpha=0.7, label="Hanninga")
ax2.set_xlabel("f [Hz]")
ax2.set_ylabel("Amplituda")
ax2.set_title(f"Efekt okienkowania ($f = {f_leak:.1f}$ Hz)")
ax2.set_xlim(0, 250)
ax2.legend()

fig.suptitle("Okienkowanie — redukcja przecieku widmowego", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "lab2_okienkowanie.svg"))
plt.close()
print("  saved lab2_okienkowanie.svg")


print("\n✓ Lab 2: all plots generated")
