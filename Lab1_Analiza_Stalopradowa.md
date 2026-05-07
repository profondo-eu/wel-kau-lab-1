# Laboratoria 1 — Badanie Algorytmów Analizy Stałoprądowej

## Zagadnienia na wejściówkę

- Tworzenie równania macierzowego (szablony/stemple elementów)
- Zmodyfikowana metoda węzłowa (MNA)
- Algorytm Newtona-Raphsona (N-R) dla układów nieliniowych

---

## 1. Równanie macierzowe obwodu

Program SPICE rozwiązuje obwód elektryczny sprowadzając go do układu równań liniowych w postaci macierzowej:

```
G * V = I
```

gdzie:
- **G** — macierz konduktancji (conductance matrix), wymiar n×n
- **V** — wektor nieznanych potencjałów węzłowych, wymiar n×1
- **I** — wektor wymuszeń prądowych, wymiar n×1
- **n** — liczba węzłów w obwodzie (bez węzła odniesienia/masy)

### Węzeł odniesienia

Jeden z węzłów obwodu jest wybierany jako **węzeł odniesienia** (masa, węzeł 0). Potencjały pozostałych węzłów mierzone są względem niego.

---

## 2. Szablony (stemple) elementów — metoda węzłowa

Każdy element obwodu wnosi swój wkład do macierzy G i wektora I według określonego **szablonu** (stamp). Szablon mówi, które komórki macierzy i wektora trzeba zmodyfikować po dodaniu danego elementu.

### 2.1 Rezystor (konduktancja G = 1/R)

Rezystor podłączony między węzłami **i** oraz **j**:

```
Macierz G:          Wektor I:
     i      j
i [ +G    -G  ]     [ 0 ]
j [ -G    +G  ]     [ 0 ]
```

**Przykład:** R = 2 kΩ między węzłami 1 i 2, G = 1/2000 = 0.5 mS

```
     1       2
1 [ +0.5m  -0.5m ]
2 [ -0.5m  +0.5m ]
```

Rezystor podłączony między węzłem **i** a masą (węzeł 0):

```
Macierz G:     Wektor I:
     i
i [ +G ]       [ 0 ]
```

### 2.2 Niezależne źródło prądowe

Źródło prądowe I_s, prąd płynie z węzła **i** do węzła **j** (strzałka od i do j):

```
Macierz G:       Wektor I:
(brak zmian)      i: [ -I_s ]
                  j: [ +I_s ]
```

Prąd **wpływający** do węzła daje + w wektorze I, **wypływający** daje -.

**Przykład:** Źródło 5 mA, prąd płynie od masy (0) do węzła 1:

```
Wektor I:
1: [ +5m ]
```

### 2.3 Niezależne źródło napięciowe (wymaga rozszerzenia — MNA)

Źródło napięciowe **nie da się** bezpośrednio opisać w klasycznej metodzie węzłowej (konduktancja nieskończona). Rozwiązanie: **zmodyfikowana metoda węzłowa** (Modified Nodal Analysis).

---

## 3. Zmodyfikowana Metoda Węzłowa (MNA)

### Idea

Dla elementów, których nie da się opisać konduktancją (źródła napięciowe, cewki idealne, źródła sterowane napięciem), wprowadza się **dodatkowe niewiadome** — prądy płynące przez te elementy — i **dodatkowe równania**.

Rozszerzone równanie macierzowe:

```
┌        ┐   ┌   ┐   ┌   ┐
│  G   B │   │ V │   │ I │
│        │ * │   │ = │   │
│  C   D │   │ J │   │ E │
└        ┘   └   ┘   └   ┘
```

gdzie:
- **V** — potencjały węzłowe (n sztuk)
- **J** — dodatkowe niewiadome, najczęściej prądy gałęziowe (m sztuk)
- **G** — macierz konduktancji n×n
- **B, C** — macierze łączące (n×m i m×n)
- **D** — macierz m×m (zwykle zera lub impedancje)
- **I** — wymuszenia prądowe
- **E** — wymuszenia napięciowe

### 3.1 Szablon źródła napięciowego (MNA)

Źródło napięciowe V_s między węzłami **i** (+) i **j** (-), z dodatkową niewiadomą I_v (prąd przez źródło):

```
        i    j    I_v          RHS
i   [              +1  ]    [     ]
j   [              -1  ]    [     ]
I_v [ +1   -1      0   ]    [ V_s ]
```

**Interpretacja:**
- Wiersze i, j: prąd I_v wpływa do węzła i (+1) i wypływa z j (-1)
- Wiersz I_v: równanie V_i - V_j = V_s

**Przykład:** Źródło 10V, + przy węźle 1, - przy węźle 2:

```
        1    2    I_v          RHS
1   [              +1  ]    [    ]
2   [              -1  ]    [    ]
I_v [ +1   -1      0   ]    [ 10 ]
```

### 3.2 Szablon źródła sterowanego napięciem (VCVS)

Źródło napięciowe sterowane napięciem: V_out = μ * V_sterujące

```
        i+   i-   o+   o-   I_v         RHS
o+  [                        +1  ]    [   ]
o-  [                        -1  ]    [   ]
I_v [ -μ   +μ    +1   -1     0  ]    [ 0 ]
```

### 3.3 Szablon źródła sterowanego prądem (VCCS)

Źródło prądowe sterowane napięciem: I_out = g * V_sterujące

```
Macierz G:
        i+    i-
o+  [  +g    -g  ]
o-  [  -g    +g  ]
```

To źródło **nie wymaga** dodatkowej zmiennej — wchodzi bezpośrednio do macierzy G.

---

## 4. Pełny przykład konstrukcji równania macierzowego

### Obwód: R1(1kΩ) między węzłami 1-2, R2(2kΩ) między węzłem 2 a masą, źródło V1=5V przy węźle 1

**Krok 1:** Identyfikacja — 2 węzły (1, 2), 1 źródło napięciowe → 1 dodatkowa zmienna I_V1

**Krok 2:** Wymiar macierzy: 3×3 (2 węzły + 1 prąd)

**Krok 3:** Nanoszenie szablonów (stemplowanie):

R1 = 1kΩ, G1 = 1mS, między węzłami 1-2:
```
     1      2
1 [ +1m   -1m  ]
2 [ -1m   +1m  ]
```

R2 = 2kΩ, G2 = 0.5mS, między węzłem 2 a masą:
```
     2
2 [ +0.5m ]
```

V1 = 5V, + przy węźle 1, - przy masie:
```
       1    I_V1       RHS
1   [       +1   ]   [   ]
I_V1[ +1     0   ]   [ 5 ]
```

**Krok 4:** Złożenie pełnej macierzy:

```
         1       2      I_V1       RHS
1   [  +1m     -1m      +1   ]   [  0  ]
2   [  -1m    +1.5m      0   ]   [  0  ]
I_V1[  +1       0        0   ]   [  5  ]
```

**Krok 5:** Rozwiązanie → V1 = 5V, V2 = 5·(0.5/1.5) ≈ 1.667V, I_V1 = ...

---

## 5. Analiza stałoprądowa (DC) — punkt pracy

Analiza DC w SPICE polega na:
1. Usunięciu elementów reaktancyjnych (C → rozwarcie, L → zwarcie)
2. Konstrukcji równania macierzowego G·V = I
3. Rozwiązaniu układu równań (dekompozycja LU)

Dla obwodów **liniowych** — jedno rozwiązanie daje wynik.

---

## 6. Analiza układu nieliniowego — algorytm Newtona-Raphsona

### Problem

Elementy nieliniowe (diody, tranzystory) mają charakterystyki opisane funkcjami nieliniowymi, np.:

**Dioda:** I_D = I_S · (e^(V_D / V_T) - 1)

gdzie I_S ≈ 10⁻¹⁴ A, V_T ≈ 26 mV (w temp. pokojowej)

Równanie macierzowe staje się **nieliniowe** — nie można go rozwiązać jednym krokiem.

### Linearyzacja — model zastępczy

W każdym kroku iteracji element nieliniowy zastępowany jest **liniowym modelem zastępczym** (linearyzacja w punkcie pracy):

Dla diody w punkcie pracy (V_D0, I_D0):

```
I_D ≈ I_D0 + g_d · (V_D - V_D0)
```

gdzie **g_d** to konduktancja dynamiczna (pochodna charakterystyki):

```
g_d = dI_D / dV_D |_(V_D = V_D0) = I_S / V_T · e^(V_D0 / V_T)
```

Model zastępczy diody = **równoległe połączenie konduktancji g_d i źródła prądowego I_eq**:

```
I_eq = I_D0 - g_d · V_D0
```

### Szablon diody (model zastępczy) w MNA

Dioda między węzłami i (anoda) i j (katoda):

```
Macierz G:           Wektor I:
     i      j
i [ +g_d  -g_d ]    [ +I_eq ]
j [ -g_d  +g_d ]    [ -I_eq ]
```

### Algorytm Newtona-Raphsona (N-R)

```
1. Wybierz punkt startowy V⁰ (np. 0V na wszystkich węzłach)
2. Powtarzaj (k = 0, 1, 2, ...):
   a) Oblicz modele zastępcze elementów nieliniowych w punkcie V^k
      (wyznacz g_d i I_eq dla każdego elementu)
   b) Zbuduj równanie macierzowe: G(V^k) · V = I(V^k)
   c) Rozwiąż układ równań → otrzymaj V^(k+1)
   d) Sprawdź zbieżność:
      |V^(k+1) - V^k| < ε  (tolerancja)
      Jeśli tak → KONIEC (znaleziono punkt pracy)
      Jeśli nie → wróć do kroku (a) z V^(k+1)
```

### Zbieżność

- N-R zbiega **kwadratowo** (bardzo szybko) gdy punkt startowy jest blisko rozwiązania
- Może **nie zbiegać** gdy punkt startowy jest daleko od rozwiązania
- SPICE stosuje dodatkowe techniki wspomagające zbieżność:
  - **Source stepping** — stopniowe zwiększanie wartości źródeł od 0 do wartości docelowej
  - **GMIN stepping** — dodanie małych konduktancji do masy
  - **.NODESET** — podpowiedzi dla punktu startowego

### Kryteria zbieżności w SPICE

Dwa rodzaje kryteriów sprawdzanych jednocześnie:
1. **Kryterium napięciowe:** |V^(k+1)_n - V^k_n| < VNTOL (domyślnie 1 μV)
2. **Kryterium prądowe:** |I^(k+1)_n - I^k_n| < ABSTOL + RELTOL · max(|I^k|) (domyślnie ABSTOL = 1 pA, RELTOL = 0.001)

Oba kryteria muszą być spełnione **jednocześnie** dla wszystkich węzłów/gałęzi.

### Parametr ITL1

**ITL1** = maksymalna liczba iteracji N-R w analizie DC (domyślnie 100). Jeśli po ITL1 iteracjach nie osiągnięto zbieżności → błąd "no convergence".

---

## 7. Potencjały startowe

Dla obwodów nieliniowych z wieloma rozwiązaniami (np. przerzutniki) ważny jest wybór punktu startowego:

### .NODESET V(n) = wartość

Podpowiedź dla algorytmu — program dodaje tymczasowe źródło napięciowe, znajduje punkt pracy, usuwa źródło i kontynuuje. Wynik końcowy **nie musi** być równy podanej wartości.

### .IC V(n) = wartość

Wymusza warunek początkowy — potencjał węzła **będzie** równy podanej wartości na początku analizy.

---

## 8. Analiza DC sweep

Źródło wymuszające zmienia wartość w zadanym zakresie, w każdym punkcie wykonywana jest pełna analiza DC:

```
.DC V1 0V 10V 0.1V
```

Oznacza: V1 zmienia się od 0 do 10V krokiem 0.1V. Punkt pracy z poprzedniego kroku służy jako punkt startowy dla następnego.

---

## 9. Typowe pytania na wejściówkę

1. **Zapisz szablon rezystora/źródła napięciowego/źródła prądowego w MNA**
2. **Dla danego obwodu (2-3 węzły) skonstruuj pełne równanie macierzowe**
3. **Wyjaśnij, dlaczego źródło napięciowe wymaga dodatkowej zmiennej w MNA**
4. **Opisz algorytm N-R — jakie są kroki jednej iteracji?**
5. **Czym jest model zastępczy elementu nieliniowego? Narysuj dla diody**
6. **Co oznacza zbieżność kwadratowa algorytmu N-R?**
7. **Wymień metody wspomagania zbieżności w SPICE**
8. **Jaka jest różnica między .NODESET a .IC?**
9. **Co się stanie, gdy algorytm N-R nie osiągnie zbieżności? (ITL1)**
10. **Dla obwodu z diodą — jak wygląda jedno przejście pętli N-R?**
