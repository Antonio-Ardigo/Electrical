"""
slddraw — a small IEC 60617 single-line-diagram symbol library built on schemdraw.

Provides reusable, book-quality power one-line symbols (utility source, circuit
breaker, two-winding transformer, busbar, NER, generator, motor, capacitor, and
labelled equipment blocks such as MCC / VFD / UPS / ATS / DB) plus a couple of
layout helpers.

Design conventions (see diagrams/DRAWING-STANDARD.md):
  * Monochrome, IEC 60617 symbols, vertical (top-to-bottom) power flow.
  * Every inline device exposes 'N' (top) and 'S' (bottom) terminals.
  * Blocks expose 'N','S','E','W','center'.
  * Place with .at(point).anchor(<anchor>); connect with wire().
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import schemdraw
from schemdraw import elements as elm
from schemdraw.segments import (
    Segment, SegmentCircle, SegmentText, SegmentPoly,
)

# ----------------------------------------------------------------------------
# Global drawing style
# ----------------------------------------------------------------------------
LW = 1.6          # standard conductor / symbol line width
BUS_LW = 6        # busbar line width
COLOR = "#111111"
MV_COLOR = "#b22222"   # firebrick — medium-voltage accent
LV_COLOR = "#11457e"   # navy — low-voltage accent
FONT = "DejaVu Sans"
FS = 11           # base font size

schemdraw.config(lw=LW, font=FONT, fontsize=FS, color=COLOR)


# ----------------------------------------------------------------------------
# Inline devices (two terminal: N at top, S at bottom)
# ----------------------------------------------------------------------------
class Breaker(elm.Element):
    """Withdrawable circuit breaker — IEC one-line square on the conductor.

    `kind`: 'closed' (solid square) or 'open'/'no' (hollow square).
    `orient`: 'v' (vertical, N/S terminals) or 'h' (horizontal, W/E terminals).
    """
    def __init__(self, *args, length=1.4, side=0.42, kind="closed",
                 orient="v", **kwargs):
        super().__init__(*args, **kwargs)
        h = length / 2
        s = side / 2
        fill = COLOR if kind == "closed" else "white"

        def maybe_swap(pts):
            return pts if orient == "v" else [(y, x) for (x, y) in pts]

        self.segments.append(Segment(maybe_swap([(0, h), (0, s)])))
        self.segments.append(Segment(maybe_swap([(0, -s), (0, -h)])))
        self.segments.append(SegmentPoly(
            maybe_swap([(-s, -s), (s, -s), (s, s), (-s, s)]), closed=True,
            fill=fill, zorder=3))
        if orient == "v":
            self.anchors.update({"N": (0, h), "S": (0, -h),
                                 "E": (s, 0), "W": (-s, 0)})
            self.params["drop"] = (0, -h)
        else:
            self.anchors.update({"W": (-h, 0), "E": (h, 0),
                                 "N": (0, s), "S": (0, -s)})
            self.params["drop"] = (h, 0)
        self.anchors["center"] = (0, 0)
        self.params["theta"] = 0


class Disconnect(elm.Element):
    """Isolator / disconnector — open knife contact (IEC)."""
    def __init__(self, *args, length=1.4, **kwargs):
        super().__init__(*args, **kwargs)
        h = length / 2
        self.segments.append(Segment([(0, h), (0, 0.28)]))
        self.segments.append(SegmentCircle((0, 0.28), 0.05, fill=COLOR))
        self.segments.append(Segment([(0, 0.28), (0.34, -0.22)]))   # blade
        self.segments.append(SegmentCircle((0, -0.28), 0.05, fill=COLOR))
        self.segments.append(Segment([(0, -0.28), (0, -h)]))
        self.anchors["N"] = (0, h)
        self.anchors["S"] = (0, -h)
        self.params["theta"] = 0
        self.params["drop"] = (0, -h)


class Fuse(elm.Element):
    """Fuse — IEC rectangle with through-line."""
    def __init__(self, *args, length=1.4, w=0.30, h=0.6, **kwargs):
        super().__init__(*args, **kwargs)
        L = length / 2
        self.segments.append(Segment([(0, L), (0, h / 2)]))
        self.segments.append(Segment([(0, -h / 2), (0, -L)]))
        self.segments.append(SegmentPoly(
            [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)],
            closed=True, fill="white"))
        self.segments.append(Segment([(0, h / 2), (0, -h / 2)]))
        self.anchors["N"] = (0, L)
        self.anchors["S"] = (0, -L)
        self.params["theta"] = 0
        self.params["drop"] = (0, -L)


class Transformer2W(elm.Element):
    """Two-winding transformer — IEC two interlinked circles (vertical)."""
    def __init__(self, *args, r=0.42, lead=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        gap = r * 0.85
        cyt = gap            # top (primary) circle centre y
        cyb = -gap           # bottom (secondary) circle centre y
        top = cyt + r + lead
        bot = cyb - r - lead
        self.segments.append(Segment([(0, top), (0, cyt + r)]))
        self.segments.append(SegmentCircle((0, cyt), r))
        self.segments.append(SegmentCircle((0, cyb), r))
        self.segments.append(Segment([(0, cyb - r), (0, bot)]))
        self.anchors["N"] = (0, top)
        self.anchors["S"] = (0, bot)
        self.anchors["E"] = (r, 0)
        self.anchors["W"] = (-r, 0)
        self.anchors["center"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, bot)


class NER(elm.Element):
    """Neutral earthing resistor — resistor in series to earth."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # horizontal lead-in then resistor going down to ground
        self.segments.append(Segment([(0, 0), (0, -0.35)]))
        self.segments.append(SegmentPoly(
            [(-0.16, -0.35), (0.16, -0.35), (0.16, -0.95), (-0.16, -0.95)],
            closed=True, fill="white"))
        self.segments.append(Segment([(0, -0.95), (0, -1.25)]))
        # earth symbol
        for i, wdt in enumerate((0.30, 0.19, 0.09)):
            y = -1.25 - i * 0.11
            self.segments.append(Segment([(-wdt, y), (wdt, y)]))
        self.anchors["N"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, 0)


class Ground(elm.Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([(0, 0), (0, -0.25)]))
        for i, wdt in enumerate((0.30, 0.19, 0.09)):
            y = -0.25 - i * 0.11
            self.segments.append(Segment([(-wdt, y), (wdt, y)]))
        self.anchors["N"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, 0)


class Capacitor(elm.Element):
    """Capacitor bank (PFC) — IEC two-plate symbol."""
    def __init__(self, *args, length=1.2, **kwargs):
        super().__init__(*args, **kwargs)
        L = length / 2
        self.segments.append(Segment([(0, L), (0, 0.1)]))
        self.segments.append(Segment([(-0.32, 0.1), (0.32, 0.1)]))
        self.segments.append(Segment([(-0.32, -0.1), (0.32, -0.1)]))
        self.segments.append(Segment([(0, -0.1), (0, -L)]))
        self.anchors["N"] = (0, L)
        self.anchors["S"] = (0, -L)
        self.params["theta"] = 0
        self.params["drop"] = (0, -L)


# ----------------------------------------------------------------------------
# Rotating machines and sources (round symbols)
# ----------------------------------------------------------------------------
class _RoundMachine(elm.Element):
    def __init__(self, letter, *args, r=0.5, lead=0.45, **kwargs):
        super().__init__(*args, **kwargs)
        top = r + lead
        self.segments.append(Segment([(0, top), (0, r)]))
        self.segments.append(SegmentCircle((0, 0), r))
        self.segments.append(SegmentText((0, 0), letter, fontsize=FS + 3))
        self.anchors["N"] = (0, top)
        self.anchors["S"] = (0, -r)
        self.anchors["center"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, -r)


class Motor(_RoundMachine):
    def __init__(self, *args, **kwargs):
        super().__init__("M", *args, **kwargs)


class Generator(_RoundMachine):
    def __init__(self, *args, **kwargs):
        super().__init__("G", *args, **kwargs)


class UtilitySource(elm.Element):
    """Utility / grid supply — circle with AC sine, arrow feeding down."""
    def __init__(self, *args, r=0.5, lead=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        # sine inside circle
        import numpy as np
        xs = np.linspace(-r * 0.6, r * 0.6, 40)
        ys = (r * 0.32) * np.sin(xs / (r * 0.6) * np.pi)
        self.segments.append(SegmentCircle((0, 0), r))
        self.segments.append(Segment(list(zip(xs, ys))))
        self.segments.append(Segment([(0, -r), (0, -r - lead)]))
        self.anchors["S"] = (0, -r - lead)
        self.anchors["center"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, -r - lead)


# ----------------------------------------------------------------------------
# Equipment blocks (rectangles with text)
# ----------------------------------------------------------------------------
class Block(elm.Element):
    """Generic labelled equipment block (MCC, VFD, UPS, ATS, DB, ...)."""
    def __init__(self, *args, name="", sub="",
                 w=1.9, h=1.1, fill="#eef2f7", lead=0.0, **kwargs):
        super().__init__(*args, **kwargs)
        x, y = w / 2, h / 2
        self.segments.append(SegmentPoly(
            [(-x, -y), (x, -y), (x, y), (-x, y)], closed=True,
            fill=fill, zorder=2))
        if name:
            self.segments.append(SegmentText(
                (0, 0.16 if sub else 0), name, fontsize=FS + 1,
                color=COLOR, zorder=4))
        if sub:
            self.segments.append(SegmentText(
                (0, -0.22), sub, fontsize=FS - 2, color="#444444", zorder=4))
        self.anchors["N"] = (0, y)
        self.anchors["S"] = (0, -y)
        self.anchors["E"] = (x, 0)
        self.anchors["W"] = (-x, 0)
        self.anchors["NW"] = (-x, y)
        self.anchors["NE"] = (x, y)
        self.anchors["center"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, -y)


# ----------------------------------------------------------------------------
# Busbar + layout helpers
# ----------------------------------------------------------------------------
def busbar(d, x0, x1, y, color=COLOR, lw=BUS_LW, label=None, label_dx=-0.2):
    """Draw a horizontal busbar from x0..x1 at height y. Returns y."""
    d += elm.Line().at((x0, y)).to((x1, y)).linewidth(lw).color(color)
    if label:
        d += elm.Label().at((x0 + label_dx, y + 0.22)).label(
            label, halign="right", fontsize=FS - 1, color=color)
    return y


def wire(d, p0, p1, lw=LW, color=COLOR):
    """Orthogonal-friendly straight connector between two points."""
    d += elm.Line().at(p0).to(p1).linewidth(lw).color(color)


def dot(d, p, color=COLOR):
    d += elm.Dot(radius=0.07).at(p).color(color)


def place(d, element, at, anchor="N"):
    """Place an element with its <anchor> at point <at>; return placed element."""
    return d.add(element.at(at).anchor(anchor))


# ----------------------------------------------------------------------------
# Standard project parameters + title block (shared across every figure)
# ----------------------------------------------------------------------------
# Saudi / SEC edition (Rev 3b).  ASCII-only — see DRAWING-STANDARD.md.
REV = "Rev 3b"
PARAM_STRIP = "13.8 kV / 400-230 V / 60 Hz / 50 degC amb"
STD_NOTE = "IEC 60617 - indicative"


def title_block(d, x_left, x_right, y_top, title, dwg_no,
                subtitle=None, color=COLOR):
    """Draw a tidy, consistent title block as a bordered band.

    Spans x_left..x_right; its top edge sits at y_top (block grows downward by
    ~1.0 unit). Carries: drawing title, drawing number, Rev, the standard note
    and the project parameter strip. ASCII-only.
    """
    h = 1.35 if subtitle else 1.05
    y_bot = y_top - h
    xm = 0.18                      # internal text margin
    # outer frame.  Pin the rect at the origin with theta=0 so its absolute
    # corner coordinates are not offset/rotated by the drawing cursor.
    d += elm.Rect(corner1=(x_left, y_bot), corner2=(x_right, y_top)).at(
        (0, 0)).theta(0).color("#888888").linewidth(1.1).fill(
        "#fbfbfb").zorder(0)
    # vertical divider for the right-hand metadata cell
    x_div = x_right - 3.9
    d += elm.Line().at((x_div, y_bot)).to((x_div, y_top)).color(
        "#bbbbbb").linewidth(0.9)
    # left cell: title, optional subtitle, then the parameter strip (stacked,
    # evenly spaced, never overlapping)
    d += elm.Label().at((x_left + xm, y_top - 0.34)).label(
        title, halign="left", fontsize=FS - 1, color=color)
    if subtitle:
        d += elm.Label().at((x_left + xm, y_top - 0.72)).label(
            subtitle, halign="left", fontsize=FS - 3, color="#555555")
    d += elm.Label().at((x_left + xm, y_bot + 0.22)).label(
        PARAM_STRIP, halign="left", fontsize=FS - 2, color="#333333")
    # right cell: drawing number / rev / standard note
    xr = x_div + xm
    d += elm.Label().at((xr, y_top - 0.32)).label(
        dwg_no, halign="left", fontsize=FS - 2, color=COLOR)
    d += elm.Label().at((xr, y_top - 0.66)).label(
        REV, halign="left", fontsize=FS - 2, color=color)
    d += elm.Label().at((xr, y_bot + 0.24)).label(
        STD_NOTE, halign="left", fontsize=FS - 3, color="#555555")
    return y_bot
