# Module 5 — Reliability Engineering: FMECA & RAM/RBD

*Part of the [MV/LV ~2 MW Process Plant training course](../README.md). Diagram:
[master single-line diagram](../diagrams/sld-master-2MW.md). Basis of design:
[reference design document](../docs/main-electrical-equipment-2MW-process-plant.md).*

> All methods and figures in this module are **indicative and tentative** — they
> illustrate the method, not a substitute for project-specific failure data and the
> governing standards.

---

## Introduction

[Module 3](module-03-spof-analysis.md) **found** single points of failure by inspection.
This module turns that into a **formal, repeatable reliability study** — the way a real
SPOF/reliability assessment is delivered: inventory the system, analyse failure modes and
their criticality (**FMECA**), quantify availability (**RAM / RBD**), and rank
**recommendations** by risk.

It follows a four-step study method (the same shape used in industrial SPOF assessments):

| Step | Name | Output |
|------|------|--------|
| **SF-01** | Document inventory | As-found SLDs, equipment list, ratings, protection settings (ISO 14224 taxonomy) |
| **SF-02** | **FMECA** | Failure modes, effects and **criticality** per component (IEC 60812) |
| **SF-03** | Recommendations | Prioritised mitigations (ranked by criticality) |
| **SF-04** | Site-visit report | Verified as-found condition, photos, data gaps |

### Learning outcomes

On completion you will be able to:

- Define the core reliability metrics — **λ, MTBF, MTTR, availability** — and compute them.
- Build a **reliability block diagram (RBD)** and quantify **series vs redundant** availability.
- Perform an **FMECA** (IEC 60812): failure modes → effects → **criticality / RPN**.
- Rank findings on a **risk matrix** and turn them into prioritised recommendations.

---

## 1. Reliability metrics

| Quantity | Symbol / formula | Meaning |
|----------|------------------|---------|
| Failure rate | λ (failures/hour) | how often a component fails |
| Mean time between failures | **MTBF = 1/λ** | average up-time between failures |
| Mean time to repair/restore | **MTTR** | average time to restore (detect + spares + repair) |
| Reliability | **R(t) = e^(−λt)** | probability of no failure up to time t |
| **Availability** | **A = MTBF / (MTBF + MTTR)** | fraction of time the function is available |
| Unavailability | **U = 1 − A** | fraction of time down (≈ U × 8760 h/yr) |

**Worked example (one transformer).** MTBF = 200,000 h, MTTR = 168 h (incl. spare logistics):

```
A = 200,000 / (200,000 + 168) = 0.99916
U = 1 − 0.99916 = 8.4 × 10⁻⁴  →  U × 8760 ≈ 7.4 h/yr downtime
```

---

## 2. Reliability Block Diagrams (RAM / RBD)

An RBD models how component availabilities combine. **Series** = all must work (any failure
stops the function); **parallel / redundant** = the function survives if at least one path works.

```
SERIES (no redundancy):        [Incomer]──[TX]──[LV bus]──[load]
                               A_sys = A1 × A2 × A3 × …      (always lower than the worst link)

PARALLEL (1-out-of-2):          ┌──[TX-1]──┐
                                ┤          ├      A_par = 1 − (1−A1)(1−A2)
                                └──[TX-2]──┘      (much higher than either alone)
```

**Worked comparison (transformer, A = 0.99916 each).**

```
Single transformer (series):     A = 0.99916            → ~7.4 h/yr down
Two transformers, 1-out-of-2:    A = 1 − (1−0.99916)²
                                   = 1 − (8.4e-4)² = 0.99999929  → ~0.006 h/yr (~22 s/yr)
```

**The catch — the common elements.** The redundant pair is only as good as the elements it
**shares**: the common LV bus, the **bus-tie ([BT](../diagrams/sld-master-2MW.md#bt))** and the
transfer scheme are **series** elements that cap the benefit. This is exactly the Module 3
lesson, now quantified: redundancy upstream is wasted if a single shared bus/tie/ATS remains.

**MTTR is a design lever.** An **automatic** bus-tie or [ATS](../diagrams/sld-master-2MW.md#ats)
(Module 4) cuts the *restore* time for the essential load from hours (manual) to **seconds**
(auto-transfer) — which raises availability far more cheaply than chasing a lower failure rate.

---

## 3. FMECA (IEC 60812)

**FMECA** = Failure Mode, Effects **and Criticality** Analysis. For each component: list its
**failure modes**, the **local** and **system** effect, then score **criticality**. Two common
scoring schemes:

- **RPN** = Severity (S) × Occurrence (O) × Detection (D), each 1–10 (higher = worse).
- **Criticality matrix** = Severity × Probability mapped to a risk colour.

### Worked FMECA (extract — master SLD components)

| Tag | Function | Failure mode | Effect (local → system) | S | O | D | RPN | Recommendation |
|-----|----------|--------------|--------------------------|---|---|---|-----|----------------|
| [TX-1](../diagrams/sld-master-2MW.md#tx-1) | Step MV→LV | Winding fault | TX trips → Bus A dead (half plant if no tie) | 8 | 3 | 4 | **96** | Auto bus-tie + N-1 load shed; 87T diff; oil/temp monitoring |
| [BT](../diagrams/sld-master-2MW.md#bt) | Back-feed dead bus | Fails to close | Essential load lost on N-1 | 9 | 2 | 5 | **90** | Auto-transfer scheme; periodic test; position monitoring |
| [ATS](../diagrams/sld-master-2MW.md#ats) | Utility↔DG transfer | Fails to transfer | Essential bus dead on utility loss | 9 | 3 | 4 | **108** | Redundant control; monthly on-load test; alarm to PMS |
| [DG](../diagrams/sld-master-2MW.md#dg) | Standby power | Fails to start | No backup during outage | 8 | 4 | 3 | **96** | Weekly auto test-on-load; fuel & battery monitoring |
| [LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) | Distribute LV | Busbar fault | Whole bus section lost | 9 | 1 | 6 | **54** | Segregation (Form 4); arc-flash detection; PM |
| [UPS](../diagrams/sld-master-2MW.md#ups) | No-break control | Battery/inverter fail | DCS/PLC ride-through lost | 7 | 3 | 3 | **63** | Redundant UPS; battery monitoring; bypass |

*(Scores are illustrative; calibrate S/O/D scales and use real failure data — IEEE 493 /
ISO 14224 — on a project.)*

**Reading it:** the **ATS (RPN 108)** and **TX-1 / DG (96)** are the top risks here — exactly the
items whose mitigations dominate the design (auto-transfer, N-1, tested standby). Note how
**detection (D)** drives risk: adding **condition monitoring** (Module 4) lowers D and therefore
RPN without touching the hardware.

---

## 4. Risk ranking & recommendations (SF-03)

Plot each finding on a **Severity × Probability** matrix and act top-down:

```
        Probability →
  S   |  Low    Med    High
  ▲ H |  Med    High   HIGH      HIGH  → mitigate now (e.g. ATS, bus-tie, DG start)
  |   |
  | M |  Low    Med    High      Med   → plan mitigation / monitor
  |   |
  | L |  Low    Low    Med       Low   → accept / routine maintenance
```

**From analysis to action.** Recommendations link straight back to the rest of the course:
**N+1 and bus-tie** (Module 3) cut *severity/occurrence* of supply loss; **auto-transfer, load
shedding and condition monitoring** (Module 4) cut *MTTR* and *detection*; tested **DG/ATS**
schemes cut *occurrence* of a failed start. Each recommendation should state the **risk before
and after** so its value is explicit.

---

## 5. Standards & references

| Topic | Standard |
|-------|----------|
| FMEA / FMECA method | **IEC 60812** (and MIL-STD-1629A) |
| Industrial power-system reliability data & methods | **IEEE 493** ("Gold Book") |
| Reliability/availability of process systems | **ISO 20815** |
| Equipment reliability & maintenance data (taxonomy) | **ISO 14224** |
| Reliability block diagrams | **IEC 61078** |
| Dependability management | IEC 60300 series |

---

## 6. Self-check problems

1. A component has **MTBF = 150,000 h** and **MTTR = 120 h**. Find its **availability** and
   annual downtime.
2. Two identical units, each **A = 0.99**, in a **1-out-of-2** (parallel) arrangement. Find the
   system availability.
3. The same two units in **series**. Find the system availability — and comment.
4. An FMECA line scores **S = 8, O = 2, D = 5**. Find the RPN. If condition monitoring lowers
   detection to **D = 2**, what is the new RPN, and what does that show?

<details>
<summary><strong>Answers</strong></summary>

1. A = 150,000 / (150,000 + 120) = **0.99920**; U = 7.99 × 10⁻⁴ → 7.99e-4 × 8760 ≈ **7.0 h/yr**.
2. A_par = 1 − (1 − 0.99)² = 1 − (0.01)² = 1 − 1e-4 = **0.9999** (≈ 0.9 h/yr down).
3. A_ser = 0.99 × 0.99 = **0.9801** (≈ 174 h/yr down) — **series is worse than either unit**;
   redundancy (Q2) is ~200× better than series (Q3) for the same components.
4. RPN = 8 × 2 × 5 = **80**; with D = 2 → RPN = 8 × 2 × 2 = **32**. Better **detection**
   (monitoring) cuts risk by ~60 % **without changing the failure rate** — often the cheapest
   mitigation.

</details>

---

*This module closes the course's reliability thread (Modules 3 → 4 → 5). Every figure is
indicative and to be confirmed by project failure data and the governing standards.*
