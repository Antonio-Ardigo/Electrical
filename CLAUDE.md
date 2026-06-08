# CLAUDE.md

Guidance for Claude (and contributors) when working in this repository.

## What this repository is

A **self-paced training course** on the **main electrical equipment of a medium-voltage /
low-voltage (MV/LV) industrial process plant**, tentatively **~2 MW**. It is documentation
and teaching material — **there is no application code, build, or test suite**. The
"deliverables" are well-structured, technically accurate Markdown documents and ASCII
single-line diagrams (SLDs).

## How the course is organised

The course is built by three roles; keep their concerns separate when editing:

| Role | Owns | Files |
|------|------|-------|
| **Planner** (curriculum) | Course structure, index, overview, glossary | `README.md`, `training/00-course-overview.md` |
| **Technical draftsman** | Single-line diagrams + tag legends | `diagrams/sld-master-2MW.md`, `diagrams/spof-examples/*` |
| **Electrical engineer** | Technical content of the modules | `training/module-01..04-*.md` |

Reference basis of design (sizing logic, equipment schedule, tag scheme):
`docs/main-electrical-equipment-2MW-process-plant.md` — **read this first** before editing
anything; everything else must stay consistent with it.

### Repository layout

```text
Electrical/
├── README.md                                  course landing page / index
├── CLAUDE.md                                   this file
├── docs/
│   └── main-electrical-equipment-2MW-process-plant.md   basis of design (source of truth)
├── training/
│   ├── 00-course-overview.md                  overview, learning outcomes, glossary
│   ├── module-01-equipment-identification.md  identify equipment + function table (linked to tags)
│   ├── module-02-calculations.md              core electrical calculations + worked examples
│   ├── module-03-spof-analysis.md              single-point-of-failure analysis
│   └── module-04-control-philosophy.md         control philosophy & power management (DCS/PMS, renewables)
└── diagrams/
    ├── DRAWING-STANDARD.md                     SLD format/style spec (schemdraw, IEC 60617)
    ├── sld-master-2MW.md                       master reference SLD (embeds svg/, anchored legend)
    ├── spof-examples/                          alternative SLDs for SPOF analysis
    ├── src/                                    schemdraw source: slddraw.py + build_*.py
    └── svg/                                    rendered SVG/PNG figures (build artefacts)
```

The reusable **`electrical-draftsman`** subagent lives in `.claude/agents/`.

### Course flow (do not reorder without reason)

1. **Module 1 — Identification:** from the master SLD, identify each item and tabulate its
   **function**, with each table row linking to the equipment **tag** in the drawing.
2. **Module 2 — Calculations:** the main electrical calculations, with worked examples.
3. **Module 3 — SPOF:** identify single points of failure across several SLDs and propose mitigations.

## Conventions — keep these consistent everywhere

- **Standards/region:** IEC. **Voltages:** 11 kV MV, 400/415 V LV. **Frequency:** 50 Hz.
- **Sizing basis:** ~2 MW demand → ~2.35 MVA → **2 × 1600 kVA** transformers on a split LV bus
  with a normally-open bus-tie.
- **Tag scheme** (reuse exactly — do not invent new tags without updating the reference doc):
  `MV-MET`, `MV-SWGR`, `MV-NER`, `TX-1`/`TX-2`, `LV-MSB`, `MCC-1..n`, `VFD`, `PFC`, `DG`,
  `ATS`, `UPS`, `DCDB`, `DB`/`EDB`.
- **Tag ↔ drawing linking:** the master SLD gives each tag an HTML anchor (e.g.
  `<a id="mv-swgr"></a>MV-SWGR`). Module tables deep-link to those anchors
  (e.g. `[MV-SWGR](../diagrams/sld-master-2MW.md#mv-swgr)`). Preserve anchors when editing.
- **Diagrams:** professional **IEC 60617 vector SLDs** built with **schemdraw** from Python source in
  `diagrams/src/` (symbol library `slddraw.py`), rendered to **SVG** in `diagrams/svg/` and embedded in
  Markdown. The source script is the master — never hand-edit an SVG; re-render instead. Follow
  `diagrams/DRAWING-STANDARD.md`. For SLD work, use the **`electrical-draftsman`** agent
  (`.claude/agents/electrical-draftsman.md`).
- **Tone:** professional, concise, GitHub-flavored Markdown. Every numeric value is **indicative**;
  state that assumptions are tentative and to be confirmed by detailed studies.

## Editing guidance for Claude

- This is technical training material — **accuracy matters more than volume**. Prefer correct,
  clearly explained engineering over padding.
- When you change the tag scheme, sizing, or architecture, update **all** of: the reference doc,
  the master SLD legend, and any module tables that reference it. Keep cross-links valid.
- Worked calculations should show formula → substitution → result with units, and round sensibly.
- There is nothing to compile or run; "verification" means checking internal consistency:
  tags match across files, links resolve, and numbers agree with the reference doc.
- Do not commit or push unless asked. Development happens on the designated feature branch;
  `main` is the base.
