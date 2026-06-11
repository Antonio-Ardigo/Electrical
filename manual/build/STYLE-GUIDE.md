# Fragment Authoring Contract — Field Manual

This document is the authoritative style guide for content agents writing HTML fragments
for the field manual. Follow it exactly; the build pipeline and CSS/JS depend on these
conventions.

---

## 1. Fragment File Naming

Each fragment is a single `.html` file in `manual/build/fragments/`.
Name files with a numeric prefix that controls sort order, e.g.:

```
00-cover.html
10-mv-equipment.html
20-calculations.html
30-spof-analysis.html
40-recommendations.html
```

The builder reads fragments in **alphabetical / numeric sort order** — prefix accordingly.

---

## 2. Top-Level Structure

Each fragment = **exactly one** `<section>` element at the top level.

```html
<section id="kebab-slug" data-title="Title Case Name" data-part="Part N — Part Name">
  <!-- content here -->
</section>
```

| Attribute      | Required | Notes                                                                     |
|----------------|----------|---------------------------------------------------------------------------|
| `id`           | Yes      | Unique kebab-case slug; used for scroll anchors and checklist storage.    |
| `data-title`   | Yes      | Human-readable title — appears in the sidebar nav.                        |
| `data-part`    | Yes      | Part group name — nav groups entries under this heading.                  |

---

## 3. Headings

| Tag   | Purpose                  | Notes                                    |
|-------|--------------------------|------------------------------------------|
| `<h2>`| Section title            | Should repeat the `data-title` value.    |
| `<h3 id="subsection-slug">`| Sub-section  | Must have `id` to appear in sidebar nav. |
| `<h4>`| Minor heading            | No id required; not shown in nav.        |

Example:

```html
<section id="mv-equipment" data-title="MV Equipment" data-part="Part 1 — Identification">
  <h2>MV Equipment</h2>

  <h3 id="mv-metering">Metering</h3>
  <p>…</p>

  <h3 id="mv-switchgear">Switchgear</h3>
  <p>…</p>
</section>
```

---

## 4. Figures (SVG Diagrams)

```html
<figure class="fig">
  <div class="svg-embed" data-src="diagrams/svg/NAME.svg"></div>
  <figcaption>Fig 1 — Descriptive caption text</figcaption>
</figure>
```

- `data-src` is **relative to the repo root** (`Electrical/`).
- The builder inlines the SVG; if the file is missing, a visible warning placeholder is injected.
- Never embed `<img>` tags pointing to external files — the manual must be self-contained.

---

## 5. Callout Boxes

Four variants — use the appropriate class:

```html
<div class="note">Informational note — facts, context, definitions.</div>

<div class="tip">Practical tip — best practice, field hint.</div>

<div class="warning">Warning — hazard, common mistake, do-not-do.</div>

<div class="key">Key takeaway: the single most important point of this section.</div>
```

---

## 6. Worked Example Block

```html
<div class="worked">
  <h4>Worked example — Transformer sizing</h4>
  <p>Given a 2 MW load at 0.85 power factor:</p>
  <code class="formula">S = P / pf = 2000 kW / 0.85 = 2353 kVA</code>
  <p>Round up to the next standard size: <strong>2 × 1600 kVA</strong>.</p>
</div>
```

- Use `<code class="formula">` for inline formula lines; these render in a mono box.
- Show: formula → substitution → result with units.

---

## 7. Persistent Checklist

```html
<ul class="checklist">
  <li>Verify transformer nameplate voltage matches supply.</li>
  <li>Check earth-fault protection relay settings.</li>
  <li>Confirm bus-tie switch is normally open.</li>
</ul>
```

- Checkboxes and localStorage persistence are added automatically by the JS.
- A progress counter (e.g. "Progress: 2 / 5") is injected above the list.
- State is keyed by `section[id]` + item index — **each section id must be unique**.

---

## 8. Data Table

```html
<table class="tbl">
  <thead>
    <tr><th>Tag</th><th>Equipment</th><th>Rating</th><th>Notes</th></tr>
  </thead>
  <tbody>
    <tr><td>TX-1</td><td>Transformer 1</td><td>1600 kVA</td><td>Dyn11, 11/0.4 kV</td></tr>
    <tr><td>TX-2</td><td>Transformer 2</td><td>1600 kVA</td><td>Dyn11, 11/0.4 kV</td></tr>
  </tbody>
</table>
```

---

## 9. Form Table (Label + Value)

Use for data sheets, assessment forms, or specification cards:

```html
<table class="form">
  <tr><td>Site name</td><td>Indicative process plant</td></tr>
  <tr><td>Supply voltage</td><td>11 kV, 50 Hz</td></tr>
  <tr><td>Total demand</td><td>~2 MW</td></tr>
  <tr><td>Assessment date</td><td>_______________</td></tr>
</table>
```

- Left column = label (bold, grey background).
- Right column = value (white background).

---

## 10. Cross-References

Link to other sections by their `id`:

```html
See <a href="#spof-analysis">Part 3 — SPOF Analysis</a> for mitigation strategies.
```

Links within the same manual file always work; the manual is single-file.

---

## 11. Inline Code & Pre-formatted Text

```html
Tag <code>MV-SWGR</code> refers to the medium-voltage switchgear.

<pre><code>I_fault = V / (√3 × Z) = 11000 / (1.732 × 0.35) = 18.15 kA</code></pre>
```

---

## 12. What NOT to do

- Do **not** use `<link>`, `<script src="...">`, or any external references — the manual is
  offline and fully self-contained.
- Do **not** use `<img src="...">` for diagrams — use the `svg-embed` figure pattern instead.
- Do **not** duplicate `id` values — they break scrollspy and checklist state.
- Do **not** add `<html>`, `<head>`, or `<body>` tags — fragments are injected into the template.
- Do **not** add `<h1>` headings — `<h2>` is the section title level.

---

## 13. Quick Checklist for Authors

Before submitting a fragment, verify:

- [ ] File named with numeric prefix, e.g. `30-spof.html`
- [ ] Single top-level `<section id="…" data-title="…" data-part="…">`
- [ ] `<h2>` repeats the section title; all `<h3>` have unique `id` attributes
- [ ] All SVG figures use `<figure class="fig"><div class="svg-embed" data-src="…"></div>`
- [ ] No external links, `<img>` tags, or `<script>` / `<link>` elements
- [ ] No duplicate `id` values across all fragments
- [ ] Numbers are marked as indicative (e.g. "~2 MW", "indicative")

---

## 14. Rev 3 Addendum (Saudi / SEC edition)

### 14.1 Multiple sections per fragment (corrects §2)

A fragment contains **one or more** top-level `<section>` elements. All sections in
one fragment must share the same `data-part`. The builder parses every top-level
section for the nav.

### 14.2 Rev 3 electrical basis

The Rev 3 manual is localized to Saudi Arabia (SEC supply): **13.8 kV MV,
400/230 V LV, 60 Hz, TN-S, 50 °C design ambient**, standards cited as
SASO-adopted IEC + SEC Distribution Code / Saudi Grid Code / SBC 401.
Binding plant numbers live in the **Rev 3 Plant Data Card** inside
`.claude/agents/electrical-engineer.md` — use those values verbatim.

### 14.3 Drawing-basis note (mandatory under every electrical SLD figure)

The SVG diagrams still show the original 11 kV / 415 V / 50 Hz reference design.
Place this note immediately after the `<figcaption>` of every electrical SLD
figure, and before any embedded study document:

```html
<div class="warning drawing-basis"><strong>Drawing basis note.</strong> This diagram was
drawn for the original 11 kV / 415 V / 50 Hz reference design and has not been re-rendered.
For this Saudi (SEC) Rev 3 edition read 11 kV as 13.8 kV, 415 V as 400 V and 50 Hz as 60 Hz.
Topology, tags and protection philosophy are unchanged.</div>
```

### 14.3a Embedded documents (`div.doc-embed`)

`<div class="doc-embed" data-src="...">` embeds a standalone HTML document; the
builder inlines it as an iframe/srcdoc. The `data-src` path is relative to the
`manual/` directory. Every `doc-embed` must be preceded by a document-basis note
when the embedded document uses a different electrical basis from the Rev 3
plant data card.

### 14.4 Catalogue disclaimer (mandatory at the top of every `cat-` section)

```html
<div class="warning"><strong>Indicative catalogue data.</strong> Product families and typical
parameters are listed for training and familiarisation only, are approximate, and change with
manufacturer revisions. No part numbers are given; always obtain current certified data sheets
and SASO/SEC acceptance status from the manufacturer.</div>
```

### 14.5 Calculation pedagogy pattern (mandatory `<h4>` sub-headings)

Every calculation topic in Part 2 uses these canonical `<h4>` headings, in order:

1. `Why this exists`
2. `What goes wrong without it`
3. `Feel for the numbers`
4. `Worked calculation`
5. `Equipment settings`
6. `Equipment technology`
7. `Control`
8. `Sizing method`

Concept before math; complete worked calcs (formula → substitution → result with
units → sanity check); intuitive energy comparisons in "Feel for the numbers".

**Exemption:** sections badged "Reference" (e.g. the load-flow overview
`c-loadflow` in `30-part2-foundations.html`) are survey/reference material and
are exempt from the 8-heading pattern.

### 14.6 Section id prefixes

| Part | Prefix |
|------|--------|
| Front matter | `cover-` |
| Part 0 — Orientation | `orientation-` |
| Part 1 — Foundations | `f-` |
| Part 2 — Calculations | `c-` |
| Part 3 — SPOF Analysis & Reliability | `s-` |
| Part 4 — Philosophies, Modifications & Control | `p-` |
| Part 5 — Field Tools & Case Study | `t-` |
| Part 6 — Equipment Catalogues | `cat-` |
| Appendices | `a-` |
