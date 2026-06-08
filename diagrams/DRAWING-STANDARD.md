# Drawing Standard — Single-Line Diagrams

This document defines the **format and conventions** for every single-line diagram
(SLD) in this repository, so that all figures are consistent, reproducible and of
technical-book quality.

## 1. Toolchain & format

| Aspect | Standard |
|--------|----------|
| Authoring | **Python + [schemdraw](https://schemdraw.readthedocs.io)** (matplotlib backend) |
| Symbol library | `diagrams/src/slddraw.py` — custom **IEC 60617** power symbols |
| Source of each figure | a build script in `diagrams/src/` (`build_master.py`, `build_spof.py`) |
| Output (committed) | **SVG** in `diagrams/svg/` (vector, embedded in Markdown) + a PNG for review |
| Graphical standard | **IEC 60617** symbols; **IEC** ratings (11 kV / 400 V, 50 Hz) |

**Principle:** the *source script is the master*, the SVG is a build artefact.
Never hand-edit an SVG — change the script and re-render so figures stay reproducible
and diff-able.

## 2. How to build

```bash
cd diagrams/src
pip install schemdraw matplotlib cairosvg     # one-time
python3 build_master.py        # -> ../svg/sld-master-2MW.svg (+ .png)
python3 build_spof.py          # -> ../svg/spof-A..E.svg (+ .png)
```

Embed in Markdown with a relative path, e.g. `![alt](svg/sld-master-2MW.svg)`.

## 3. Symbol library (`slddraw.py`)

| Symbol | Class / helper | IEC representation |
|--------|----------------|--------------------|
| Utility / grid source | `UtilitySource` | circle with AC sine |
| Circuit breaker | `Breaker(kind, orient)` | solid square = closed, hollow = open/N.O.; `orient='h'` for bus-section/tie |
| Isolator / disconnector | `Disconnect` | open knife contact |
| Fuse | `Fuse` | rectangle on the conductor |
| Two-winding transformer | `Transformer2W` | two interlinked circles (Dyn11) |
| Neutral earthing resistor | `NER` | resistor in series to earth |
| Earth | `Ground` | three diminishing bars |
| Capacitor bank (PFC) | `Capacitor` | two parallel plates |
| Motor / generator | `Motor` / `Generator` | circle with `M` / `G` |
| Equipment block | `Block(name, sub, fill)` | labelled rectangle (MCC, VFD, UPS, ATS, DB…) |
| Busbar | `busbar(...)` | heavy horizontal line |
| Connector / node | `wire(...)` / `dot(...)` | conductor / junction dot |

Every inline device exposes `N` (top) and `S` (bottom) terminals; blocks expose
`N/S/E/W/center`. Place with `place(d, Element(), (x, y), anchor=...)` and connect
with `wire(d, p0, p1)`.

> **Note:** schemdraw treats a `label=` kwarg as an auto-drawn label. The `Block`
> equipment label parameter is therefore named **`name=`** (not `label=`) to avoid
> a double-rendered caption.

## 4. Style rules

- **Power flow** is **top-to-bottom**: utility at top, loads at the bottom.
- **Voltage colour accents:** MV busbars **firebrick** (`#b22222`), LV busbars
  **navy** (`#11457e`); all devices/conductors otherwise **near-black** (`#111111`).
- **Line weights:** conductors `1.6`, busbars `6`.
- **Font:** DejaVu Sans; base size `11`; tags `~10-12`, notes `~8`.
- **Tags** (bold-ish, full size) name equipment using the **repo tag scheme**
  (`MV-SWGR`, `TX-1/TX-2`, `LV-MSB`, `MCC`, `VFD`, `PFC`, `DG`, `ATS`, `UPS`,
  `NER`, `52-x`, `ACB/MCCB`…); **notes** (grey, small) carry ratings/comments.
- **SPOF marking:** a red (`#cc0000`) dashed ring around the failure point plus a
  red caption; a resilient/contrast layout uses green (`#1a7f37`).
- **ASCII only** in any text drawn into a figure — schemdraw's text sizing breaks
  on some glyphs (`&`, `↔`, `×`, `·`). Use `-`, `/`, `x`, `~` instead.

## 5. Tag ↔ drawing links

The master SLD's **Tag Legend** gives every tag an HTML anchor
(`<a id="mv-swgr"></a>MV-SWGR`). Training modules deep-link to those anchors, e.g.
`[MV-SWGR](../diagrams/sld-master-2MW.md#mv-swgr)`. **Preserve the anchors** when
editing the legend.

## 6. Adding a new diagram

1. Add/compose symbols in a new or existing build script in `diagrams/src/`.
2. Reuse `slddraw` symbols and the colours/weights above — do not invent new styles.
3. Render to `diagrams/svg/<name>.svg` (+ `.png`).
4. Embed the SVG in the relevant Markdown with a relative path and a caption.
5. If it introduces equipment tags, keep them consistent with the reference design
   doc and the master legend.

*All figures are concept-level and indicative; ratings to be confirmed by detailed
load, short-circuit and protection studies.*
