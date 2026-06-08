# Course Overview — MV/LV Electrical Equipment of a ~2 MW Process Plant

This overview expands on the [course landing page](../README.md): it sets out detailed learning
outcomes per module, suggested study time, the team roles that build the course, the
assessment / self-check approach, and a glossary of key abbreviations.

**Design basis (consistent throughout):** ~2 MW process plant · utility MV at **11 kV** ·
distribution/utilization LV at **400/415 V**, 3-phase · **50 Hz** · IEC conventions · MV system
resistance-earthed (NER), LV TN-S · redundancy via **2 × transformers + bus-tie** plus a standby
diesel generator for essential loads. See the
[reference design document](../docs/main-electrical-equipment-2MW-process-plant.md) for the full
basis of design, tag scheme and sizing logic.

> All ratings and diagrams are **indicative and tentative** — illustrative of method and typical
> practice, not a substitute for project-specific studies and specifications.

---

## How the Course Fits Together

The three modules form a deliberate progression around one shared example plant:

1. **Identify** the equipment and understand what each item *does* (Module 1).
2. **Size and verify** that equipment with the core calculations (Module 2).
3. **Stress-test** the architecture by hunting single points of failure (Module 3).

The same tag set — `MV-SWGR`, `TX-1`/`TX-2`, `LV-MSB`, `MCC`, `VFD`, `PFC`, `DG`, `ATS`, `UPS`,
`NER` — is used in every module and on every diagram so that knowledge transfers directly.

---

## Detailed Learning Outcomes per Module

### Module 1 — Equipment Identification
*File:* [module-01-equipment-identification.md](module-01-equipment-identification.md) ·
*Diagram:* [sld-master-2MW.md](../diagrams/sld-master-2MW.md)

On completion you will be able to:

- Navigate a complete MV/LV single-line diagram and trace power flow from the utility MV incomer
  down to process motors and essential/clean-power loads.
- Locate and name each principal item by its **tag** (e.g. `MV-SWGR`, `TX-1`, `LV-MSB`, `MCC-1`,
  `VFD`, `PFC`, `DG`, `ATS`, `UPS`, `NER`).
- State the **function** of each item and how it relates to its neighbours, using a table whose
  rows link visually to the tags on the drawing.
- Distinguish a **PCC** (Power Control Centre / main LV switchboard) from an **MCC** (Motor Control
  Centre) and explain where each is used.
- Recognise the standard symbols for ACBs, MCCBs, contactors, transformers, CTs/VTs and earthing.

### Module 2 — Electrical Calculations
*File:* [module-02-calculations.md](module-02-calculations.md) ·
*Diagram:* [sld-master-2MW.md](../diagrams/sld-master-2MW.md)

On completion you will be able to:

- Build a **demand / diversity** estimate and convert plant load (MW) to apparent power (MVA).
- Size the **MV/LV transformers** (including N+1 logic for the 2 × 1600 kVA split-bus arrangement).
- Compute **full-load current (FLC)** at MV and LV and the transformer **secondary short-circuit
  current** from its impedance (Z ≈ 6 %).
- Estimate **voltage drop** along feeders and check it against IEC limits.
- Size **power-factor correction (PFC)** to move ~0.85 → 0.95+, including the need for detuned
  reactors with VFD harmonics.
- Select and coordinate **protective devices** (ACB/MCCB) and verify **cable** ampacity against
  load and fault duty.

### Module 3 — Single Points of Failure (SPOF)
*File:* [module-03-spof-analysis.md](module-03-spof-analysis.md) ·
*Diagrams:* [spof-examples/](../diagrams/spof-examples/)

On completion you will be able to:

- Define a **single point of failure** in the context of plant power distribution and explain its
  operational and safety consequences.
- Systematically scan a single-line diagram for SPOFs (single incomer, single transformer,
  un-tied bus, single ATS, shared cable route, common earthing, etc.).
- Compare several example architectures and rank them by **resilience**.
- Propose mitigations — **N+1** redundancy, **bus-tie** operation, **dual feeds**, standby
  generation (**DG + ATS**), and **UPS** for control/critical loads — and articulate their
  trade-offs (cost, complexity, footprint).

### Module 4 — Control Philosophy & Power Management
*File:* [module-04-control-philosophy.md](module-04-control-philosophy.md) ·
*Diagram:* [control architecture](../diagrams/svg/control-architecture.svg)

On completion you will be able to:

- State the main **continuity-of-supply philosophies** (redundancy/segregation, automatic
  bus transfer, DG/ATS, load shedding, no-break supplies, motor re-acceleration) that avoid
  service interruption.
- Describe **DCS / SCADA / PMS** integration and the role of **IEC 61850** (GOOSE for fast
  load shedding & bus transfer, MMS for monitoring), and when to **hardwire** vs network.
- Identify **best-practice technologies** — digital substation, intelligent load shedding,
  condition monitoring/digital twin, **BESS** / grid-forming inverters, cybersecurity.
- Explain how **renewable-driven grid voltage instability** affects the plant and the
  **ride-through** (UVRT, VFD kinetic buffering) and **dynamic support** (STATCOM/SVC, DVR,
  BESS) measures that mitigate it.

### Module 5 — Reliability Engineering: FMECA & RAM/RBD
*File:* [module-05-reliability-fmeca.md](module-05-reliability-fmeca.md)

On completion you will be able to:

- Define and compute the core reliability metrics — **λ, MTBF, MTTR, availability**.
- Build a **reliability block diagram (RBD)** and quantify **series vs redundant** availability.
- Perform an **FMECA** (IEC 60812): failure modes → effects → **criticality / RPN**.
- Rank findings on a **risk matrix** and produce prioritised recommendations, following the
  **SF-01…SF-04** study method (IEEE 493 / ISO 20815 / ISO 14224).

---

## Suggested Study Time

| Module | Reading & worked examples | Self-check & exercises | Total (indicative) |
|--------|---------------------------|------------------------|--------------------|
| 0 — Overview & reference doc | 0.5 h | — | **~0.5 h** |
| 1 — Equipment Identification | 1.5 h | 0.5 h | **~2 h** |
| 2 — Electrical Calculations | 2.5 h | 1.0 h | **~3.5 h** |
| 3 — SPOF Analysis | 1.5 h | 1.0 h | **~2.5 h** |
| 4 — Control Philosophy & Power Management | 2.0 h | 0.5 h | **~2.5 h** |
| 5 — Reliability Engineering (FMECA & RAM/RBD) | 1.5 h | 0.5 h | **~2 h** |
| **Course total** | | | **~13 h** |

Times are indicative for a learner meeting the prerequisites; allow more if the electrical
fundamentals are new.

---

## Roles Involved in Building the Course

This course is produced collaboratively. Each role owns a distinct part of the deliverable:

| Role | Responsibility |
|------|----------------|
| **Electrical engineer** | Authors the technical module content — equipment functions, the calculation methods and worked examples, and the SPOF analysis. Owns the basis of design and ensures ratings, standards and methods are correct. |
| **Technical draftsman** | Produces the single-line diagrams — the master reference SLD and the SPOF example variants — with consistent symbols and the shared tag scheme. |
| **Training planner / curriculum designer** | Defines the course structure, learning objectives and outcomes, study plan, front matter (this overview and the README), assessment approach and glossary; keeps tags and conventions consistent across all artefacts. |

---

## Assessment & Self-Check Approach

This is a **self-paced, self-assessed** course — there is no formal examination. Progress is
confirmed through:

- **End-of-module self-checks** — short question sets that map back to that module's learning
  outcomes. Attempt them before reading the model answers.
- **Tag-spotting drills (Module 1)** — given the master SLD, name and locate each tagged item and
  state its function from memory.
- **Worked-then-blank exercises (Module 2)** — each calculation is shown fully worked, then a
  similar problem is posed with different figures for you to solve and check against the method.
- **SPOF hunts (Module 3)** — for each example diagram, list the single points of failure, then
  compare with the provided analysis and proposed mitigations.
- **Capstone check** — re-read the [reference design doc](../docs/main-electrical-equipment-2MW-process-plant.md)
  and confirm you can explain every item on its §6 "Main Equipment Checklist" and justify the
  redundancy philosophy.

Suggested mastery bar: you can read the master SLD unaided, reproduce each calculation method,
and identify the major SPOFs in an unfamiliar diagram.

---

## Glossary of Key Abbreviations

| Abbr. | Term | Meaning in this course |
|-------|------|------------------------|
| **MV** | Medium Voltage | Higher distribution voltage; here the **11 kV** utility/incoming level (typically 1 kV–36 kV). |
| **LV** | Low Voltage | Utilization voltage; here **400/415 V**, 3-phase, 50 Hz (≤ 1 kV AC). |
| **SLD** | Single-Line Diagram | One-line schematic showing the power system's main components and their connections. |
| **MCC** | Motor Control Centre | LV assembly of motor starters (DOL, star-delta, soft-starter, VFD) feeding process motors. |
| **PCC** | Power Control Centre | The main LV switchboard distributing power to MCCs and feeders (here `LV-MSB`). |
| **VFD** | Variable Frequency Drive | Power-electronic converter providing variable-speed control of motors (a.k.a. VSD). |
| **PFC** | Power Factor Correction | Capacitor bank (often detuned) that raises power factor and reduces reactive demand. |
| **ATS** | Automatic Transfer Switch | Automatically transfers the essential bus between utility and standby generator. |
| **UPS** | Uninterruptible Power Supply | Battery-backed clean supply for DCS/PLC/SCADA, instrumentation and critical comms. |
| **NER** | Neutral Earthing Resistor | Resistor in the MV neutral that limits earth-fault current. |
| **SPOF** | Single Point of Failure | A component whose failure alone disables a function or the whole supply. |
| **ACB** | Air Circuit Breaker | Large LV breaker, typically the switchboard incomer / bus-tie. |
| **MCCB** | Moulded-Case Circuit Breaker | Compact LV breaker for outgoing feeders and smaller circuits. |
| **DOL** | Direct-On-Line | Simplest motor starter — connects the motor straight to the supply (small motors). |
| **DCS** | Distributed Control System | Plant process-control system with operator HMI; receives electrical status and issues high-level commands. |
| **SCADA** | Supervisory Control & Data Acquisition | Supervisory monitoring/control layer for the power system. |
| **PMS** | Power Management System | Dedicated electrical controller: load shedding, bus transfer, generator control/synchronisation, energy management. |
| **IEC 61850** | Substation comms standard | Defines station/process-bus messaging — **MMS** (monitoring) and **GOOSE** (fast peer-to-peer trips/transfers). |
| **IED** | Intelligent Electronic Device | Numerical multifunction relay (protection + measurement + control) at each bay. |
| **LVRT/UVRT** | (Low/Under) Voltage Ride-Through | Capability/settings that let the plant ride through short voltage dips instead of tripping. |
| **STATCOM/SVC** | Static (synchronous) compensator / SVC | Fast dynamic reactive-power source for voltage stabilisation and flicker control. |
| **BESS** | Battery Energy Storage System | Storage (often grid-forming) giving ride-through, inertia emulation, fast frequency/voltage support, islanding. |
| **ROCOF** | Rate of Change of Frequency | Measure of frequency volatility; rises as grid inertia falls with more renewables. |
| **FMECA** | Failure Mode, Effects & Criticality Analysis | Structured method (IEC 60812) listing failure modes, effects and criticality per component. |
| **RAM** | Reliability, Availability, Maintainability | The quantitative analysis of how often/long a system is unavailable. |
| **RBD** | Reliability Block Diagram | Series/parallel model used to compute system availability from component data. |
| **MTBF / MTTR** | Mean Time Between Failures / To Repair | Average up-time between failures / average restore time; set availability A = MTBF/(MTBF+MTTR). |
| **RPN** | Risk Priority Number | FMECA score = Severity × Occurrence × Detection, used to rank risks. |
| **ISO 14224** | Reliability data taxonomy | Standard equipment taxonomy and failure-data classification used in the study. |

**Other tags used (from the reference design):** `MV-SWGR` (MV switchgear), `MV-MET` (metering),
`MV-PROT` (MV protection relays), `TX-1`/`TX-2` (MV/LV transformers), `LV-MSB` (main LV
switchboard / PCC), `DG` (diesel generator), `DB`/`EDB` (distribution / essential distribution
boards), `DCDB` (DC battery & charger), `B/T` (bus-tie).

---

*This overview is part of the course front matter. Module content and diagrams are authored
separately; figures throughout are indicative and to be confirmed against project-specific studies.*
