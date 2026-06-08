# MV/LV Electrical Equipment of a ~2 MW Process Plant — Training Course

A self-paced training course on the **main electrical equipment** of a medium-voltage /
low-voltage (MV/LV) industrial **process plant** with an installed/demand capacity of
approximately **2 MW**. Working from a complete example single-line diagram (SLD), you will
learn to **identify** the principal equipment and its function, perform the **core electrical
calculations** with worked examples, and analyse **single points of failure (SPOF)** across
several example architectures. The course follows **IEC conventions** (11 kV MV, 400/415 V LV,
50 Hz) and reuses the tag scheme of the project reference design
(`MV-SWGR`, `TX-1`/`TX-2`, `LV-MSB`, `MCC`, `VFD`, `PFC`, `DG`, `ATS`, `UPS`, `NER`, …).

> **Note:** All figures, ratings and diagrams in this course are **indicative and tentative**.
> They illustrate method and typical practice — they are **not** a substitute for a project's
> detailed load list, short-circuit/load-flow studies, utility connection agreement, or the
> governing specifications and standards.

---

## Target Audience & Prerequisites

**Audience:** Early-career electrical engineers, EPC/commissioning staff, process and
maintenance engineers, and technical drafters who need a practical, equipment-focused
understanding of an industrial MV/LV power distribution system.

**Prerequisites:**

- Basic electrical theory — AC power, three-phase systems, the relationship S = √3 · V · I,
  power factor, and per-unit/impedance fundamentals.
- Familiarity with reading engineering drawings (helpful but not essential — Module 1 builds it).
- No prior switchgear or protection experience is assumed.

---

## Course-Level Learning Objectives

By the end of this course you will be able to:

1. **Read** a complete MV/LV single-line diagram and locate each principal piece of equipment by its tag.
2. **Explain the function** of every major item (MV switchgear, transformers, LV switchboard/PCC,
   MCC, VFD, PFC, DG, ATS, UPS, NER) and how they interconnect.
3. **Perform the core sizing calculations** — load/demand, transformer rating, full-load and
   short-circuit currents, voltage drop, power-factor correction, and cable/protection coordination.
4. **Identify single points of failure** in a given architecture and propose redundancy
   improvements (N+1, bus-tie, dual-feed, standby generation).
5. Apply consistent **IEC tag conventions and standards** when describing or documenting a plant.

---

## Course Structure

| # | Module | Goal | File |
|---|--------|------|------|
| 1 | **Equipment Identification** | From a complete example SLD, identify the main equipment and give the **function** of each item in a table that visually links each row to its **tag** on the drawing. | [training/module-01-equipment-identification.md](training/module-01-equipment-identification.md) |
| 2 | **Electrical Calculations** | Work through the main electrical **calculations** (demand, transformer sizing, FLC, short-circuit, voltage drop, PFC, cable selection) with worked examples. | [training/module-02-calculations.md](training/module-02-calculations.md) |
| 3 | **Single Points of Failure (SPOF)** | Identify and assess **single points of failure** across several example single-line diagrams and propose mitigations. | [training/module-03-spof-analysis.md](training/module-03-spof-analysis.md) |

Start with the **[Course Overview](training/00-course-overview.md)** for detailed per-module
outcomes, suggested study times, the team roles, the self-check approach, and a glossary.

---

## Diagrams & Reference

- **Master reference SLD:** [diagrams/sld-master-2MW.md](diagrams/sld-master-2MW.md) — the complete
  example single-line diagram used throughout Modules 1 and 2.
- **SPOF example diagrams:** [diagrams/spof-examples/](diagrams/spof-examples/) — a set of alternative
  single-line architectures used in Module 3 for failure-point analysis.
- **Reference design document:**
  [docs/main-electrical-equipment-2MW-process-plant.md](docs/main-electrical-equipment-2MW-process-plant.md)
  — the basis of design, equipment schedule, tag scheme and sizing logic underpinning the whole course.

---

## How to Use This Course

1. **Read the [Course Overview](training/00-course-overview.md)** and skim the
   [reference design doc](docs/main-electrical-equipment-2MW-process-plant.md) to absorb the
   tag scheme and sizing basis.
2. **Work the modules in order** (1 → 2 → 3). Each builds on the previous: identify the equipment,
   then size it, then assess where the architecture is vulnerable.
3. **Keep the [master SLD](diagrams/sld-master-2MW.md) open** alongside Modules 1 and 2 — the tags
   in the tables map directly onto the drawing.
4. **Attempt the self-checks** at the end of each module before reading the answers.
5. Treat every number as **indicative**: the value of the course is the **method**, not the specific ratings.

---

## Repository Layout

```text
Electrical/
├── README.md                                  ← course landing page (this file)
├── docs/
│   └── main-electrical-equipment-2MW-process-plant.md   ← reference / basis of design
├── training/
│   ├── 00-course-overview.md                  ← fuller course overview + glossary
│   ├── module-01-equipment-identification.md  ← Module 1: identify equipment + function table
│   ├── module-02-calculations.md              ← Module 2: main electrical calculations
│   └── module-03-spof-analysis.md             ← Module 3: single-points-of-failure analysis
└── diagrams/
    ├── sld-master-2MW.md                       ← master reference single-line diagram
    └── spof-examples/                          ← alternative SLDs for SPOF analysis
```

> Module content and diagrams are authored by other team members (electrical engineer and
> technical draftsman); this index and the course front matter define the structure they fill in.

---

*Design basis: ~2 MW process plant · 11 kV MV / 400 V LV · 50 Hz · IEC conventions.
All ratings indicative and to be confirmed.*
