# Laboratoria 2 — Badanie Algorytmów Analizy Czasowej i Widmowej

## Zagadnienia na wejściówkę

- Metody numeryczne analizy czasowej (4 metody) i ich właściwości
- Modele stowarzyszone (companion models) elementów reaktancyjnych
- Algorytm zmiennokrokowy
- Zjawiska towarzyszące analizie widmowej (aliasing, przeciek, okienkowanie)

---

## CZĘŚĆ I — ANALIZA CZASOWA

## 1. Problem analizy czasowej

Elementy reaktancyjne (C, L) opisane są równaniami różniczkowymi:

```
Kondensator:  i_C(t) = C · dv_C/dt
Cewka:        v_L(t) = L · di_L/dt
```

Aby rozwiązać obwód w dziedzinie czasu, trzeba **numerycznie scałkować** te równania. SPICE zamienia elementy reaktancyjne na ich **modele stowarzyszone** (companion models) — ekwiwalentne obwody złożone z rezystorów i źródeł, zależne od metody całkowania.

---

## 2. Cztery metody całkowania numerycznego

### 2.1 Metoda Eulera ekstrapolacyjna (Forward Euler — FE)

Przybliżenie pochodnej „w przód":

```
dv/dt ≈ (v(t_(n+1)) - v(t_n)) / h
```

gdzie h = Δt — krok czasowy.

Dla kondensatora:
```
i_C(t_(n+1)) = C · (v(t_(n+1)) - v(t_n)) / h
```

**Model stowarzyszony kondensatora (FE):**

```
Konduktancja zastępcza:  G_eq = C/h
Źródło prądowe:          I_eq = -C/h · v(t_n)
```

Schemat zastępczy: równoległe połączenie G_eq i źródła I_eq.

**Właściwości FE:**
- Metoda **jawna** (explicit) — nowa wartość obliczana wprost z poprzedniej
- **NIESTABILNA** — może dawać rosnące oscylacje
- **Nie stosowana w SPICE** z powodu niestabilności
- Rząd dokładności: 1 (błąd ~ h)

### 2.2 Metoda Eulera interpolacyjna (Backward Euler — BE)

Przybliżenie pochodnej „wstecz":

```
dv/dt ≈ (v(t_n) - v(t_(n-1))) / h
```

Dla kondensatora:
```
i_C(t_n) = C · (v(t_n) - v(t_(n-1))) / h
```

**Model stowarzyszony kondensatora (BE):**

```
G_eq = C/h
I_eq = -C/h · v(t_(n-1))    ← wartość z POPRZEDNIEGO kroku
```

**Model stowarzyszony cewki (BE):**

```
G_eq = h/L
I_eq = i_L(t_(n-1))         ← prąd z poprzedniego kroku
```

**Właściwości BE:**
- Metoda **niejawna** (implicit) — wymaga rozwiązania układu równań
- **Zawsze stabilna** (bezwarunkowo)
- **Najmniej dokładna** ze stabilnych metod
- Rząd dokładności: 1 (błąd ~ h)
- Nie stosowana w IsSpice 4 (ale stosowana w innych wersjach SPICE)

### 2.3 Metoda trapezów (Trapezoidal Rule — TR)

Przybliżenie całki jako średnia arytmetyczna pochodnych na końcach przedziału:

```
v(t_n) = v(t_(n-1)) + h/2 · [dv/dt|_(t_n) + dv/dt|_(t_(n-1))]
```

Dla kondensatora:
```
i_C(t_n) = 2C/h · v(t_n) - 2C/h · v(t_(n-1)) - i_C(t_(n-1))
```

**Model stowarzyszony kondensatora (TR):**

```
G_eq = 2C/h
I_eq = -2C/h · v(t_(n-1)) - i_C(t_(n-1))
```

**Model stowarzyszony cewki (TR):**

```
G_eq = h/(2L)
I_eq = i_L(t_(n-1)) + h/(2L) · v_L(t_(n-1))
```

**Właściwości TR:**
- Metoda **niejawna**
- **Stabilna** (jeśli krok nie jest zbyt duży)
- **Najdokładniejsza** spośród metod prostych (rząd 2)
- **Domyślna metoda w IsSpice 4 / PSpice**
- Największa wydajność obliczeniowa w większości przypadków
- Rząd dokładności: 2 (błąd ~ h²)
- Wada: może generować **oscylacje numeryczne** dla skokowych wymuszeń

### 2.4 Metody Geara (BDF — Backward Differentiation Formulas)

Pochodna przybliżana za pomocą wielu poprzednich punktów:

**Gear rząd 2:**
```
dv/dt ≈ (3v(t_n) - 4v(t_(n-1)) + v(t_(n-2))) / (2h)
```

W IsSpice 4 stosuje się algorytmy Geara rzędów od 2 do 6.

**Właściwości Geara:**
- Metoda **niejawna**
- **Zawsze stabilna** (bezwarunkowo) — to główna zaleta
- Skuteczniejsza od metody trapezów w przypadku **równań sztywnych** (stiff equations)
- Mogą pracować z **dłuższym krokiem** niż metoda trapezów
- Rząd dokładności: zależy od rzędu (2-6)

---

## 3. Porównanie metod — tabela

| Metoda | Rząd | Stabilność | Dokładność | Stosowana w SPICE? |
|--------|------|-----------|------------|-------------------|
| Euler ekstrapolacyjny (FE) | 1 | NIEstabilna | Niska | NIE |
| Euler interpolacyjny (BE) | 1 | Bezwarunkowa | Niska | Rzadko |
| **Trapezów (TR)** | **2** | **Warunkowa** | **Wysoka** | **TAK (domyślna)** |
| Geara (BDF) | 2-6 | Bezwarunkowa | Średnia-Wysoka | TAK (rów. sztywne) |

---

## 4. Algorytm zmiennokrokowy (Variable Time Step)

SPICE **nie stosuje** stałego kroku czasowego. Krok jest dynamicznie dostosowywany do szybkości zmian w obwodzie.

### Pierwszy punkt czasowy

```
t_1 = TStop / 50
```

### Mechanizm zmiany kroku

- **Skrócenie kroku:** program cofa się do poprzedniego punktu i zmniejsza krok **8-krotnie** (÷8). Może skracać aż do Δt_min.
- **Wydłużenie kroku:** krok zwiększany jest **2-krotnie** (×2). Może wydłużać aż do Δt_max.

### Limity kroku

**Minimalny krok:**
```
Δt_min = TStop / (50 · 10⁹)
```

**Maksymalny krok** (zależy od metody):
- Metoda zliczania iteracji: Δt_max = TStep
- Metoda błędu obcięcia: Δt_max = TStop / 50

### Trzy wskaźniki sterujące zmianą kroku

1. **Dynamika zmian napięć/prądów** — główny wskaźnik:
   - Monitoring liczby iteracji N-R w każdym punkcie (ITL3/ITL4)
   - Monitoring **lokalnego błędu obcięcia** (LTE)
2. **Brak zbieżności** — jeśli N-R nie zbiega w ITL4 iteracjach → skrócenie kroku
3. **Punkty załamania** — skokowe zmiany sygnałów źródłowych wymuszają zagęszczenie punktów

### Parametry instrukcji .TRAN

```
.TRAN TStep TStop [TStart [TMax]] [UIC]
```

- **TStep** — krok wynikowy (odstęp między punktami wyjściowymi)
- **TStop** — czas końcowy analizy
- **TStart** — czas początkowy zapisu wyników (domyślnie 0)
- **TMax** — maksymalny wewnętrzny krok czasowy
- **UIC** — Use Initial Conditions (pomiń analizę DC, użyj .IC)

### Zalecenie: TStep = TMax

Aby uniknąć zafałszowania wyników (zbyt duży krok przeskakujący szybkie zmiany), zaleca się:
```
TStep = TMax
```
i dobierać TStep tak, aby na przewidywany okres zmienności przypadało **50-250 punktów**.

### Interpolacja wynikowa

Wewnętrznie SPICE oblicza odpowiedź w punktach wyznaczonych przez algorytm zmiennokrokowy. Po zakończeniu analizy, **metodą interpolacji wielomianowej** oblicza wartości w punktach żądanych przez użytkownika (co TStep).

---

## 5. Warunki początkowe analizy czasowej

### Domyślnie

SPICE najpierw wykonuje **analizę DC** (punkt pracy), traktując:
- Kondensatory → rozwarcie
- Cewki → zwarcie

Wyznaczony punkt pracy jest warunkiem początkowym analizy TRAN.

### .IC V(n) = wartość

Wymusza napięcie początkowe na kondensatorze/węźle. Stosowane z flagą **UIC** w .TRAN:
```
C1 0 1 1nF IC=5V
.TRAN 1us 10us UIC
```

### .NODESET V(n) = wartość

Tylko podpowiedź dla punktu startowego DC. Program dodaje tymczasowe źródło, znajduje punkt pracy, usuwa źródło. Wynik **nie musi** być równy podanej wartości.

### Różnica .NODESET vs .IC — przykład

Obwód RC (R=1kΩ, C=1nF) bez źródła:
- **.NODESET V(1)=5V** → analiza DC daje V(1)=0V (brak źródła → kondensator rozładowany) → analiza TRAN startuje od 0V
- **.IC V(1)=5V** → analiza TRAN startuje od **5V** (wymuszony warunek) → obserwujemy rozładowanie kondensatora

---

## 6. Algorytm programu SPICE — analiza czasowa (schemat blokowy)

```
START
  │
  ▼
Wybór startowego punktu pracy (DC)
  │
  ▼
┌─────────────────────────────────────────┐
│ Utworzenie/aktualizacja modeli           │◄──────────┐
│ zastępczych elementów nieliniowych       │           │
│            ▼                             │           │
│ Utworzenie/aktualizacja liniowych         │           │
│ modeli stowarzyszonych (companion)       │           │
│            ▼                             │           │
│ Wypełnienie równania G·V = I             │           │
│            ▼                             │           │
│ Rozwiązanie układu równań                │           │
│            ▼                             │           │
│ Czy osiągnięto zbieżność?───NIE─────────┘           │
│            │                                          │
│           TAK                                         │
│            ▼                                          │
│ Wybór kroku czasowego                                 │
│ Wyznaczenie kolejnego punktu                          │
│            ▼                                          │
│ Czy koniec czasu analizy?───NIE──────────────────────┘
│            │
│           TAK
│            ▼
│          STOP
└───────────────────────────────────────────┘
```

---

## CZĘŚĆ II — ANALIZA WIDMOWA

## 7. Reprezentacja widmowa sygnału

### Motywacja

Parametry dziedziny czasu (amplituda, okres, wartość średnia) nie opisują w pełni przebiegu. Alternatywą jest rozkład na **składowe harmoniczne** — suma sinusoid i cosinusoid o różnych częstotliwościach.

### Dlaczego sygnały harmoniczne?

1. **"Natura nie lubi kantów"** — sygnały fizyczne są gładkie
2. **Unikalna własność** przy różniczkowaniu i całkowaniu (pochodna sinusoidy = sinusoida)
3. **Ortogonalność** — odpowiednio dobrane funkcje harmoniczne tworzą bazę ortonormalną

---

## 8. Ortogonalność sygnałów

Dwa sygnały są **ortogonalne** (prostopadłe), jeśli ich iloczyn skalarny wynosi zero.

**Iloczyn skalarny sygnałów dyskretnych:**
```
<x, y> = Σ x_i · y_i   (dla i = 1..N)
```

**Iloczyn skalarny sygnałów ciągłych:**
```
<x(t), y(t)> = ∫ x(t) · y(t) dt   (od -∞ do +∞)
```

### Ortogonalność funkcji harmonicznych

```
<sin(2πft), cos(2πft)> = ∫ sin(2πft)·cos(2πft) dt = 0
```

Sin i cos tej samej częstotliwości są **zawsze ortogonalne**.

```
<sin(2πft), sin(2·2πft)> = 0
```

Sinusy (lub cosinusy) o **różnych** częstotliwościach harmonicznych również są ortogonalne.

---

## 9. Przekształcenie Fouriera

### Transformata ciągła (FT)

```
X_c(f) = ∫ x_c(t) · e^(-j2πft) dt   (od -∞ do +∞)
```

Korzystając ze wzoru Eulera (e^(jα) = cos α + j sin α):

```
X_c(f) = ∫ x_c(t)·cos(2πft) dt - j ∫ x_c(t)·sin(2πft) dt
```

### Interpretacja

- **Część rzeczywista** Re{X_c(f)} — korelacja sygnału z cos(2πft)
- **Część urojona** Im{X_c(f)} — korelacja sygnału z sin(2πft)
- **Moduł** |X_c(f)| — amplituda składowej o częstotliwości f (niezależna od fazy)
- **Faza** arg{X_c(f)} — przesunięcie fazowe składowej

### Warunki istnienia (Dirichleta)

Sygnał musi być **bezwzględnie całkowalny**: ∫|x_c(t)|dt < ∞

Sygnały okresowe (cos, sin, 1(t)) **nie spełniają** tego warunku — stosuje się transformatę w sensie granicznym.

---

## 10. Sygnał dyskretny i próbkowanie

### Dystrybucja Diraca

```
δ(t) = { ∞  dla t = 0
        { 0  dla t ≠ 0       ∫δ(t)dt = 1
```

Własność próbkowania: x(t)·δ(t) = x(0)·δ(t)

Własność filtracji: ∫x(t)·δ(t-τ)dt = x(τ)

### Próbkowanie sygnału

Spróbkowana wersja x(t) sygnału ciągłego x_c(t):

```
x(t) = x_c(t) · σ(t) = Σ x_c(nT_s) · δ(t - nT_s)
```

gdzie T_s — okres próbkowania, f_s = 1/T_s — częstotliwość próbkowania.

### Kwantowanie amplitudy

Sygnał cyfrowy ma skwantowaną amplitudę:
```
Liczba poziomów kwantyzacji = 2^n = R/q
```
gdzie n — liczba bitów, R — zakres, q — krok kwantyzacji.

---

## 11. Dyskretna Transformata Fouriera (DFT)

### Własności widma sygnału dyskretnego

- Widmo jest **ciągłe i okresowe** z okresem f_s
- Tylko **pierwsza połowa** widma (do f_s/2) niesie niezależną informację

### Twierdzenie o próbkowaniu (Nyquist-Shannon-Kotelnikow)

```
f_max ≤ f_s / 2
```

Maksymalna częstotliwość sygnału nie może przekraczać **połowy częstotliwości próbkowania** (częstotliwość Nyquista: f_N = f_s/2).

### Aliasing

Jeśli f_max > f_s/2, widma sąsiednich okresów **nakładają się** — powstaje **aliasing** (fałszywe składowe widmowe). Zjawisko **nieodwracalne**.

Przykład audio: f_s = 44.1 kHz, f_max = 16 kHz → OK (f_max < 22.05 kHz)

### Definicja DFT

Dla ciągu N próbek x(n), n = 0, 1, ..., N-1:

```
X(m) = Σ x(n) · e^(-j2π·mn/N)    dla n = 0..N-1
```

Rozpisując ze wzoru Eulera:

```
X(m) = Σ x(n) · [cos(2π·mn/N) - j·sin(2π·mn/N)]
```

### Parametry DFT

- **N** — liczba próbek (w obu dziedzinach)
- **f_1 = Δf = f_s / N** — rozdzielczość częstotliwościowa (pierwsza harmoniczna)
- **T_1 = N · T_s** — okres pierwszej harmonicznej = czas trwania sygnału
- **m** — numer prążka widmowego (m = 0, 1, ..., N-1)
- **f_m = m · Δf** — częstotliwość m-tego prążka

### Twierdzenie o symetrii

```
X(N-m) = X*(m)     (sprzężenie zespolone)
```

Tylko pierwszych **N/2** prążków jest niezależnych (do częstotliwości Nyquista f_N = f_s/2).

---

## 12. Amplituda DFT — skalowanie

### Składowa stała (DC)

```
X(0) = Σ x(n) = x_śr · N    →    A_DC = X(0) / N
```

### Składowa harmoniczna (m > 0)

Jeśli sygnał zawiera harmoniczną o amplitudzie Amp_m i częstotliwości f_syg = m·Δf:

```
X(m) = Amp_m · N/2
```

**Skalowanie do amplitud fizycznych:**

```
A_DC = X_0 · (1/N)                    ← składowa stała
Amp_m = X_m · (2/N)    dla m ≥ 1      ← amplitudy harmonicznych
```

**Wartości skuteczne:**
```
A_sk_m = X_m · √2 / N
```

**Widmo mocy:**
```
P_DC = X_0² / N²
P_m = X_m² · 2/N²
```

---

## 13. Przeciek DFT (spectral leakage)

### Problem

Jeśli częstotliwość sygnału **nie jest** dokładnie wielokrotnością Δf (tzn. f_syg ≠ m·Δf), energia sygnału „przecieka" do **wszystkich** prążków widma.

### Przyczyna

DFT analizuje tylko **fragment** sygnału ograniczony oknem prostokątnym. Iloczyn sygnału z oknem prostokątnym w dziedzinie czasu = splot ich widm w dziedzinie częstotliwości. Widmo okna prostokątnego to funkcja **sinc** o szerokich listkach bocznych.

### Funkcja sinc

```
sinc(α) = sin(α)/α   dla α ≠ 0
sinc(0) = 1
```

Amplituda m-tego prążka: X(m) = A_syg · (N/2) · sinc[(k-m)π]

- Gdy k-m jest liczbą całkowitą → sinc = 0 dla wszystkich m ≠ k → **brak przecieku**
- Gdy k-m nie jest całkowite → sinc ≠ 0 → **przeciek do wielu prążków**

### Jak uniknąć przecieku?

1. **Dobrać N i f_s tak, aby f_syg = m·Δf** (całkowita liczba okresów w oknie)
2. Zastosować **okienkowanie** (windowing)

---

## 14. Okienkowanie (windowing)

### Idea

Zamiast okna prostokątnego (ostre krawędzie → duży przeciek), mnożymy sygnał przez funkcję **okna o łagodnych zboczach** (Hanning, Hamming, Blackman itp.).

Okno powoduje, że wartości sygnału na krańcach przedziału dążą do zera → mniejsza nieciągłość → węższe listki boczne funkcji sinc → **mniejszy przeciek**.

### Koszt

Okienkowanie **redukuje moc sygnału** i zmniejsza amplitudy prążków widma (wymaga kompensacji).

---

## 15. Analiza widmowa w SPICE — deklaracja .FOUR

```
.FOUR częstotliwość_podstawowa V(węzeł)
```

SPICE oblicza DFT z wyników analizy .TRAN i podaje amplitudy oraz fazy kolejnych harmonicznych.

---

## 16. Podsumowanie kluczowych zależności

| Wielkość | Wzór | Znaczenie |
|----------|------|-----------|
| Rozdzielczość częstotliwościowa | Δf = f_s / N = 1 / (N·T_s) | Odległość między prążkami |
| Częstotliwość Nyquista | f_N = f_s / 2 | Maks. analizowalna częstotliwość |
| Warunek braku aliasingu | f_max < f_s / 2 | Twierdzenie o próbkowaniu |
| Warunek braku przecieku | f_syg = m · Δf | Całkowita liczba okresów w oknie |
| Pierwszy punkt czasowy SPICE | t_1 = TStop / 50 | Start algorytmu zmiennokrokowego |
| Min. krok czasowy | Δt_min = TStop / (50·10⁹) | Dolny limit kroku |
| Skrócenie kroku | ÷ 8 | Cofnięcie + 8× mniejszy krok |
| Wydłużenie kroku | × 2 | Podwojenie kroku |

---

## 17. Typowe pytania na wejściówkę

1. **Wymień 4 metody całkowania numerycznego i podaj ich właściwości (stabilność, dokładność)**
2. **Która metoda jest domyślna w SPICE i dlaczego?** (Trapezów — najlepsza dokładność przy stabilności)
3. **Dlaczego metoda Eulera ekstrapolacyjna nie jest stosowana w SPICE?** (Niestabilna)
4. **Kiedy stosuje się metody Geara zamiast trapezów?** (Równania sztywne)
5. **Narysuj model stowarzyszony kondensatora dla metody trapezów** (G_eq = 2C/h, I_eq)
6. **Jak działa algorytm zmiennokrokowy? Ile razy zmniejsza/zwiększa krok?** (÷8 / ×2)
7. **Co to jest TStep, TStop, TMax? Jaki jest zalecany stosunek TStep do TMax?** (TStep = TMax)
8. **Co to jest aliasing? Podaj warunek jego uniknięcia** (f_max < f_s/2)
9. **Co to jest przeciek DFT? Kiedy nie występuje?** (Gdy f_syg = m·Δf)
10. **Jak okienkowanie wpływa na widmo?** (Redukuje przeciek, ale zmniejsza amplitudy)
11. **Ile niezależnych prążków widma daje N-punktowe DFT?** (N/2)
12. **Jak przeskalować wynik DFT do amplitudy fizycznej?** (Amp_m = X_m · 2/N)
13. **Co oznacza Δt_min = TStop/(50·10⁹)?** (Minimalny krok algorytmu zmiennokrokowego)
14. **Jaka jest różnica między .IC a .NODESET w kontekście analizy TRAN?**
15. **Co to jest częstotliwość Nyquista?** (f_N = f_s/2 — maks. częstotliwość reprezentowalna)
