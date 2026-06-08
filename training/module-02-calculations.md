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
- Read a **load-flow** result (bus voltages, tap, losses) and confirm limits.
- **Coordinate protection** for selectivity (grading margin, relay/trip settings).
- Estimate **arc-flash** incident energy and boundary (**IEEE 1584**) and use the
  clearing-time lever.
- Size the **earthing** system (NER, earth grid, earth conductor) and set the
  **lightning-protection** class.

Sections **§9–§12** extend the set to the full power-system study suite — **load-flow,
protection coordination, arc-flash (IEEE 1584) and earthing/lightning** — matching the
studies required by an electrical SPOF-assessment scope (alongside the short-circuit
study of §4).

**Constants used throughout:** √3 = 1.732; LV line voltage V = 400 V; MV line
voltage = 11 kV; 50 Hz.

---

## Why these calculations matter

Engineering calculations are what turn a concept single-line diagram into
**correctly-rated, safe, coordinated equipment**. Every rating you see on the SLD
— a transformer kVA, a breaker frame and breaking capacity, a busbar bracing
figure, a cable cross-section, a capacitor bank, a genset — is the *output* of one
of the calculations below, and the calculation is the **audit trail** that
justifies it.

Skip or guess them and you fail in one of two directions:

- **Under-rating** → unsafe or non-functional plant: cables and busbars that
  overheat (fire risk), switchgear that cannot interrupt a fault (catastrophic
  failure), protection that mis-coordinates or fails/nuisance-trips, motors that
  won't start, and process voltage too low to run.
- **Over-rating** → wasted capital tied up in oversized transformers, switchgear
  frames, cable and gensets that the plant will never use.

The right calculation, done with the right inputs, lands the design between those
two — safe and coordinated, without paying for capacity that is never needed.

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

> **Why this calc matters**
> - **Why it's essential:** sets the total size of the whole electrical plant.
> - **If not done / done wrong:** over-estimate wastes capital on oversized
>   gear; under-estimate leaves no capacity and forces a costly retrofit.
> - **Inputs:** connected-load list (nameplate kW), demand/diversity factor,
>   plant power factor.
> - **Outputs:** maximum demand (MW) and apparent power (MVA), installed base.
> - **Equipment sized / selected:** sets the base for **TX-1/TX-2**,
>   **MV-SWGR**, **LV-MSB** and feeders — effectively everything downstream.

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

> **Why this calc matters**
> - **Why it's essential:** picks the transformer rating and proves redundancy
>   (one unit can carry the essential load).
> - **If not done / done wrong:** undersized → overload/loss of supply on N-1;
>   oversized → paying for kVA and switchgear frames never used.
> - **Inputs:** apparent power (from §1), redundancy concept (N-1), essential-
>   load fraction, standard transformer ratings.
> - **Outputs:** number/rating of units (2 × 1600 kVA), normal and N-1 loading
>   in pu.
> - **Equipment sized / selected:** **TX-1/TX-2**, the **bus-tie (BT)** scheme,
>   and the load-shedding requirement on **LV-MSB**.

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

> **Why this calc matters**
> - **Why it's essential:** the continuous current every conductor and breaker
>   on the LV incomer must carry.
> - **If not done / done wrong:** under-rated busbar/breaker overheats and ages
>   prematurely; over-rated wastes copper and frame cost.
> - **Inputs:** transformer kVA, LV line voltage.
> - **Outputs:** LV full-load current (≈2310 A); MV-side FLC (≈84 A).
> - **Equipment sized / selected:** **LV-MSB** incomer **ACB** frame and busbar
>   rating; MV transformer-feeder breakers (`52-T1`/`52-T2`) in **MV-SWGR**.

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

> **Why this calc matters**
> - **Why it's essential:** sets the fault current the switchgear must safely
>   interrupt and the busbars must withstand mechanically.
> - **If not done / done wrong:** breaker with too-low breaking capacity can
>   explode on a fault, or unbraced busbars deform — a safety-critical failure.
> - **Inputs:** LV full-load current (§3), transformer impedance Z%, source/
>   parallelling assumptions.
> - **Outputs:** prospective short-circuit current (kA) per unit and parallel.
> - **Equipment sized / selected:** breaking capacity (Icu/Ics) and busbar
>   bracing of **LV-MSB**, **MCC** and all **ACB/MCCB**; bus-tie interlock.

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

> **Why this calc matters**
> - **Why it's essential:** sizes the motor feeder/protection and decides the
>   starting method (DOL vs soft-start vs VFD).
> - **If not done / done wrong:** DOL inrush dips the bus and nuisance-trips or
>   stalls the motor; under-rated starter/contactor fails on start.
> - **Inputs:** motor kW, voltage, pf, efficiency, starting multiple (≈6.5×).
> - **Outputs:** motor FLC (≈194 A), starting current (≈1260 A DOL), starting-
>   method recommendation.
> - **Equipment sized / selected:** motor starter/overload and feeder in the
>   **MCC**, soft-starter or **VFD**, and the LV-vs-MV feed decision.

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

> **Why this calc matters**
> - **Why it's essential:** picks a conductor that carries the load without
>   overheating and keeps voltage at the load high enough to run.
> - **If not done / done wrong:** under-sized cable overheats (insulation
>   failure/fire) or volt-drop too high to start/run the load; over-sized wastes
>   copper/aluminium.
> - **Inputs:** design current (FLC), grouping/temperature derating factors,
>   run length, conductor R/X, voltage-drop limit.
> - **Outputs:** required tabulated rating, cable cross-section, %voltage drop.
> - **Equipment sized / selected:** the feeder **cable** (95 mm² Cu XLPE here)
>   and its gland/tray/containment.

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

> **Why this calc matters**
> - **Why it's essential:** raises power factor to avoid utility reactive-power
>   penalties and frees transformer/cable capacity.
> - **If not done / done wrong:** ongoing low-pf penalties on the energy bill and
>   capacity wasted carrying reactive current; an un-detuned bank can resonate
>   with VFD harmonics and fail.
> - **Inputs:** active power, present pf, target pf, harmonic environment.
> - **Outputs:** required reactive power (≈580 kVAr), detuning requirement.
> - **Equipment sized / selected:** the automatic capacitor bank **PFC** (with
>   7 % detuning reactors) and its feeder/switching steps.

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

> **Why this calc matters**
> - **Why it's essential:** sizes the backup source that keeps essential/safety
>   loads running when the utility fails.
> - **If not done / done wrong:** undersized genset stalls on motor start or
>   trips on overload during an outage (loss of essential plant); oversized is
>   very costly per kVA and runs inefficiently lightly loaded.
> - **Inputs:** essential active load, pf, largest-motor step load, transient
>   voltage-dip limit, site de-rating (altitude/ambient).
> - **Outputs:** generator rating (≈1000 kVA), step-load/voltage-dip check.
> - **Equipment sized / selected:** the standby **DG** set, its breaker/ATS and
>   the essential-load distribution it feeds.

---

## 9. Load-flow analysis

**Goal:** confirm the **voltage profile, power flows and losses** at peak load —
that every bus stays within ±5 % and no branch is thermally overloaded.

**Transformer voltage regulation.** Split Z = 6 % into R ≈ 1.2 %, X ≈ 5.9 %. At the
normal ~73 % loading (§2), pf ≈ 0.90 (cosφ = 0.90, sinφ = 0.436):

```
ΔV% ≈ load_pu × (R%·cosφ + X%·sinφ)
ΔV% ≈ 0.73 × (1.2×0.90 + 5.9×0.436)
ΔV% ≈ 0.73 × (1.08 + 2.57) = 0.73 × 3.65 = 2.7 %
```

**Bus voltage.** With the transformer off-load tap set to nominal, the
[LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) sits ~2.7 % below its no-load value at
full load (≈ 389 V); a **+2.5 % tap** restores it to ~400 V. Adding the worst feeder
drop of 2.4 % (§6) puts the motor terminal at ≈ **97–98 %** of nominal — inside the
±5 % limit. Correcting power factor (§7) lowers current and lifts the profile further.

**Losses (indicative).** Transformer load (copper) loss scales with loading²; at 73 %
of a unit with ~17 kW full-load loss, each transformer dissipates ≈ 0.73² × 17 ≈ **9 kW**.

**Result:** voltages within limits after tap selection; flows confirm each transformer
at ~73 % and feeders within ampacity. The study validates the §1–§7 sizing and tells
you whether the tap, cable sizes and PFC are adequate **or** where reinforcement is needed.

> **Why this calc matters**
> - **Why it's essential:** proves the steady-state network actually delivers
>   acceptable voltage to every load and that nothing is overloaded.
> - **If not done / done wrong:** hidden under-voltage (process trips, motors won't
>   start) or over-voltage, and undetected branch overloads; or needless reinforcement.
> - **Inputs:** load list, source voltage, transformer/cable impedances, tap settings, pf.
> - **Outputs:** bus voltages, branch power flows, losses, required tap position.
> - **Equipment sized / selected:** transformer **tap range**, conductor sizes,
>   **PFC** placement; validates **TX-1/TX-2** and feeder loading.

---

## 10. Protection coordination (selectivity)

**Goal:** set the protective devices so the one **closest to the fault trips first**,
isolating the smallest possible zone (selectivity), while still clearing every fault fast.

**The series of devices** (fault on a motor feeder, tracing upstream): motor MCCB →
[MCC](../diagrams/sld-master-2MW.md#mcc-1) → LV outgoing MCCB → LV incomer
[ACB](../diagrams/sld-master-2MW.md#lv-msb) → MV transformer-feeder relay `[52-T]`
([MV-SWGR](../diagrams/sld-master-2MW.md#mv-swgr)) → MV incomer `[52-I]`.

**Time grading.** Between two graded relays leave a margin Δt for breaker opening +
relay overshoot + CT error + safety (≈ 0.3 s):

```
t_upstream = t_downstream + Δt
LV incomer ACB short-time delay  t = 0.20 s
MV 52-T relay (51)               t = 0.20 + 0.30 = 0.50 s
```

**MV relay pickup** (CT 100/1 A on the ~84 A primary FLC of §3):

```
I_pickup = 1.25 × 84 A = 105 A  → 1.05 × CT  (set ~1.05 on 100/1)
```

Transformer **internal** faults are cleared instantly by the **87T differential**
(see `[52-T]`), independent of the time grading above.

**Result:** indicative grading — motor feeder ≈ 0.05 s, LV incomer ≈ 0.20 s, MV feeder
≈ 0.50 s — is **selective**: a feeder fault trips only that feeder, not the whole bus.

> **Why this calc matters**
> - **Why it's essential:** turns the fault levels (§4) into actual relay/trip
>   settings that isolate faults selectively and fast.
> - **If not done / done wrong:** loss of selectivity (an upstream breaker trips for a
>   downstream fault → far larger outage), or too-slow clearing (equipment damage and
>   higher arc-flash energy — see §11).
> - **Inputs:** fault levels (§4), device time-current curves, CT ratios, grading margin.
> - **Outputs:** relay pickup and time settings, trip-unit bands, a discrimination study.
> - **Equipment sized / selected:** **MV-PROT** relays/IEDs and the **ACB/MCCB** trip
>   units; informs use of zone-selective interlocking / bus differential.

---

## 11. Arc-flash / incident-energy study (IEEE 1584)

**Goal:** estimate the **incident energy** and **arc-flash boundary** at the
[LV-MSB](../diagrams/sld-master-2MW.md#lv-msb), to label the gear and select PPE — and
to show why **clearing time** (§10) is the dominant lever.

**Inputs.** Bolted fault I_bf ≈ 38.5 kA (§4), 400 V, in an enclosure; working distance
D = 600 mm; upstream device clearing time t.

**Arcing current** (LV arcing/bolted ratio ≈ 0.5–0.6 per IEEE 1584):

```
I_a ≈ 0.58 × 38.5 kA ≈ 22 kA
```

**Incident energy** scales with arcing current × time and inversely with distance². With
the upstream device clearing at **t = 0.20 s** (the LV incomer band from §10), the
IEEE 1584-2018 empirical model gives, indicatively:

```
E ≈ 10 cal/cm²  (at D = 600 mm)
```

**Arc-flash boundary** (distance where E falls to E_B = 1.2 cal/cm², inverse-square scaling):

```
AFB ≈ D × √(E / 1.2) = 0.6 m × √(10 / 1.2) = 0.6 × 2.89 ≈ 1.7 m
```

**The clearing-time lever.** Halving the clearing time roughly halves the energy. Adding
an **arc-reduction measure** (maintenance switch, zone-selective interlocking, or an
arc-flash relay) to clear in **t = 0.05 s** drops E to ≈ **2.5 cal/cm²** and shrinks the
boundary — at some tension with the selectivity grading of §10, which is why bus
differential / ZSI is used to get both.

**Result:** ~**10 cal/cm²** at 600 mm → arc-rated PPE must exceed this (e.g. a 12–25
cal/cm² kit), arc-flash boundary ≈ **1.7 m**; faster tripping is the cheapest way to
reduce it. *Exact figures require the full IEEE 1584-2018 model and site data.*

> **Why this calc matters**
> - **Why it's essential:** quantifies the thermal hazard to personnel and sets PPE,
>   labels and arc-mitigation — a life-safety requirement (NFPA 70E / IEEE 1584).
> - **If not done / done wrong:** people exposed to under-rated PPE (severe burns),
>   non-compliant/ missing arc-flash labels, no basis for mitigation.
> - **Inputs:** bolted fault current (§4), arcing-current ratio, **clearing time** (§10),
>   working distance, electrode/enclosure configuration.
> - **Outputs:** incident energy (cal/cm²), arc-flash boundary, PPE category, labels.
> - **Equipment sized / selected:** **PPE** and warning labels; drives arc-reduction
>   relays / maintenance switches / ZSI and influences switchgear selection (arc-rated).

---

## 12. Earthing & lightning-protection assessment

**Goal:** size the **earthing system** — the MV neutral earthing resistor
([MV-NER](../diagrams/sld-master-2MW.md#mv-ner)), the earth grid and the earth
conductors — and set the **lightning-protection** class (IEC 62305).

**MV neutral earthing resistor.** The MV system is **resistance-earthed** to limit the
earth-fault current (here to ≈ 300 A) so faults are detectable but damage/arc energy is
limited:

```
R_NER = (V_LL / √3) / I_ef = (11,000 / 1.732) / 300 = 6351 / 300 ≈ 21 Ω
```

(Rated for the fault duration, e.g. a 10 s short-time rating; I²R during fault
≈ 300² × 21 ≈ 1.9 MW dissipated briefly.)

**LV earthing.** The 400 V system is **TN-S, solidly earthed**, so an LV earth fault is
of the same order as a line fault and is cleared quickly by the feeder protection.

**Earth-conductor sizing (adiabatic).** Conductor that must carry the LV fault for the
clearing time (I = 38.5 kA, t = 0.2 s, k ≈ 143 for Cu/PVC):

```
A = I × √t / k = 38,500 × √0.2 / 143 = 38,500 × 0.447 / 143 ≈ 120 mm²
```

**Earth grid & lightning.** Target grid resistance (e.g. ≤ 1 Ω for the substation,
depending on soil resistivity ρ) with touch/step voltages inside the **IEEE 80** limits;
the **lightning-protection level (LPL I–IV)** follows an **IEC 62305** risk assessment,
fixing air-termination, down-conductor and earth-termination requirements, all bonded to
the grid.

**Result:** **R_NER ≈ 21 Ω**, earth conductors ≥ **120 mm² Cu** (governed by the LV
fault), grid resistance to target with verified touch/step voltages, and an LPS class
from the IEC 62305 risk study.

> **Why this calc matters**
> - **Why it's essential:** keeps touch/step voltages safe, gives protection a path to
>   detect earth faults, limits fault damage, and protects against lightning.
> - **If not done / done wrong:** dangerous touch/step voltages (electrocution),
>   undetected earth faults, equipment damage, and lightning exposure.
> - **Inputs:** system earthing method, earth-fault current & duration, soil resistivity,
>   grid geometry, lightning risk assessment.
> - **Outputs:** NER ohms/rating, earth-conductor csa, grid resistance, touch/step
>   compliance, LPS class.
> - **Equipment sized / selected:** **MV-NER**, the earth grid/electrodes and bonding,
>   earthing **conductors**, and the lightning-protection system (LPS).

---

## Calculations → equipment → cost impact

A one-row-per-calculation map from each calculation to the equipment it sizes and
why it does (or doesn't) drive capital cost.

| Calculation | Key inputs | Key outputs | Equipment sized | If skipped | Cost impact (H/M/L + why) |
|---|---|---|---|---|---|
| 1. Load & demand | Connected kW, diversity factor, pf | Demand (MW), apparent power (MVA) | Base for TX-1/TX-2, MV-SWGR, LV-MSB, feeders | Whole plant mis-sized; costly retrofit or wasted capital | **High** — sets the entire plant size; everything scales from it |
| 2. Transformer sizing & N-1 | MVA, redundancy concept, essential fraction | Unit rating, normal/N-1 loading (pu) | TX-1/TX-2, bus-tie (BT) scheme | Overload on N-1 or oversized units/switchgear | **High** — transformers + switchgear frames + cable sizes all scale with it |
| 3. Transformer FLC (LV) | Transformer kVA, LV voltage | LV FLC (~2310 A), MV FLC (~84 A) | LV-MSB incomer ACB, busbars; MV feeder breakers | Under-rated busbar/breaker overheats | **High** — sets ACB frame and busbar ampacity (large copper) |
| 4. Short-circuit / fault | LV FLC, Z%, source assumptions | Prospective Isc (kA) | Breaking capacity & bracing of LV-MSB, MCC, ACB/MCCB | Breaker can't clear fault — safety failure | **High** — drives breaker breaking capacity and busbar bracing (expensive) |
| 5. Motor FLC & starting | Motor kW, V, pf, η, start multiple | FLC, start current, start method | MCC starter/overload, soft-starter/VFD, LV-vs-MV feed | Bus dip/nuisance trip; under-rated starter fails | **Medium** — soft-starter/VFD cost vs DOL; affects MCC/feed choice |
| 6. Cable sizing & volt-drop | Design current, derating, length, R/X | Required Iz, cross-section, %ΔV | Feeder cable, containment | Cable overheats (fire) or volt-drop too high | **Medium** — copper/aluminium volume across the plant |
| 7. Power-factor correction | P, present pf, target pf, harmonics | Required kVAr, detuning | PFC bank + 7 % reactors | Utility reactive penalties; capacity wasted | **Medium** — avoids reactive-power penalties and frees capacity |
| 8. Standby generator | Essential load, pf, step load, dip limit | DG rating (~1000 kVA) | DG set, ATS/breaker, essential distro | Genset stalls on outage, or oversized | **High** — gensets are costly per kVA |
| 9. Load-flow | Loads, source V, Z, taps, pf | Bus voltages, flows, losses, tap | Transformer tap, cable sizes, PFC placement | Hidden under/over-voltage or overloads | **Medium** — mainly validates ratings/taps; flags reinforcement |
| 10. Protection coordination | Fault levels, device curves, CT ratios | Relay/trip settings, selectivity | MV-PROT relays, ACB/MCCB trip units | Loss of selectivity (wider outage) or slow clearing | **Low–Med** — mostly settings/engineering (hardware only if extra relays) |
| 11. Arc-flash (IEEE 1584) | Arcing current, clearing time, distance | Incident energy, AFB, PPE category | PPE, labels, arc-reduction (ZSI/relay) | Severe burn risk; non-compliant labels | **Medium** — PPE + arc-reduction relays; safety-critical |
| 12. Earthing & lightning | Earthing method, fault current, soil ρ | NER ohms, earth csa, grid R, LPS class | MV-NER, earth grid, conductors, LPS | Touch/step hazard; equipment & lightning damage | **Medium** — earth grid copper + NER + LPS; safety-critical |

---

## Where the money is

The calculations that **dominate capital cost** are the **demand/transformer
sizing (§1–§3)** and the **short-circuit rating (§4)**: between them they fix the
frame sizes, the breaker breaking capacities, the busbar bracing, the cable
cross-sections and the genset — the most expensive items in the plant. By
contrast, **power-factor correction (§7)** and **voltage-drop / cable losses
(§6)** mainly affect **operating cost and utility penalties** rather than the
headline capital figure. **Motor starting (§5)** sits in between: it adds modest
capital (soft-starter/VFD over DOL) but protects supply quality and reduces the
genset size.

The added studies are mostly **engineering and settings plus modest hardware**:
**load-flow (§9)** chiefly validates the §1–§7 sizing and flags where (or whether)
reinforcement is needed; **protection coordination (§10)** is largely relay/trip
settings; **arc-flash (§11)** and **earthing/lightning (§12)** add PPE, arc-reduction
relays, earth-grid copper and an LPS. Their headline CAPEX is modest, but they are
**safety-critical** — their value is measured in avoided injury, equipment loss and
downtime rather than in the capital figure.

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
| Transformer regulation | ΔV% ≈ load_pu·(R%cosφ + X%sinφ) | 0.73·(1.2·0.9+5.9·0.436) = 2.7 % |
| Grading margin (relays) | t_up = t_down + Δt | 0.20 + 0.30 = 0.50 s |
| Arc-flash boundary | AFB ≈ D·√(E/1.2) | 0.6·√(10/1.2) = 1.7 m |
| NER resistance | R = (V_LL/√3)/I_ef | 6351 / 300 = 21 Ω |
| Earth conductor (adiabatic) | A = I·√t / k | 38,500·√0.2/143 = 120 mm² |

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
6. The MV system is resistance-earthed to limit the earth-fault current to **400 A**
   at 11 kV. What **NER resistance** is required?
7. An arc-flash study gives **6 cal/cm²** at a 600 mm working distance. Estimate the
   **arc-flash boundary** (E_B = 1.2 cal/cm²) using the inverse-square scaling.

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
6. R_NER = (11,000 / 1.732) / 400 = 6351 / 400 = **15.9 Ω**.
7. AFB = 0.6 × √(6 / 1.2) = 0.6 × √5 = 0.6 × 2.236 = **1.34 m**.

</details>

---

*Next: [Module 3 — Single Points of Failure (SPOF) Analysis](module-03-spof-analysis.md).
Every figure here is indicative and to be confirmed by detailed study.*
