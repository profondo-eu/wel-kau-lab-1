# Laboratoria 2 — Badanie Algorytmów Analizy Czasowej i Widmowej

> **Cel:** Zrozumieć, jak SPICE symuluje zachowanie obwodu w czasie (metody numeryczne)
> i jak analizuje sygnał w dziedzinie częstotliwości (DFT).

---

## Spis treści

### Część I — Analiza czasowa
1. [O co chodzi w analizie czasowej?](#1-o-co-chodzi-w-analizie-czasowej)
2. [Modele stowarzyszone — zamiana C i L na rezystory](#2-modele-stowarzyszone--zamiana-c-i-l-na-rezystory)
3. [Metoda Eulera ekstrapolacyjna (Forward Euler)](#3-metoda-eulera-ekstrapolacyjna-forward-euler)
4. [Metoda Eulera interpolacyjna (Backward Euler)](#4-metoda-eulera-interpolacyjna-backward-euler)
5. [Metoda trapezów](#5-metoda-trapezów)
6. [Metody Geara (BDF)](#6-metody-geara-bdf)
7. [Porównanie metod — który wybrać?](#7-porównanie-metod--który-wybrać)
8. [Przykład: Obwód RC krok po kroku](#8-przykład-obwód-rc-krok-po-kroku)
9. [Algorytm zmiennokrokowy](#9-algorytm-zmiennokrokowy)
10. [Warunki początkowe (.IC vs .NODESET)](#10-warunki-początkowe-ic-vs-nodeset)

### Część II — Analiza widmowa
11. [Po co analiza widmowa?](#11-po-co-analiza-widmowa)
12. [Ortogonalność — fundament analizy widmowej](#12-ortogonalność--fundament-analizy-widmowej)
13. [Transformata Fouriera — intuicja](#13-transformata-fouriera--intuicja)
14. [Próbkowanie i twierdzenie Nyquista](#14-próbkowanie-i-twierdzenie-nyquista)
15. [Aliasing — co się psuje przy złym próbkowaniu](#15-aliasing--co-się-psuje-przy-złym-próbkowaniu)
16. [Dyskretna Transformata Fouriera (DFT)](#16-dyskretna-transformata-fouriera-dft)
17. [Przykład: DFT krok po kroku](#17-przykład-dft-krok-po-kroku)
18. [Przeciek widmowy (spectral leakage)](#18-przeciek-widmowy-spectral-leakage)
19. [Okienkowanie — lekarstwo na przeciek](#19-okienkowanie--lekarstwo-na-przeciek)
20. [Ściąga na wejściówkę](#20-ściąga-na-wejściówkę)

---

# CZĘŚĆ I — ANALIZA CZASOWA

## 1. O co chodzi w analizie czasowej?

### Problem

Masz obwód z kondensatorem lub cewką. Podajesz sygnał (np. skok napięcia) i chcesz wiedzieć,
**jak napięcia i prądy zmieniają się w czasie**.

```
      PRZED (t < 0)                    PO (t = 0: włączamy źródło)

         ┌───┐                              V₁ = 5V
         │ R │                             (+)  (-)
         │   │                              │    │
    ─────┤   ├─────                    ┌────┘    └──═══
         │   │                         │
         └───┘                      węzeł 1
           │                           │
          ═══                        ┌───┐
                                     │ R │ 1kΩ
      Nic się nie dzieje             └─┬─┘
                                       │
                                    węzeł 2
                                       │
                                     ─┤├─  C = 1nF
                                       │
                                      ═══

                    Pytanie: jak V(2) zmienia się w czasie?
```

Odpowiedź analityczna: V₂(t) = 5·(1 - e^(-t/RC)) — ale SPICE **nie zna** tego wzoru!
SPICE rozwiązuje to **numerycznie**, krok po kroku.

### Kluczowa idea

Kondensator i cewka opisane są równaniami różniczkowymi:

```
    Kondensator:  i_C = C · dv/dt     (prąd zależy od SZYBKOŚCI zmiany napięcia)
    Cewka:        v_L = L · di/dt     (napięcie zależy od SZYBKOŚCI zmiany prądu)
```

SPICE nie umie rozwiązywać równań różniczkowych bezpośrednio. Zamiast tego:

```
    ┌────────────────────┐         ┌────────────────────┐
    │   Kondensator      │         │   Rezystor + źródło │
    │   (równanie        │  ────►  │   (model liniowy    │
    │    różniczkowe)    │         │    — można wstawić  │
    │                    │         │    do macierzy!)    │
    └────────────────────┘         └────────────────────┘
           oryginał                   model stowarzyszony
                                     (companion model)
```

**Model stowarzyszony** zamienia kondensator/cewkę na **rezystor + źródło prądowe**,
których wartości zależą od metody numerycznej i od poprzednich kroków czasowych.

---

## 2. Modele stowarzyszone — zamiana C i L na rezystory

### Ogólna postać modelu stowarzyszonego

Każda metoda numeryczna daje inny model, ale wszystkie mają tę samą strukturę:

```
        Kondensator:                 Model stowarzyszony:

          węzeł a                       węzeł a
             │                             │
           ─┤├─  C                      ┌──┴──┐
             │                          │     │
          węzeł b                      G_eq  I_eq
                                        │  ↑  │
                                        │  │  │
                                        └──┬──┘
                                        węzeł b

    G_eq = konduktancja zastępcza (zależy od C, h i metody)
    I_eq = źródło zastępcze (zależy od wartości z POPRZEDNICH kroków)
    h = krok czasowy (Δt)
```

**Szablon w macierzy** (identyczny jak rezystor + źródło prądowe!):

```
              kol. a    kol. b       RHS
wiersz a  [   +G_eq   -G_eq   ]    [ +I_eq ]
wiersz b  [   -G_eq   +G_eq   ]    [ -I_eq ]
```

To jest genialne: po zastąpieniu C i L modelami, cały obwód staje się **czysto rezystywny**
i SPICE może go rozwiązać tak samo jak obwód stałoprądowy (Lab 1)!

---

## 3. Metoda Eulera ekstrapolacyjna (Forward Euler)

### Idea — „zgadnij przyszłość na podstawie teraźniejszości"

Znasz nachylenie (pochodną) w punkcie t_n. Zakładasz, że to nachylenie się nie zmieni
i „jedziesz prosto" do następnego punktu:

```
     v(t)
      │
      │        ● t_(n+1) (prawdziwa wartość)
      │       ╱
      │     ╱  ← prawdziwa krzywa
      │   ╱
      │  ● ─ ─ ─ ─ ─ ─ ● t_(n+1) (przybliżenie FE)
      │ ╱    ↗
      │╱    nachylenie w t_n
      ● t_n
      │
      └──────────────────── t
              h
         ◄────────►
```

### Wzór

```
dv/dt ≈ (v(t_(n+1)) - v(t_n)) / h

    „zmiana napięcia" ≈ „nachylenie" × „krok czasowy"
```

### Model stowarzyszony kondensatora (FE)

```
G_eq = C / h
I_eq = -(C/h) · v(t_n)
```

### Właściwości

```
┌─────────────────────────────────────────────┐
│  Euler ekstrapolacyjny (Forward Euler)      │
├─────────────────────────────────────────────┤
│  Rząd dokładności:  1 (błąd ~ h)            │
│  Stabilność:        NIESTABILNA!            │
│  Stosowana w SPICE: NIE                     │
│  Typ:               jawna (explicit)        │
└─────────────────────────────────────────────┘
```

### Dlaczego niestabilna? — wizualizacja

Dla zbyt dużego kroku h wynik **oscyluje i rośnie** zamiast zbiegać:

```
     v(t)
      │    ×
      │   × ×         × ← oscylacje rosną!
      │  ×   ×       ×
      │ ×     ×     ×
      │×       ×   ×         (× = wynik Forward Euler)
      ●─────────×─×──────── (─ = prawdziwe rozwiązanie)
      │
      └──────────────────── t

      NIESTABILNE! Dlatego SPICE NIE UŻYWA tej metody.
```

---

## 4. Metoda Eulera interpolacyjna (Backward Euler)

### Idea — „nachylenie w NOWYM punkcie, nie starym"

Zamiast brać nachylenie z punktu starego (jak FE), bierzemy nachylenie z punktu **nowego**.
To sprawia, że trzeba rozwiązać układ równań (metoda niejawna), ale jest **stabilna**.

```
     v(t)
      │
      │        ● t_n (znamy)
      │       ╱
      │     ╱  ← nachylenie w t_n (czyli OBECNE)
      │   ╱
      ●──╱──────────── → tak liczy BE
     t_(n-1)
      │
      └──────────────────── t
              h
         ◄────────►
```

### Wzór

```
dv/dt ≈ (v(t_n) - v(t_(n-1))) / h
```

### Model stowarzyszony kondensatora (BE)

```
G_eq = C / h
I_eq = -(C/h) · v(t_(n-1))       ← wartość z POPRZEDNIEGO kroku
```

### Model stowarzyszony cewki (BE)

```
G_eq = h / L
I_eq = i_L(t_(n-1))              ← prąd z POPRZEDNIEGO kroku
```

### Właściwości

```
┌─────────────────────────────────────────────┐
│  Euler interpolacyjny (Backward Euler)      │
├─────────────────────────────────────────────┤
│  Rząd dokładności:  1 (błąd ~ h)            │
│  Stabilność:        BEZWARUNKOWA (zawsze!)  │
│  Stosowana w SPICE: rzadko (mało dokładna)  │
│  Typ:               niejawna (implicit)     │
└─────────────────────────────────────────────┘
```

---

## 5. Metoda trapezów

### Idea — „średnia nachyleń z OBU końców przedziału"

Zamiast brać nachylenie z jednego końca, bierzemy **średnią** nachyleń z lewego
i prawego końca przedziału. To daje znacznie lepszą dokładność:

```
     v(t)
      │
      │          ● t_n
      │        ╱╱
      │      ╱╱    ← prawdziwa krzywa
      │    ╱╱
      │  ● ╱
      │  ╱       nachylenie w t_(n-1): s₁
      ● t_(n-1)  nachylenie w t_n:     s₂
      │
      │  Przybliżenie: v(t_n) ≈ v(t_(n-1)) + h · (s₁ + s₂) / 2
      │                                          ↑
      └──────────────────── t        ŚREDNIA dwóch nachyleń
```

**Analogia geometryczna:** Pole pod krzywą przybliżamy **trapezem** (stąd nazwa):

```
     v'(t)
      │
   s₂ ┤───────────●
      │          ╱│
      │        ╱  │    Pole trapezu = h · (s₁ + s₂) / 2
      │      ╱    │
   s₁ ●───╱      │
      │          │
      └──┬───────┬── t
       t_(n-1)  t_n
         ◄───h───►
```

### Wzór

```
v(t_n) = v(t_(n-1)) + (h/2) · [v'(t_n) + v'(t_(n-1))]
```

### Model stowarzyszony kondensatora (trapezów)

```
G_eq = 2C / h                                        ← UWAGA: 2C/h (nie C/h!)
I_eq = -(2C/h) · v(t_(n-1)) - i_C(t_(n-1))          ← zależy od V i I z poprzedniego kroku
```

### Model stowarzyszony cewki (trapezów)

```
G_eq = h / (2L)                                      ← UWAGA: h/2L (nie h/L!)
I_eq = i_L(t_(n-1)) + (h/(2L)) · v_L(t_(n-1))       ← zależy od I i V z poprzedniego kroku
```

### Właściwości

```
┌─────────────────────────────────────────────┐
│  Metoda trapezów (Trapezoidal Rule)         │
├─────────────────────────────────────────────┤
│  Rząd dokładności:  2 (błąd ~ h²)           │
│  Stabilność:        warunkowa (h nie za duże)│
│  Stosowana w SPICE: TAK — DOMYŚLNA!        │
│  Typ:               niejawna (implicit)     │
│  Wada:              oscylacje numeryczne    │
│                     przy skokach sygnału    │
└─────────────────────────────────────────────┘
```

### Dlaczego domyślna?

Najlepszy kompromis: wysoka dokładność (rząd 2) + dobra wydajność + stabilność w większości przypadków.

### Oscylacje numeryczne — problem metody trapezów

Przy skokowej zmianie sygnału (np. przełączenie) metoda trapezów może generować
fałszywe oscylacje, których nie ma w prawdziwym sygnale:

```
     v(t)
      │
   5V ┤─────────────────────── prawdziwe rozwiązanie (płaskie)
      │    ×     ×     ×
   4V ┤
      │
   3V ┤
      │  ×     ×     ×        × = wynik metody trapezów
   2V ┤                          (fałszywe oscylacje!)
      │
      └──────────────────── t
         skok napięcia
```

W takich przypadkach lepiej sprawdza się metoda **Geara**.

---

## 6. Metody Geara (BDF)

### Idea — „użyj WIELU poprzednich punktów"

Metody Eulera i trapezów pamiętają tylko 1-2 poprzednie punkty.
Gear używa 2-6 poprzednich punktów — więcej historii = lepsze przewidywanie.

### Gear rząd 2

```
dv/dt ≈ (3·v(t_n) - 4·v(t_(n-1)) + v(t_(n-2))) / (2h)
```

Wykorzystuje wartości z **dwóch** poprzednich kroków (t_(n-1) i t_(n-2)).

### Gear rząd 3, 4, 5, 6 — analogicznie, coraz więcej historii

```
Gear 2: v(t_n), v(t_(n-1)), v(t_(n-2))                       ← 2 poprzednie
Gear 3: v(t_n), v(t_(n-1)), v(t_(n-2)), v(t_(n-3))           ← 3 poprzednie
...
Gear 6: v(t_n), ..., v(t_(n-6))                               ← 6 poprzednich
```

### Właściwości

```
┌─────────────────────────────────────────────┐
│  Metody Geara (BDF)                         │
├─────────────────────────────────────────────┤
│  Rząd dokładności:  2-6 (zależy od rzędu)   │
│  Stabilność:        BEZWARUNKOWA            │
│  Stosowana w SPICE: TAK (równania sztywne)  │
│  Typ:               niejawna (implicit)     │
│  Zaleta:            brak oscylacji          │
│  Wada:              potrzebuje „rozbiegu"   │
│                     (kilka pierwszych kroków)│
└─────────────────────────────────────────────┘
```

### Kiedy Gear zamiast trapezów?

**Równania sztywne** (stiff equations) — to obwody, w których występują jednocześnie
bardzo szybkie i bardzo wolne zjawiska:

```
Przykład: Tranzystor przełączający (nanosekundy)
          w obwodzie zasilania (milisekundy)

          Stosunek stałych czasowych: 10⁶ : 1 → równanie SZTYWNE

          Metoda trapezów: potrzebuje BARDZO małego kroku → wolna
          Metoda Geara:    radzi sobie z dużym krokiem → szybka
```

---

## 7. Porównanie metod — który wybrać?

### Tabela porównawcza

```
┌────────────────────┬───────┬──────────────┬───────────┬──────────────┐
│      Metoda        │ Rząd  │  Stabilność  │ Dokładność│ W SPICE?     │
├────────────────────┼───────┼──────────────┼───────────┼──────────────┤
│ Euler ekstrap. (FE)│   1   │ NIESTABILNA  │   niska   │     NIE      │
│ Euler interp. (BE) │   1   │ bezwarunkowa │   niska   │   rzadko     │
│ TRAPEZÓW (TR)      │   2   │ warunkowa    │   wysoka  │ TAK(domyślna)│
│ Geara (BDF)        │  2-6  │ bezwarunkowa │śr.-wysoka │ TAK(sztywne) │
└────────────────────┴───────┴──────────────┴───────────┴──────────────┘
```

### Schemat decyzyjny

```
                    Jaki obwód?
                        │
              ┌─────────┴──────────┐
              │                    │
        Typowy obwód          Równania sztywne
       (RC, RLC, OPamp)      (szybko+wolno jednocześnie)
              │                    │
              ▼                    ▼
        METODA TRAPEZÓW       METODA GEARA
        (domyślna SPICE)     (IsSpice: rząd 2-6)
```

### Modele stowarzyszone — zestawienie

```
┌──────────────────┬─────────────────────────────────────────────────┐
│                  │           KONDENSATOR C                          │
│     Metoda       ├──────────────────────┬──────────────────────────┤
│                  │       G_eq           │         I_eq             │
├──────────────────┼──────────────────────┼──────────────────────────┤
│ Forward Euler    │       C/h            │  -(C/h)·v(t_n)          │
│ Backward Euler   │       C/h            │  -(C/h)·v(t_(n-1))     │
│ TRAPEZÓW         │      2C/h            │  -(2C/h)·v(t_(n-1))    │
│                  │                      │   - i_C(t_(n-1))        │
└──────────────────┴──────────────────────┴──────────────────────────┘

┌──────────────────┬─────────────────────────────────────────────────┐
│                  │              CEWKA L                             │
│     Metoda       ├──────────────────────┬──────────────────────────┤
│                  │       G_eq           │         I_eq             │
├──────────────────┼──────────────────────┼──────────────────────────┤
│ Backward Euler   │       h/L            │  i_L(t_(n-1))           │
│ TRAPEZÓW         │      h/(2L)          │  i_L(t_(n-1))           │
│                  │                      │  + (h/2L)·v_L(t_(n-1))  │
└──────────────────┴──────────────────────┴──────────────────────────┘
```

---

## 8. Przykład: Obwód RC krok po kroku

### Obwód

```
      V₁ = 5V (skok w t=0)
     (+)   (-)
      │     │
 ┌────┘    ═══
 │
węzeł 1
 │
┌───┐
│ R │ = 1 kΩ
└─┬─┘
 │
węzeł 2
 │
─┤├─  C = 1 μF
 │
═══ (masa)
```

Rozwiązanie analityczne: V₂(t) = 5·(1 - e^(-t/τ)), gdzie τ = RC = 1ms

Policzmy **metodą trapezów** z krokiem **h = 0.5 ms**:

### Krok 0: t = 0, warunki początkowe

```
V₂(0) = 0 V  (kondensator rozładowany)
i_C(0) = 0 A
```

### Krok 1: t = 0.5 ms

Model stowarzyszony kondensatora (trapezów):
```
G_eq = 2C/h = 2·10⁻⁶ / 0.5·10⁻³ = 4 mS
I_eq = -(2C/h)·V₂(0) - i_C(0) = -4m·0 - 0 = 0
```

Równanie macierzowe (źródło V1 wymusza V1 = 5V):

```
              V1       V2      I_V1       RHS
wiersz 1  [ +1m      -1m       +1   ]   [  0  ]
wiersz 2  [ -1m    +1m+4m       0   ]   [  0  ]   ← 1m(R) + 4m(C_eq)
wiersz IV1[ +1        0         0   ]   [  5  ]
```

Rozwiązanie:
```
V1 = 5 V
V2: -1m·5 + 5m·V2 = 0  →  V2 = 5/5 = 1.000 V
i_C = G_eq·(V2-0) + I_eq = 4m·1 + 0 = 4 mA
```

### Krok 2: t = 1.0 ms

```
G_eq = 4 mS  (nie zmienia się — krok stały)
I_eq = -(2C/h)·V₂(0.5ms) - i_C(0.5ms) = -4m·1 - 4m = -8 mA
```

```
              V1       V2      I_V1       RHS
wiersz 1  [ +1m      -1m       +1   ]   [   0  ]
wiersz 2  [ -1m      +5m        0   ]   [ -8m  ]
wiersz IV1[ +1        0         0   ]   [   5  ]
```

```
V2: -1m·5 + 5m·V2 = -8m  →  5m·V2 = -8m + 5m = -3m  →  V2 = -3/5???
```

Hmm, to wygląda na błąd — sprawdźmy sign. I_eq wpływa do węzła 2:
```
wiersz 2: -1m·V1 + 5m·V2 = +I_eq = -8m
```

Poprawmy:
```
V2 = (-8m + 5m) / 5m — nie, wróćmy do KCL

KCL węzeł 2: prąd z R + prąd z modelu C = 0
Prąd z R do węzła 2: G_R·(V1-V2) = 1m·(5-V2)
Prąd z modelu C: G_eq·V2 + I_eq = 4m·V2 + (-8m)

Suma = 0:
1m·(5-V2) + 4m·V2 - 8m = 0
5m - 1m·V2 + 4m·V2 - 8m = 0
3m·V2 = 3m
V2 = 1.000 V??? To też nie wygląda dobrze.
```

Przeliczmy I_eq poprawnie:
```
i_C(0.5ms) = C·dv/dt ≈ (V2(0.5ms) - V2(0))/h · C... nie,
i_C to prąd przez kondensator = (V1-V2)/R = (5-1)/1000 = 4 mA ✓

I_eq = -(2C/h)·1 - 4m = -4m - 4m = -8m (RHS to +I_eq = -8mA)

KCL w 2: prąd z R (wpływa) + prąd modelu C = 0
(V1-V2)·G_R + (G_eq·V2 + I_eq) = 0
1m·(5-V2) + 4m·V2 + (-8m) = 0
5m - V2·1m + 4m·V2 - 8m = 0
V2·(4m - 1m) = 8m - 5m
V2·3m = 3m
V2 = 1.0 V
```

To nie wydaje się prawidłowe — V2 powinno rosnąć. Poprawmy: I_eq to prąd źródła zastępczego
modelu stowarzyszonego wchodzący do węzła, więc w RHS powinien być ze znakiem +.

Zróbmy inaczej — użyjmy jawnego wzoru metody trapezów:

```
V₂(t_n) = V₂(t_(n-1)) + (h/2)·[v'(t_n) + v'(t_(n-1))]

v' = dV₂/dt = (V₁ - V₂)/(R·C) = (5 - V₂) / 1ms
```

### Obliczenia krok po kroku (jawny wzór iteracyjny)

Przekształcając metodę trapezów dla obwodu RC:

```
V₂(t_n) = V₂(t_(n-1)) + (h/(2RC)) · [(5 - V₂(t_n)) + (5 - V₂(t_(n-1)))]
```

Przenosząc V₂(t_n) na lewą stronę (metoda niejawna!):

```
V₂(t_n) · [1 + h/(2RC)] = V₂(t_(n-1)) · [1 - h/(2RC)] + h/RC · 5
```

Dla h = 0.5ms, RC = 1ms, h/(2RC) = 0.25:

```
V₂(t_n) · 1.25 = V₂(t_(n-1)) · 0.75 + 2.5
V₂(t_n) = 0.6 · V₂(t_(n-1)) + 2.0
```

| Krok | Czas | V₂ (trapezów) | V₂ (dokładne) | Błąd |
|------|------|---------------|----------------|------|
| 0 | 0.0 ms | 0.000 V | 0.000 V | 0 |
| 1 | 0.5 ms | 2.000 V | 1.967 V | +0.033 V |
| 2 | 1.0 ms | 3.200 V | 3.161 V | +0.039 V |
| 3 | 1.5 ms | 3.920 V | 3.884 V | +0.036 V |
| 4 | 2.0 ms | 4.352 V | 4.323 V | +0.029 V |
| 5 | 2.5 ms | 4.611 V | 4.591 V | +0.020 V |
| 10 | 5.0 ms | 4.988 V | 4.993 V | -0.005 V |

### Wizualizacja

```
  V₂ [V]
   5 ┤─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ asymptota (5V)
     │                    ○─────○─────○─────
   4 ┤               ○╱
     │            ○╱          ○ = metoda trapezów
   3 ┤        ○╱              ─ = rozwiązanie dokładne
     │      ╱
   2 ┤  ○╱
     │ ╱
   1 ┤╱
     │
   0 ●───┬───┬───┬───┬───┬───┬───┬───┬───── t [ms]
     0  0.5  1  1.5  2  2.5  3  3.5  4
```

Metoda trapezów (rząd 2) daje **bardzo dobre** przybliżenie nawet przy grubym kroku h = 0.5ms.

---

## 9. Algorytm zmiennokrokowy

SPICE **nie używa** stałego kroku czasowego! Automatycznie dostosowuje h do dynamiki obwodu:

```
  V(t)
   │
   │                     ╱╲   ← szybkie zmiany
   │  ─ ─ ─ ─ ─ ─ ─ ─ ╱  ╲     = MAŁY krok
   │                  ╱    │╲
   │                 ╱     │ ╲
   │                ╱      │  ╲
   │               ╱       │   ╲
   │──────────────╱        │    ╲────────────
   │  ↑                    │              ↑
   │  wolne zmiany         │          wolne zmiany
   │  = DUŻY krok          │          = DUŻY krok
   └───┬──┬──┬──┬──┬──┬┬┬┬┬┬┬┬──┬──┬──┬──── t
       ○  ○  ○  ○  ○  ○○○○○○○○  ○  ○  ○
       ◄── duże ──►  ◄gęste►  ◄── duże ──►
           kroki       kroki       kroki

   ○ = punkty obliczeniowe (ich gęstość się zmienia!)
```

### Jak SPICE zmienia krok?

| Sytuacja | Co robi SPICE | Współczynnik |
|----------|--------------|-------------|
| Trzeba **skrócić** krok (szybkie zmiany) | Cofa się i zmniejsza krok | **÷ 8** (ośmiokrotnie) |
| Można **wydłużyć** krok (wolne zmiany) | Podwaja krok | **× 2** (dwukrotnie) |

Asymetria (÷8 vs ×2) jest celowa — lepiej szybko „wbić hamulce" niż wolno przyspieszać.

### Pierwszy punkt czasowy

```
t₁ = TStop / 50
```

### Limity kroku

```
Minimalny:  Δt_min = TStop / (50 · 10⁹)     ← bardzo mały!
Maksymalny: Δt_max = TStep  (metoda iteracji)
         lub TStop/50       (metoda błędu obcięcia)
```

### Trzy wskaźniki decydujące o zmianie kroku

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DYNAMIKA OBWODU (najważniejszy!)                         │
│    • Mało iteracji N-R → krok może rosnąć                   │
│    • Dużo iteracji N-R → krok musi maleć                    │
│    • Alternatywnie: lokalny błąd obcięcia (LTE)             │
├─────────────────────────────────────────────────────────────┤
│ 2. BRAK ZBIEŻNOŚCI                                          │
│    • N-R nie zbiega w ITL4 iteracjach → skrócenie kroku     │
├─────────────────────────────────────────────────────────────┤
│ 3. PUNKTY ZAŁAMANIA źródeł                                   │
│    • Skok napięcia / prądu → zagęszczenie punktów           │
└─────────────────────────────────────────────────────────────┘
```

### Deklaracja .TRAN

```
.TRAN  TStep  TStop  [TStart  [TMax]]  [UIC]
         │      │       │        │       │
         │      │       │        │       └─ Use Initial Conditions
         │      │       │        └── maks. krok wewnętrzny
         │      │       └── start zapisu wyników
         │      └── koniec analizy
         └── krok wynikowy (co ile wyświetlać)
```

### Zalecenia praktyczne

```
┌──────────────────────────────────────────────────────────────┐
│  ZALECENIE: TStep = TMax                                      │
│                                                                │
│  Dlaczego? Bez TMax, krok wewnętrzny może być                 │
│  DUŻO WIĘKSZY niż TStep i przeskoczyć szybkie zmiany:        │
│                                                                │
│  V(t)                                                          │
│   │    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲   ← prawdziwy przebieg                │
│   │  ○─────────○─────────○ ← co „widzi" SPICE (za rzadko!)  │
│   └──────────────────── t                                      │
│                                                                │
│  Rozwiązanie: .TRAN 1u 10m 0 1u                               │
│               TStep=1μs, TStop=10ms, TMax=1μs                 │
│                                                                │
│  Dobierz TStep tak, aby na okres sygnału                      │
│  przypadało 50-250 punktów.                                    │
│  Np. f = 1kHz → T = 1ms → TStep = 1ms/100 = 10μs            │
└──────────────────────────────────────────────────────────────┘
```

### Interpolacja wynikowa — ważne!

SPICE oblicza wyniki w **własnych** (nierównomiernych) punktach. Na koniec **interpoluje**
wielomianowo do punktów żądanych przez użytkownika (co TStep). Wyświetlone wartości
**nie są** bezpośrednimi wynikami obliczeń — to interpolacje!

---

## 10. Warunki początkowe (.IC vs .NODESET)

### Porównanie

```
┌──────────────────┬──────────────────────────────────────────────┐
│    .NODESET       │    .IC                                       │
│    "podpowiedź"   │    "wymuszenie"                              │
├──────────────────┼──────────────────────────────────────────────┤
│ Dodaje tymczasowe │ Wymusza napięcie na początku                 │
│ źródło → DC →     │ analizy TRAN (pomija DC)                    │
│ usuwa źródło →    │                                              │
│ prawdziwy DC      │ Wymaga flagi UIC w .TRAN                    │
├──────────────────┼──────────────────────────────────────────────┤
│ Wynik MOŻE BYĆ   │ Wynik JEST RÓWNY                             │
│ INNY niż podana  │ podanej wartości                             │
│ wartość           │                                              │
├──────────────────┼──────────────────────────────────────────────┤
│ .NODESET V(1)=5V │ C1 1 0 1nF IC=5V                            │
│                  │ .TRAN 1us 10us UIC                           │
│                  │ lub: .IC V(1)=5V                              │
└──────────────────┴──────────────────────────────────────────────┘
```

### Przykład wizualny

```
    Obwód RC bez źródła (R=1kΩ, C=1nF):

         węzeł 1
            │
          ┌─┤
          │ │
         R  C
          │ │
          └─┤
            │
           ═══

    Z .NODESET V(1)=5V:              Z .IC V(1)=5V:

    V(1)                              V(1)
    5V ┤                              5V ●
       │                                 │╲
    4V ┤                              4V ┤ ╲
       │                                 │  ╲
    3V ┤                              3V ┤   ╲
       │                                 │    ╲
    2V ┤                              2V ┤     ╲
       │                                 │      ╲
    1V ┤                              1V ┤        ╲───
       │                                 │
    0V ●────────────────              0V ┤
       └──┬──┬──┬──┬──              └──┬──┬──┬──┬──
         0  1μ 2μ 3μ                  0  1μ 2μ 3μ

    V=0 (bo DC bez źródła            V=5V → rozładowanie
         daje 0V na C)               eksponencjalne
```

---

# CZĘŚĆ II — ANALIZA WIDMOWA

## 11. Po co analiza widmowa?

### Problem

Masz sygnał w dziedzinie czasu. Chcesz wiedzieć, **z jakich częstotliwości się składa**.

```
    Dziedzina czasu:                    Dziedzina częstotliwości:

    V(t)                                |X(f)|
     │  ╱╲    ╱╲                         │
     │ ╱  ╲  ╱  ╲   ╱╲                  │  █
     │╱    ╲╱    ╲ ╱  ╲                  │  █ █
     │           ╲╱                      │  █ █
     │                                   │  █ █ █
     └────────────── t                   └──┬─┬─┬──── f
                                           f₁ f₂ f₃
     "co się dzieje w czasie"            "z jakich częstotliwości
                                          składa się sygnał"
```

**Zastosowania:**
- Zniekształcenia w wzmacniaczu (jakie harmoniczne się pojawiły?)
- Tłumienie sygnału przez filtr (która częstotliwość jest tłumiona?)
- Analiza zakłóceń EMC (skąd przychodzi szum?)

---

## 12. Ortogonalność — fundament analizy widmowej

### Intuicja — co to znaczy „ortogonalny"?

Dwa sygnały są ortogonalne, gdy **nie mają ze sobą nic wspólnego** — jeden nie zawiera
żadnej „domieszki" drugiego. Jak wektory prostopadłe w geometrii:

```
        y                           y
        │   ╱ a                     │
        │  ╱                        │  a = [2, 2]
        │╱                          │╱
        ┼────── x                   ┼──────── x
       ╱│                            ╲
      ╱ │                             b = [1, -1]
     b  │
                                    a · b = 2·1 + 2·(-1) = 0
     Wektory prostopadłe
     → iloczyn skalarny = 0         ORTOGONALNE!
```

### Ortogonalność sygnałów harmonicznych

Kluczowa własność: **sin i cos tej samej częstotliwości są ortogonalne**:

```
    sin(2πft)                cos(2πft)            sin × cos
     │  ╱╲                    │╲                   │  ╱╲
     │ ╱  ╲                   │ ╲   ╱╲             │ ╱  ╲
     │╱    ╲     ╱╲           │  ╲ ╱  ╲            │╱    ╲
    ─┼──────╲───╱──╲── t     ─┼───╲╱────── t      ─┼──────╲── t
     │       ╲ ╱    ╲         │   ╱╲               │       ╲╱
     │        ╲╱               │  ╱  ╲              │
     │                        │ ╱    ╲             │
                                                    ↑
                              Iloczyn = sygnał      Pole + = pole -
                              którego SUMA = 0!     → całka = 0
```

Podobnie: sin(f) i sin(2f) są ortogonalne, sin(f) i sin(3f) też, itd.

**To oznacza:** Jeśli sygnał składa się z wielu harmonicznych, można je **rozdzielić**
(każdą wyodrębnić osobno), bo nie „przeszkadzają" sobie nawzajem.

---

## 13. Transformata Fouriera — intuicja

### Jak działa — analogia do głosowania

Wyobraź sobie, że masz sygnał i chcesz sprawdzić, „ile" jest w nim częstotliwości f:

```
1. Wygeneruj sygnał odniesienia cos(2πft)
2. Pomnóż go przez badany sygnał (próbka po próbce)
3. Zsumuj wynik

Wysoka suma = sygnał ZAWIERA tę częstotliwość (korelacja!)
Niska suma  = sygnał NIE ZAWIERA tej częstotliwości

Powtórz dla wszystkich interesujących częstotliwości.
```

### Wzór transformaty Fouriera

```
X(f) = ∫ x(t) · e^(-j2πft) dt     (od -∞ do +∞)
```

Korzystając ze wzoru Eulera (e^(-jα) = cos α - j·sin α):

```
X(f) = ∫ x(t)·cos(2πft) dt  -  j · ∫ x(t)·sin(2πft) dt
       └────────────────────┘       └────────────────────┘
         część rzeczywista             część urojona
         (korelacja z cos)             (korelacja z sin)
```

### Co mówi wynik?

```
    X(f) = Re + j·Im = |X|·e^(jφ)

    |X(f)| = √(Re² + Im²)  → AMPLITUDA składowej o częstotliwości f
    φ(f)   = atan2(Im, Re)  → FAZA (przesunięcie) składowej
```

**Moduł** jest niezależny od fazy — nawet jeśli sygnał jest przesunięty w czasie,
amplituda widmowa się nie zmieni (zmieni się tylko faza).

---

## 14. Próbkowanie i twierdzenie Nyquista

### Próbkowanie — zamiana sygnału ciągłego na dyskretny

```
    Sygnał ciągły x_c(t):              Sygnał dyskretny x(n):

    V │  ╱╲  ╱╲                        V │  ●
      │ ╱  ╲╱  ╲  ╱╲                    │  │ ●
      │╱        ╲╱  ╲                    │  │ │●       ●
      │              ╲                   │● │ ││  ● ● │  ●
      └────────────── t                  ││ │ ││  │ │ │  │
                                         └┴─┴─┴┴──┴─┴─┴──── t
                                          ◄T_s►
    Ciągły (nieskończenie                Dyskretny (wartość znana
     wiele wartości)                      tylko co T_s sekund)
```

```
f_s = 1 / T_s   ← częstotliwość próbkowania [Hz] lub [Sa/s]
```

### Twierdzenie Nyquista-Shannona (najważniejsze twierdzenie!)

```
┌───────────────────────────────────────────────────────┐
│                                                       │
│    f_max  ≤  f_s / 2                                  │
│                                                       │
│    Maksymalna częstotliwość    Połowa częstotliwości   │
│    w sygnale                  próbkowania              │
│                               (= częstotliwość        │
│                                 Nyquista f_N)          │
│                                                       │
│    Żeby poprawnie „złapać" sygnał, trzeba             │
│    próbkować CO NAJMNIEJ 2 razy na okres!             │
└───────────────────────────────────────────────────────┘
```

**Intuicja:** Żeby zobaczyć sinusoidę, potrzebujesz minimum 2 próbki na okres:

```
    Wystarczająco (f_s = 4·f):       Za mało (f_s = 1.2·f):

    │  ●                              │         ●
    │ ╱│╲                             │        ╱ ╲
    │╱ │ ╲    ●                       │●      ╱   ╲         ●
    ┼──│──╲──╱│── t                   ┼ ╲    ╱     ╲      ╱
    │  │   ╲╱ │                       │  ╲  ╱       ╲   ╱
    │  │   ●  │                       │   ╲╱    ●    ╲╱
    │  │      │                       │              ↑
    4 próbki na okres                 Te próbki „widzą"
    → sygnał odtwarzalny             INNĄ częstotliwość! (aliasing)
```

---

## 15. Aliasing — co się psuje przy złym próbkowaniu

### Definicja

Gdy f_max > f_s/2, widma sąsiednich okresów **nakładają się** i **nie da się ich rozdzielić**:

```
    Poprawne próbkowanie (f_max < f_s/2):

    |X(f)|
     │   ╱╲          ╱╲          ╱╲
     │  ╱  ╲        ╱  ╲        ╱  ╲
     │ ╱    ╲      ╱    ╲      ╱    ╲
     └╱──────╲────╱──────╲────╱──────╲── f
    -f_s   -f_s/2   0   f_s/2    f_s

     Widma NIE nachodzą → OK


    Złe próbkowanie (f_max > f_s/2):

    |X(f)|
     │   ╱╲     ╱╲╱╲     ╱╲
     │  ╱  ╲   ╱ ╲╱ ╲   ╱  ╲
     │ ╱    ╲ ╱  ██  ╲ ╱    ╲
     └╱──────╲╱──██──╲╱──────── f
    -f_s   -f_s/2  0  f_s/2  f_s

     Widma NACHODZĄ → ██ = aliasing!
     Zafałszowane — NIEODWRACALNE!
```

### Przykład z życia — dźwięk

| Scenariusz | f_s | f_max | f_s/2 | Aliasing? |
|-----------|-----|-------|-------|-----------|
| CD audio | 44.1 kHz | 16 kHz | 22.05 kHz | NIE (16 < 22) |
| Telefon | 8 kHz | 16 kHz | 4 kHz | TAK! (16 > 4) |
| Telefon + filtr | 8 kHz | 3.5 kHz | 4 kHz | NIE (3.5 < 4) |

---

## 16. Dyskretna Transformata Fouriera (DFT)

### Od FT do DFT

W komputerze nie możemy policzyć całki od -∞ do +∞ z nieskończoną rozdzielczością.
Mamy **N próbek** i liczymy widmo w **N punktach** częstotliwości:

```
                 N-1
    X(m) =  Σ   x(n) · e^(-j2π·mn/N)      m = 0, 1, ..., N-1
                n=0
```

### Kluczowe parametry

```
┌──────────────────────────────────────────────────────────────────┐
│  N   = liczba próbek czasowych = liczba prążków widmowych       │
│  f_s = częstotliwość próbkowania = 1/T_s                        │
│                                                                  │
│  Δf  = f_s / N  ← ROZDZIELCZOŚĆ CZĘSTOTLIWOŚCIOWA               │
│                   (odległość między prążkami widma)               │
│                                                                  │
│  f_N = f_s / 2  ← CZĘSTOTLIWOŚĆ NYQUISTA                        │
│                   (maks. „widzialna" częstotliwość)              │
│                                                                  │
│  f_m = m · Δf   ← częstotliwość m-tego prążka                   │
│                                                                  │
│  Niezależnych prążków: N/2 (reszta to lustrzane odbicia)        │
└──────────────────────────────────────────────────────────────────┘
```

### Twierdzenie o symetrii

```
X(N-m) = X*(m)     (sprzężenie zespolone)

Prążki od 0 do N/2-1: niezależne
Prążki od N/2 do N-1: lustrzane odbicia → POMIJAMY
```

### Skalowanie amplitud (jak odczytać „prawdziwe" wartości)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Składowa stała (DC):     A_DC = |X(0)| / N                     │
│                                                                  │
│  Amplituda harmonicznej:  Amp_m = |X(m)| · 2/N    (m ≥ 1)      │
│                                                                  │
│  Wartość skuteczna:       A_sk  = |X(m)| · √2/N                 │
│                                                                  │
│  Widmo mocy:              P_m   = |X(m)|² · 2/N²                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 17. Przykład: DFT krok po kroku

### Sygnał

```
x(t) = 2 + 3·cos(2π·100·t)    ← składowa stała 2V + harmoniczna 3V przy 100 Hz
```

Próbkujemy: f_s = 1000 Hz (T_s = 1 ms), N = 10 próbek

### Parametry DFT

```
Δf = f_s / N = 1000/10 = 100 Hz    ← rozdzielczość
f_N = f_s / 2 = 500 Hz             ← maks. częstotliwość
```

### Próbki

```
n:    0     1     2     3     4     5     6     7     8     9
t:   0ms  1ms   2ms   3ms   4ms   5ms   6ms   7ms   8ms   9ms

x(n): 5.00  3.93  1.19  0.07  0.81  3.00  5.19  3.93  1.07  0.81

      (x = 2 + 3·cos(2π·100·n/1000) = 2 + 3·cos(2πn/10))
```

```
    x(n)
    5 ┤●              ●
      │ ╲            ╱ ╲        ●
    4 ┤  ●          ╱   ●
      │   ╲        ╱
    3 ┤    ╲   ●  ╱               ●
      │     ╲    ╱
    2 ┤      ╲  ╱
      │       ╲╱
    1 ┤    ●       ●
      │
    0 ┤  ●
      └──┬──┬──┬──┬──┬──┬──┬──┬──┬── n
         0  1  2  3  4  5  6  7  8  9
```

### Wynik DFT

| m | f_m | \|X(m)\| | A_DC lub Amp_m | Interpretacja |
|---|-----|---------|----------------|--------------|
| 0 | 0 Hz | 20 | 20/10 = **2.0 V** | Składowa stała ✓ |
| 1 | 100 Hz | 15 | 15·2/10 = **3.0 V** | Harmoniczna 100 Hz ✓ |
| 2 | 200 Hz | 0 | 0 | Brak |
| 3 | 300 Hz | 0 | 0 | Brak |
| 4 | 400 Hz | 0 | 0 | Brak |
| 5-9 | | (lustrzane) | (pomijamy) | Symetria |

```
    |X(m)| · 2/N
    3V ┤     █
       │     █
    2V ┤ █   █
       │ █   █
    1V ┤ █   █
       │ █   █
    0V ┤─█───█───────────────── f
       0Hz 100Hz 200Hz 300Hz 400Hz 500Hz

       DC   f₁   (nic więcej — sygnał miał tylko te 2 składowe)
```

Dokładnie odzyskaliśmy: A_DC = 2V, Amp przy 100Hz = 3V. DFT działa!

---

## 18. Przeciek widmowy (spectral leakage)

### Problem — co się dzieje gdy „nie trafimy" w częstotliwość

W przykładzie wyżej f_syg = 100 Hz = 1·Δf — **dokładnie** na prążku DFT. Co gdyby f_syg = 137 Hz?

```
137 Hz / 100 Hz = 1.37 — NIE jest liczbą całkowitą!
```

Wtedy energia sygnału **rozlewa się** na wiele prążków:

```
    Brak przecieku (f = 100 Hz = 1·Δf):     Przeciek (f = 137 Hz ≠ m·Δf):

    |X|                                       |X|
     │     █                                   │   █ █
     │     █                                   │ █ █ █ █
     │     █                                   │ █ █ █ █ █
     └─────┴────── f                           └─┴─┴─┴─┴─┴── f
          100 Hz                                   137 Hz
                                                    ↑
     Cała energia w JEDNYM prążku           Energia rozproszona
                                            na WIELE prążków!
```

### Dlaczego tak się dzieje?

DFT analizuje **fragment** sygnału — jakby wycinała go oknem prostokątnym.
Jeśli w tym fragmencie nie mieści się **całkowita** liczba okresów, na brzegach
pojawia się nieciągłość, która tworzy sztuczne składowe widmowe:

```
    Całkowita liczba okresów               Niecałkowita liczba okresów
    (brak przecieku):                      (PRZECIEK!):

    │╱╲  ╱╲  ╱╲  ╱╲│                      │╱╲  ╱╲  ╱╲  ╱╲ │
    │   ╲╱  ╲╱  ╲╱ │                      │   ╲╱  ╲╱  ╲╱ ╲ │
    │               │                      │              ↑  │
    └───────────────┘                      └──────────── SKOK!
    brzegi na tym samym                    brzegi na RÓŻNYM
    poziomie → ciągłość                    poziomie → nieciągłość
                                           → sztuczne harmoniczne
```

### Warunek braku przecieku

```
f_syg = m · Δf = m · f_s / N     (m — liczba całkowita)
```

Czyli w oknie próbkowania musi się zmieścić **całkowita** liczba okresów sygnału.

---

## 19. Okienkowanie — lekarstwo na przeciek

### Idea

Zamiast „twardego" okna prostokątnego, mnożymy sygnał przez **okno o łagodnych zboczach**:

```
    Okno prostokątne:                  Okno Hanninga (łagodne):

    │████████████████│                 │      ╱████╲      │
    │████████████████│                 │    ╱████████╲    │
    │████████████████│                 │  ╱████████████╲  │
    │████████████████│                 │╱████████████████╲│
    └────────────────┘                 └──────────────────┘
    Ostre krawędzie                    Łagodne zanikanie do zera
    → duży przeciek                    → mały przeciek
```

### Jak to działa?

```
    Sygnał × okno prostokątne:         Sygnał × okno Hanninga:

    │╱╲  ╱╲  ╱╲  ╱╲ │                 │    ╱╲  ╱╲  ╱╲    │
    │   ╲╱  ╲╱  ╲╱ ╲ │                 │  ╱    ╲╱  ╲╱  ╲  │
    │              ↑  │                 │╱              ╲│
    └──────────── SKOK!                └──────────────────┘
                                       Krawędzie ≈ 0 → brak skoku
    → DUŻY przeciek                    → mały przeciek
```

### Kompromis

Okienkowanie zmniejsza przeciek, ale:
- **Zmniejsza amplitudy** prążków (okno „osłabia" sygnał)
- **Pogarsza rozdzielczość** (prążki stają się szersze)

Popularne okna: **Hanning**, **Hamming**, **Blackman**, **Kaiser**

---

## 20. Ściąga na wejściówkę

### Modele stowarzyszone — szybki podgląd

```
┌─────────────────┬──────────────────────┬─────────────────────────┐
│     Metoda       │  Kondensator G_eq    │  Kondensator I_eq       │
├─────────────────┼──────────────────────┼─────────────────────────┤
│ Forward Euler   │      C/h             │  -(C/h)·v(t_n)          │
│ Backward Euler  │      C/h             │  -(C/h)·v(t_(n-1))     │
│ TRAPEZÓW        │     2C/h             │  -(2C/h)·v(t_(n-1))    │
│                 │                      │   - i_C(t_(n-1))        │
├─────────────────┼──────────────────────┼─────────────────────────┤
│     Metoda       │  Cewka G_eq          │  Cewka I_eq             │
├─────────────────┼──────────────────────┼─────────────────────────┤
│ Backward Euler  │      h/L             │  i_L(t_(n-1))           │
│ TRAPEZÓW        │     h/(2L)           │  i_L(t_(n-1))           │
│                 │                      │  + h/(2L)·v_L(t_(n-1))  │
└─────────────────┴──────────────────────┴─────────────────────────┘
```

### Algorytm zmiennokrokowy — kluczowe liczby

```
┌──────────────────────────────────────────────────┐
│  Pierwszy punkt:    t₁ = TStop / 50              │
│  Min krok:          Δt_min = TStop / (50·10⁹)   │
│  Skrócenie:         ÷ 8 (ośmiokrotne)           │
│  Wydłużenie:        × 2 (dwukrotne)             │
│  Zalecenie:         TStep = TMax                 │
│  Punktów na okres:  50 - 250                     │
└──────────────────────────────────────────────────┘
```

### Analiza widmowa — kluczowe wzory

```
┌──────────────────────────────────────────────────────────────┐
│  Rozdzielczość:     Δf = f_s / N                             │
│  Częst. Nyquista:   f_N = f_s / 2                            │
│  Tw. Nyquista:      f_max < f_s / 2  (warunek próbkowania)  │
│  Brak przecieku:    f_syg = m · Δf   (całkowite m)           │
│  Skalowanie DC:     A_DC = |X(0)| / N                        │
│  Skalowanie AC:     Amp = |X(m)| · 2/N                       │
│  Prążków niezal.:   N / 2                                    │
└──────────────────────────────────────────────────────────────┘
```

### 15 pytań i odpowiedzi

| # | Pytanie | Odpowiedź |
|---|---------|-----------|
| 1 | Wymień 4 metody całkowania | FE (niestabilna), BE (stabilna, rząd 1), TR (domyślna, rząd 2), Gear (BDF, rząd 2-6) |
| 2 | Która domyślna w SPICE? | Trapezów — najlepsza dokładność przy dobrej stabilności |
| 3 | Dlaczego nie FE? | Niestabilna — wynik oscyluje i rośnie |
| 4 | Kiedy Gear? | Równania sztywne (szybko+wolno jednocześnie) |
| 5 | G_eq kondensatora (TR)? | 2C/h |
| 6 | G_eq cewki (TR)? | h/(2L) |
| 7 | Jak zmienia się krok? | Skrócenie ÷8, wydłużenie ×2 |
| 8 | Co to aliasing? | Nakładanie widm przy f_max > f_s/2 (nieodwracalne!) |
| 9 | Tw. Nyquista? | f_max < f_s/2 |
| 10 | Co to przeciek DFT? | Rozlanie energii na wiele prążków gdy f ≠ m·Δf |
| 11 | Jak uniknąć przecieku? | f_syg = m·Δf lub okienkowanie |
| 12 | Ile prążków niezależnych? | N/2 (tw. o symetrii) |
| 13 | Amp z DFT? | \|X(m)\| · 2/N |
| 14 | .IC vs .NODESET? | IC = wymuszenie, NODESET = podpowiedź |
| 15 | Co to f_N? | f_s/2 — maks. częstotliwość bez aliasingu |
