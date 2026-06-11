#!/usr/bin/env python3
"""
build_manual.py — Field Manual Builder
Assembles fragment HTML files into a single self-contained manual.

Usage:
    python3 manual/build/build_manual.py [--rev N]

Run from the repo root (i.e. /path/to/Electrical/).
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (all relative to repo root, which is the expected working directory)
# ---------------------------------------------------------------------------
REPO_ROOT    = Path(__file__).resolve().parent.parent.parent  # Electrical/
BUILD_DIR    = Path(__file__).resolve().parent                 # Electrical/manual/build/
FRAGMENTS_DIR = BUILD_DIR / "fragments"
TEMPLATE     = BUILD_DIR / "template.html"
OUTPUT_DIR   = BUILD_DIR.parent                                # Electrical/manual/


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def parse_sections(html: str) -> list[dict]:
    """
    Return list of dicts {id, title, part, subsections: [{id, title}]}
    from top-level <section id="..." data-title="..." data-part="..."> elements.
    """
    sections = []
    section_pat = re.compile(
        r'<section\b[^>]*\bid=["\']([^"\']+)["\'][^>]*>',
        re.IGNORECASE | re.DOTALL,
    )
    title_pat   = re.compile(r'\bdata-title=["\']([^"\']*)["\']', re.IGNORECASE)
    part_pat    = re.compile(r'\bdata-part=["\']([^"\']*)["\']',  re.IGNORECASE)

    for m in section_pat.finditer(html):
        tag = m.group(0)
        sec_id    = m.group(1)
        title_m   = title_pat.search(tag)
        part_m    = part_pat.search(tag)
        sec_title = title_m.group(1) if title_m else sec_id
        sec_part  = part_m.group(1)  if part_m  else "Sections"

        # Find subsections (h3 with id) inside this section
        # Find the section body: from this <section> open tag to the next </section>
        start = m.start()
        # Find matching </section> — count nesting
        depth = 0
        pos = start
        end = len(html)
        open_sec  = re.compile(r'<section\b', re.IGNORECASE)
        close_sec = re.compile(r'</section\s*>', re.IGNORECASE)
        for tm in re.finditer(r'</?section\b[^>]*>', html[start:], re.IGNORECASE):
            tag_text = tm.group(0)
            if re.match(r'<section\b', tag_text, re.IGNORECASE):
                depth += 1
            else:
                depth -= 1
            if depth == 0:
                end = start + tm.end()
                break

        body = html[start:end]
        h3_pat = re.compile(r'<h3\b[^>]*\bid=["\']([^"\']+)["\'][^>]*>(.*?)</h3>', re.IGNORECASE | re.DOTALL)
        subsections = []
        for h3m in h3_pat.finditer(body):
            h3_id    = h3m.group(1)
            h3_title = re.sub(r'<[^>]+>', '', h3m.group(2)).strip()
            subsections.append({"id": h3_id, "title": h3_title})

        sections.append({
            "id":          sec_id,
            "title":       sec_title,
            "part":        sec_part,
            "subsections": subsections,
        })

    return sections


def build_nav(sections: list[dict]) -> str:
    """Build sidebar nav HTML grouped by data-part."""
    # Group sections by part, preserving order
    parts: dict[str, list[dict]] = {}
    part_order: list[str] = []
    for sec in sections:
        p = sec["part"]
        if p not in parts:
            parts[p] = []
            part_order.append(p)
        parts[p].append(sec)

    lines = []
    for part in part_order:
        part_id = re.sub(r'\W+', '-', part.lower()).strip('-')
        lines.append(f'<div class="nav-part" id="nav-part-{part_id}">')
        lines.append(f'  <div class="nav-part-header">'
                     f'<span>{part}</span>'
                     f'<span class="nav-part-toggle">▾</span>'
                     f'</div>')
        lines.append('  <ul class="nav-part-items">')
        for sec in parts[part]:
            lines.append(f'    <li class="nav-item">')
            lines.append(f'      <a href="#{sec["id"]}">{sec["title"]}</a>')
            if sec["subsections"]:
                lines.append('      <ul class="nav-sub-items">')
                for sub in sec["subsections"]:
                    lines.append(f'        <li class="nav-sub-item">'
                                 f'<a href="#{sub["id"]}">{sub["title"]}</a></li>')
                lines.append('      </ul>')
            lines.append('    </li>')
        lines.append('  </ul>')
        lines.append('</div>')

    return "\n".join(lines)


def inline_svgs(html: str, repo_root: Path, warnings: list[str]) -> tuple[str, int]:
    """
    Replace <div class="svg-embed" data-src="PATH"></div> with inline SVG.
    Returns (modified_html, count_inlined).
    """
    pattern = re.compile(
        r'<div\s+class=["\']svg-embed["\'][^>]*\bdata-src=["\']([^"\']+)["\'][^>]*>\s*</div>',
        re.IGNORECASE | re.DOTALL,
    )
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        src = m.group(1).strip()
        svg_path = repo_root / src

        if not svg_path.exists():
            msg = f"WARNING: SVG not found: {src} (path: {svg_path})"
            warnings.append(msg)
            print(msg, file=sys.stderr)
            return (
                f'<div class="svg-missing">'
                f'[SVG missing: <code>{src}</code>]'
                f'</div>'
            )

        try:
            svg_content = read_file(svg_path)
        except Exception as exc:
            msg = f"WARNING: Could not read SVG {src}: {exc}"
            warnings.append(msg)
            print(msg, file=sys.stderr)
            return (
                f'<div class="svg-missing">'
                f'[SVG read error: <code>{src}</code>]'
                f'</div>'
            )

        # Strip XML declaration and DOCTYPE (not valid inside HTML5)
        svg_content = re.sub(r'<\?xml[^?]*\?>', '', svg_content)
        svg_content = re.sub(r'<!DOCTYPE[^>]*>', '', svg_content, flags=re.IGNORECASE)
        svg_content = svg_content.strip()

        count += 1
        return f'<div class="svg-wrapper">{svg_content}</div>'

    result = pattern.sub(replacer, html)
    return result, count


def inline_docs(html: str, repo_root: Path, warnings: list[str]) -> tuple[str, int]:
    """
    Replace <div class="doc-embed" data-src="PATH"></div> with an isolated,
    auto-sized <iframe srcdoc="..."> containing the full HTML of PATH.
    Keeps the manual a single self-contained file while fully isolating the
    embedded document's own styles. Returns (modified_html, count_embedded).
    """
    pattern = re.compile(
        r'<div\s+class=["\']doc-embed["\'][^>]*\bdata-src=["\']([^"\']+)["\'][^>]*>\s*</div>',
        re.IGNORECASE | re.DOTALL,
    )
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        src = m.group(1).strip()
        doc_path = repo_root / src
        if not doc_path.exists():
            msg = f"WARNING: doc-embed not found: {src} (path: {doc_path})"
            warnings.append(msg)
            print(msg, file=sys.stderr)
            return f'<div class="svg-missing">[document missing: <code>{src}</code>]</div>'
        content = read_file(doc_path)
        # Escape only what a double-quoted srcdoc attribute requires.
        esc = content.replace("&", "&amp;").replace('"', "&quot;")
        count += 1
        return (
            '<iframe class="doc-embed-frame" title="Embedded study document" loading="lazy" '
            'style="width:100%;border:1px solid #c9cfd6;border-radius:6px;background:#fff;min-height:600px;" '
            'onload="try{this.style.height=(this.contentWindow.document.documentElement.scrollHeight+32)+&#39;px&#39;;}catch(e){}" '
            f'srcdoc="{esc}"></iframe>'
        )

    return pattern.sub(replacer, html), count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the field manual HTML.")
    parser.add_argument("--rev", type=str, default="0", help="Revision label (e.g. 0, 2, 3b)")
    args = parser.parse_args()
    rev = args.rev

    warnings: list[str] = []

    # 1. Load template
    if not TEMPLATE.exists():
        sys.exit(f"ERROR: template not found: {TEMPLATE}")
    template = read_file(TEMPLATE)

    # 2. Collect fragments
    if not FRAGMENTS_DIR.exists():
        sys.exit(f"ERROR: fragments directory not found: {FRAGMENTS_DIR}")

    fragment_files = sorted(FRAGMENTS_DIR.glob("*.html"))
    if not fragment_files:
        warnings.append("WARNING: No fragment files found in " + str(FRAGMENTS_DIR))

    print(f"Found {len(fragment_files)} fragment(s):")
    for ff in fragment_files:
        print(f"  {ff.name}")

    # 3. Concatenate fragment content
    combined_html = ""
    for ff in fragment_files:
        combined_html += read_file(ff) + "\n"

    # 4. Parse sections for nav
    sections = parse_sections(combined_html)
    print(f"\nParsed {len(sections)} section(s):")
    for sec in sections:
        n_sub = len(sec["subsections"])
        print(f"  [{sec['part']}] #{sec['id']} — {sec['title']}"
              + (f" ({n_sub} subsection{'s' if n_sub != 1 else ''})" if n_sub else ""))

    # 5. Build nav HTML
    nav_html = build_nav(sections)

    # 5b. Mark the FIRST section of each Part so print can page-break per Part
    #     (not per section — avoids many half-empty printed pages).
    first_ids: set[str] = set()
    seen_parts: set[str] = set()
    for sec in sections:
        if sec["part"] not in seen_parts:
            seen_parts.add(sec["part"])
            first_ids.add(sec["id"])

    def _mark_part_start(m: re.Match) -> str:
        tag = m.group(0)
        sid = m.group(1)
        if sid in first_ids and "data-part-start" not in tag:
            return tag[:-1] + ' data-part-start="1">'
        return tag

    combined_html = re.sub(
        r'<section\b[^>]*\bid=["\']([^"\']+)["\'][^>]*>',
        _mark_part_start, combined_html,
    )

    # 6. Inline SVGs and embedded documents
    combined_html, svg_count = inline_svgs(combined_html, REPO_ROOT, warnings)
    combined_html, doc_count = inline_docs(combined_html, REPO_ROOT, warnings)

    # 7. Assemble final HTML
    out = template

    # Inject revision badge
    out = out.replace("<!--REV-->", f"Rev {rev}")

    # Inject nav
    out = out.replace("<!--NAV-->", nav_html)

    # Inject content
    out = out.replace("<!--CONTENT-->", combined_html)

    # 8. Write output
    output_filename = f"manual-rev{rev}.html"
    output_path     = OUTPUT_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(out)

    size_kb = output_path.stat().st_size / 1024

    # 9. Summary
    print(f"\n{'='*60}")
    print(f"BUILD SUMMARY")
    print(f"{'='*60}")
    print(f"  Fragments     : {len(fragment_files)}")
    print(f"  Sections      : {len(sections)}")
    print(f"  SVGs inlined  : {svg_count}")
    print(f"  Docs embedded : {doc_count}")
    print(f"  Revision      : Rev {rev}")
    print(f"  Output        : {output_path}")
    print(f"  Output size   : {size_kb:.1f} kB")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")
    else:
        print(f"\nNo warnings.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
