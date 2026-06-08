# Module 2 — Electrical Calculations

*Part of the [MV/LV ~2 MW Process Plant training course](../README.md). Diagram:
[master single-line diagram](../diagrams/sld-master-2MW.md). Basis of design:
[reference design document](../docs/main-electrical-equipment-2MW-process-plant.md).*

> All ratings and figures in this module are **indicative and tentative** — they
> illustrate method and typical practice, not a substitute for project-specific
> load lists, short-circuit/load-flow studies and the governing standards.

---

## Introduction

This module works through the **core electrical calculations** for the ~2 MW
plant identified in [Module 1](module-01-equipment-identification.md). Each
calculation follows the same pattern: **formula → substitution → result with
units**, with assumptions stated up front. Numbers are kept internally
consistent with the basis of design: ~2 MW demand, 11 kV / 400 V, 50 Hz,
**2 × 1600 kVA** (Dyn11, **Z ≈ 6 %**) transformers on a split LV bus.

### Learning outcomes

On completion you will be able to:

- Build a **demand / diversity** estimate and convert plant load (MW → MVA).
- Justify and size the **2 × 1600 kVA** transformers, including the **N-1** check
  via the bus-tie.
- Compute **full-load current** and **transformer secondary short-circuit
  current** from the impedance.
- Size a **motor feeder** (FLC, DOL starting, soft-start/VFD rationale).
- Size a **cable** with derating and a **voltage-drop** check.
- Size **power-factor correction** (0.85 → 0.95) and the **standby generator**.

**Constants used throughout:** √3 = 1.732; LV line voltage V = 400 V; MV line
voltage = 11 kV; 50 Hz.

---

## 1. Load & demand estimate

**Goal:** confirm the ~2 MW plant demand and convert it to apparent power (MVA).

**Assumptions.** Sum of connected loads (nameplate) ≈ 2.7 MW; overall demand
(diversity) factor ≈ 0.75; overall power factor before correction = 0.85.

**Demand (active power):**

```
P_demand = Σ P_connected × demand factor
P_demand = 2.7 MW × 0.75 = 2.025 MW ≈ 2.0 MW
```

**Apparent power:**

```
S = P / pf
S = 2.0 MW / 0.85 = 2.35 MVA
```

**Result:** maximum demand ≈ **2.0 MW**, **2.35 MVA** at 0.85 pf — consistent
with the design basis. Adding a diversity/spare margin of +20–25 % gives an
installed transformer base of ~**2.8–3.0 MVA**, which drives the 2 × 1600 kVA
selection in §2.

---

## 2. Transformer sizing & loading (and the N-1 check)

**Goal:** explain why **2 × 1600 kVA** and verify one transformer can carry the
essential load via the [bus-tie](../diagrams/sld-master-2MW.md#bt).

**Why 2 × 1600 kVA.** Installed base ~2.8–3.0 MVA split into two equal units for
redundancy → 2 × 1600 kVA = 3200 kVA installed. Two units (rather than one
3150 kVA) give a split bus and N-1 capability.

**Normal per-unit loading** (load shared across both
[TX-1](../diagrams/sld-master-2MW.md#tx-1) /
[TX-2](../diagrams/sld-master-2MW.md#tx-2), each carrying ~half):

```
S_per_tx (normal) = 2.35 MVA / 2 = 1.175 MVA
Loading = 1.175 / 1.6 = 0.73 pu  → ~73 %
```

**N-1 check.** One transformer lost; the bus-tie closes; the survivor carries
the whole plant:

```
Loading (N-1, full load) = 2.35 MVA / 1.6 MVA = 1.47 pu → 147 %  ✗ (continuous)
```

147 % is too high to run continuously, so on N-1 the plant **sheds
non-essential load**. Essential load is typically ~50–60 % of total:

```
S_essential ≈ 0.55 × 2.35 = 1.29 MVA
Loading (N-1, essential) = 1.29 / 1.6 = 0.81 pu → ~81 %  ✓
```

**Result:** each transformer runs at ~**73 %** in normal operation; on loss of
one source the bus-tie lets the survivor carry the **essential load at ~81 %**
(within rating), with non-essential load shed. The 2 × 1600 kVA + bus-tie design
is therefore **N-1 secure for essential load**.

---

## 3. Transformer full-load current (LV side)

**Goal:** the 400 V full-load current (FLC) of a 1600 kVA transformer — the basis
for incomer ACB and busbar rating.

**Formula:**

```
I_fl = S / (√3 × V)
```

**Substitution (1600 kVA at 400 V):**

```
I_fl = 1,600,000 VA / (1.732 × 400 V)
I_fl = 1,600,000 / 692.8 = 2310 A
```

**Result:** **I_fl ≈ 2310 A** per transformer at 400 V. This sets the
[LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) incomer ACB (≥2500 A frame) and
the ~2500–3200 A bus rating noted in the design basis.

*(For reference, the 11 kV primary FLC = 1,600,000 / (1.732 × 11,000) ≈ **84 A**,
sizing the MV transformer-feeder breakers `[52-T1]`/`[52-T2]`.)*

---

## 4. Transformer short-circuit / fault contribution

**Goal:** the LV symmetrical short-circuit current from the transformer, to
confirm the [LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) withstand rating.

**Assumption.** Z = 6 %; infinite upstream MV source (conservative — ignores MV
source impedance, so the real value is slightly lower).

**Formula:**

```
I_sc = I_fl / Z(pu)
```

**Substitution (per transformer):**

```
I_sc = 2310 A / 0.06 = 38,500 A ≈ 38.5 kA
```

**Two transformers in parallel** (bus-tie closed — bounding case for the bus):

```
I_sc (both) ≈ 2 × 38.5 kA = 77 kA  (upper bound, ignoring source/cable Z)
```

**Result:** ~**38.5 kA** from a single transformer; the bus must withstand the
parallel case. Selecting [LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) and
the MCC bus at **50–65 kA** covers the single-transformer fault with margin; the
**bus-tie is operated normally-open** (and interlocked) so the two contributions
are not summed continuously, keeping fault duty within the 50–65 kA board rating.

---

## 5. Motor full-load current & starting

**Goal:** FLC and starting current of a representative LV motor, and why
soft-start / [VFD](../diagrams/sld-master-2MW.md#vfd) is used.

**Example motor.** P = 110 kW, 400 V, pf = 0.86, efficiency η = 0.95.

**Full-load current:**

```
I_fl = P / (√3 × V × pf × η)
I_fl = 110,000 / (1.732 × 400 × 0.86 × 0.95)
I_fl = 110,000 / 566 = 194 A
```

**DOL starting current (≈ 6.5 × FLC):**

```
I_start (DOL) = 6.5 × 194 A = 1260 A
```

**Result:** FLC ≈ **194 A**; DOL inrush ≈ **1260 A**. A ~1260 A surge causes
voltage dip on the bus, mechanical/electrical stress and possible nuisance trips.
A **soft-starter** cuts this to ~3× FLC (~580 A); a **VFD** limits starting
current to near FLC **and** gives speed control. For this reason motors above
~55 kW are typically soft-started or driven by a VFD in the
[MCC](../diagrams/sld-master-2MW.md#mcc-1).

**LV→MV threshold.** Individual motors larger than ~**150–200 kW** are often more
economically fed at **MV (3.3 / 6.6 kV)** via a dedicated MV starter rather than
the 400 V MCC — the LV FLC becomes large (a 200 kW LV motor draws ~350 A) and
cable/starter cost rises. Our 110 kW example sits comfortably below that line.

---

## 6. Cable sizing (one worked feeder)

**Goal:** size and check the feeder cable for the 110 kW motor of §5.

**Step 1 — design (base) current.** Feeder must carry the motor FLC:

```
I_B = 194 A
```

**Step 2 — derating.** Installation factors (IEC 60364):

```
k_grouping = 0.80 (cables grouped on tray)
k_temp     = 0.94 (40 °C ambient)
k_total    = 0.80 × 0.94 = 0.752
Required tabulated rating  I_z(req) = I_B / k_total = 194 / 0.752 = 258 A
```

**Step 3 — size selection.** Choose a cable whose tabulated rating ≥ 258 A.
A **95 mm² Cu XLPE** (≈ 264–300 A on tray, per manufacturer/IEC tables) satisfies
`I_z ≥ 258 A`. (Confirm against the actual installation table.)

**Step 4 — voltage-drop check.** Run length L = 120 m; for 95 mm² Cu take
R ≈ 0.23 Ω/km, X ≈ 0.08 Ω/km; pf = 0.86 → cosφ = 0.86, sinφ = 0.51.

```
ΔV = √3 × I × (R·cosφ + X·sinφ) × L
ΔV = 1.732 × 194 × (0.23×0.86 + 0.08×0.51) × 0.120
ΔV = 1.732 × 194 × (0.1978 + 0.0408) × 0.120
ΔV = 1.732 × 194 × 0.2386 × 0.120 = 9.6 V

%ΔV = 9.6 / 400 × 100 = 2.4 %
```

**Result:** **95 mm² Cu XLPE**, 2.4 % drop at full load — within the typical
**≤5 %** motor-feeder limit (and ≤3 % is comfortable). Selection accepted.

---

## 7. Power-factor correction (PFC)

**Goal:** size the [PFC](../diagrams/sld-master-2MW.md#pfc) bank to move the plant
from 0.85 → 0.95.

**Formula:**

```
Q_c = P × (tanφ1 − tanφ2)
```

**Substitution (P = 2.0 MW; pf1 = 0.85 → φ1 = 31.8°; pf2 = 0.95 → φ2 = 18.2°):**

```
tanφ1 = tan(31.8°) = 0.620
tanφ2 = tan(18.2°) = 0.329
Q_c = 2000 kW × (0.620 − 0.329) = 2000 × 0.291 = 582 kVAr
```

**Result:** ~**580 kVAr** (select a standard ~600 kVAr automatic bank in steps).
Because VFDs inject harmonics, the bank is **detuned (7 % reactors)** to avoid
resonance — as noted for the [PFC](../diagrams/sld-master-2MW.md#pfc) tag.
Correcting to 0.95 also drops the apparent power (2.35 → 2.0/0.95 = 2.11 MVA),
relieving transformer and cable loading.

---

## 8. Standby generator sizing rationale

**Goal:** justify the [DG](../diagrams/sld-master-2MW.md#dg) rating (~1000 kVA)
on an essential-load basis.

**Assumptions.** The DG covers essential loads only (not the full 2 MW):
essential active load ≈ 0.65 MW at pf 0.8.

**Running (steady) demand:**

```
S_essential = P / pf = 0.65 MW / 0.8 = 0.81 MVA
```

**Step-load / starting allowance.** The largest essential motor must start
against the generator's limited fault capacity, causing a transient kVA demand
and voltage dip. Allow headroom for the worst-case motor start (~25–30 % above
running):

```
S_DG ≥ S_essential × 1.25 = 0.81 × 1.25 = 1.01 MVA
```

**Result:** select a **~1000 kVA** standby DG — matching the design basis. Final
sizing must check the transient **voltage dip** on the largest motor start (often
the governing constraint), step-load acceptance, and de-rating for altitude/
ambient. Soft-starting/VFD the largest essential motors reduces the required
generator size.

---

## Formula reference summary

| Quantity | Formula | This-plant example |
|----------|---------|--------------------|
| Apparent power | S = P / pf | 2.0 MW / 0.85 = 2.35 MVA |
| 3-phase current | I = S / (√3·V) | 1600 kVA @ 400 V → 2310 A |
| Transformer loading | S_load / S_rated (pu) | 1.175 / 1.6 = 0.73 pu |
| Short-circuit current | I_sc = I_fl / Z(pu) | 2310 / 0.06 = 38.5 kA |
| Motor FLC | I = P / (√3·V·pf·η) | 110 kW → 194 A |
| DOL starting current | I_start ≈ 6–7 × I_fl | 6.5 × 194 = 1260 A |
| Cable derating | I_z(req) = I_B / (k_g·k_t) | 194 / 0.752 = 258 A |
| Voltage drop | ΔV = √3·I·(R cosφ + X sinφ)·L | 9.6 V = 2.4 % |
| PFC reactive power | Q_c = P·(tanφ1 − tanφ2) | 2000·0.291 = 582 kVAr |
| Generator (essential) | S = P/pf × step factor | 0.81 × 1.25 = 1.0 MVA |

---

## Self-check problems

Work each before opening the answer.

1. A second LV motor is rated **75 kW**, 400 V, pf 0.85, η 0.94. Find its FLC and
   its DOL starting current (use 6.5×).
2. A **1250 kVA** transformer has Z = 6 %. Find its 400 V FLC and secondary
   short-circuit current.
3. Re-correct the plant from **0.85 → 0.93** (instead of 0.95). How much kVAr is
   now needed (P = 2.0 MW)?
4. With one transformer out, the bus-tie carries **1.3 MVA** of essential load on
   a 1600 kVA unit. What is the per-unit loading — is it acceptable?
5. A feeder carries **I_B = 160 A** with grouping/temperature derating factors of
   0.85 and 0.91. What tabulated cable rating I_z is required?

<details>
<summary><strong>Answers</strong></summary>

1. FLC = 75,000 / (1.732 × 400 × 0.85 × 0.94) = 75,000 / 553 = **136 A**;
   DOL = 6.5 × 136 = **882 A**.
2. FLC = 1,250,000 / (1.732 × 400) = **1804 A**;
   I_sc = 1804 / 0.06 = **30.1 kA**.
3. pf2 = 0.93 → φ2 = 21.6°, tanφ2 = 0.396; tanφ1 = 0.620.
   Q_c = 2000 × (0.620 − 0.396) = 2000 × 0.224 = **448 kVAr** (~450 kVAr bank).
4. Loading = 1.30 / 1.60 = **0.81 pu (81 %)** — within continuous rating, so
   **acceptable** for the essential-load N-1 case (non-essential load shed).
5. I_z(req) = 160 / (0.85 × 0.91) = 160 / 0.7735 = **207 A** — select a cable
   with tabulated rating ≥ 207 A.

</details>

---

*Next: [Module 3 — Single Points of Failure (SPOF) Analysis](module-03-spof-analysis.md).
Every figure here is indicative and to be confirmed by detailed study.*
