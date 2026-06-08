"""Generate the five SPOF example single-line diagrams as SVG (+ PNG).

Outputs diagrams/svg/spof-A..E.svg
Run:  python3 build_spof.py
"""
import os
import schemdraw
from schemdraw import elements as elm
from schemdraw.segments import SegmentCircle
import slddraw as s

OUT = os.path.join(os.path.dirname(__file__), "..", "svg")
FS = s.FS
RED = "#cc0000"
GREEN = "#1a7f37"


def tag(d, p, t, ha="left", size=FS, color=s.COLOR):
    d += elm.Label().at(p).label(t, halign=ha, fontsize=size, color=color)


def note(d, p, t, ha="left", size=FS - 3, color="#555555"):
    d += elm.Label().at(p).label(t, halign=ha, fontsize=size, color=color)


class _Ring(elm.Element):
    def __init__(self, *a, r=0.6, color=RED, **k):
        super().__init__(*a, **k)
        self.segments.append(SegmentCircle((0, 0), r, color=color, lw=1.8, ls="--"))
        self.anchors["center"] = (0, 0)
        self.params["theta"] = 0
        self.params["drop"] = (0, 0)


def spof(d, p, text="SPOF", r=0.6, lbldx=0.0, lbldy=0.92, color=RED, ha="center"):
    d.add(_Ring(r=r, color=color).at(p).anchor("center"))
    d += elm.Label().at((p[0] + lbldx, p[1] + lbldy)).label(
        text, halign=ha, fontsize=FS - 1, color=color)


def vbrk(d, x, yc, kind="closed", label=None):
    s.place(d, s.Breaker(kind=kind), (x, yc), anchor="center")
    if label:
        tag(d, (x + 0.28, yc + 0.05), label, size=FS - 2)
    return yc + 0.6, yc - 0.6


def title(d, x, y, t, sub):
    tag(d, (x, y), t, ha="center", size=FS + 1)
    note(d, (x, y - 0.34), sub, ha="center", size=FS - 2)


def source_to_mvbus(d, x, y_src, y_brk, y_bus, bl, br, label="52-I"):
    s.place(d, s.UtilitySource(r=0.4), (x, y_src), anchor="center")
    note(d, (x + 0.5, y_src), "11 kV", size=FS - 2)
    s.wire(d, (x, y_src - 0.8), (x, y_brk + 0.6))
    vbrk(d, x, y_brk, label=label)
    s.wire(d, (x, y_brk - 0.6), (x, y_bus))
    s.dot(d, (x, y_bus))
    s.busbar(d, bl, br, y_bus, color=s.MV_COLOR)


def tx_drop(d, x, y_bus, y_tx, y_acb, y_lvbus, txlabel):
    s.dot(d, (x, y_bus))
    s.wire(d, (x, y_bus), (x, y_tx + 1.0), color=s.MV_COLOR)
    s.place(d, s.Transformer2W(r=0.38), (x, y_tx), anchor="center")
    tag(d, (x + 0.5, y_tx + 0.12), txlabel, size=FS - 1)
    note(d, (x + 0.5, y_tx - 0.16), "1600 kVA", size=FS - 3)
    s.wire(d, (x, y_tx - 1.0), (x, y_acb + 0.6))
    vbrk(d, x, y_acb)
    s.wire(d, (x, y_acb - 0.6), (x, y_lvbus))
    s.dot(d, (x, y_lvbus))


def lv_feeder(d, x, y_lvbus, y_eq, name, sub, fill="#eef2f7"):
    s.dot(d, (x, y_lvbus))
    s.wire(d, (x, y_lvbus), (x, y_eq + 1.05), color=s.LV_COLOR)
    vbrk(d, x, y_eq + 0.55)
    s.place(d, s.Block(name=name, sub=sub, w=1.7, h=1.0, fill=fill),
            (x, y_eq), anchor="center")


def save(d, stem):
    d.save(os.path.join(OUT, stem + ".svg"))
    d.save(os.path.join(OUT, stem + ".png"), dpi=130)


# ============================================================ A
def diagram_A():
    d = schemdraw.Drawing(); d.config(unit=1, fontsize=FS)
    source_to_mvbus(d, 0, 8.2, 7.2, 6.4, -1.2, 1.2)
    tx_drop(d, 0, 6.4, 5.0, 3.6, 2.7, "TX-1")
    s.busbar(d, -2.6, 2.6, 2.7, color=s.LV_COLOR)
    tag(d, (-2.6, 2.7 + 0.3), "LV-MSB  -  single bus", size=FS - 1, color=s.LV_COLOR)
    lv_feeder(d, -1.6, 2.7, 1.2, "MCC", "motors")
    lv_feeder(d, 1.6, 2.7, 1.2, "DB", "light/pwr")
    spof(d, (0, 5.0), "SPOF: single TX\n+ single bus", r=0.7, lbldx=1.6, lbldy=0.0, ha="left")
    title(d, 0, -0.4, "SPOF-A  -  Single transformer, single bus",
          "Any loss of TX-1, its feeder, the incomer or the bus blacks out the whole plant.")
    save(d, "spof-A")


# ============================================================ B
def diagram_B():
    d = schemdraw.Drawing(); d.config(unit=1, fontsize=FS)
    source_to_mvbus(d, 0, 8.6, 7.6, 6.8, -3.2, 3.2)
    tx_drop(d, -3.0, 6.8, 5.4, 4.0, 3.1, "TX-1")
    tx_drop(d, 3.0, 6.8, 5.4, 4.0, 3.1, "TX-2")
    s.busbar(d, -4.8, -1.2, 3.1, color=s.LV_COLOR)
    s.busbar(d, 1.2, 4.8, 3.1, color=s.LV_COLOR)
    note(d, (-4.8, 3.1 - 0.4), "Bus A", size=FS - 2, color=s.LV_COLOR)
    note(d, (4.8, 3.1 - 0.4), "Bus B", ha="right", size=FS - 2, color=s.LV_COLOR)
    lv_feeder(d, -3.0, 3.1, 1.5, "MCC-1", "Bus A loads")
    lv_feeder(d, 3.0, 3.1, 1.5, "MCC-2", "Bus B loads")
    # no tie
    note(d, (0, 3.1), "NO TIE", ha="center", size=FS - 1, color=RED)
    spof(d, (-3.0, 5.4), "lose TX-1\n= lose Bus A", r=0.65, lbldx=-1.45, lbldy=0.0, ha="right")
    spof(d, (3.0, 5.4), "lose TX-2\n= lose Bus B", r=0.65, lbldx=1.45, lbldy=0.0, ha="left")
    title(d, 0, -0.3, "SPOF-B  -  Two transformers, no bus-tie",
          "Redundant sources, but no tie: a single source loss drops its entire half of the plant.")
    save(d, "spof-B")


# ============================================================ C
def diagram_C():
    d = schemdraw.Drawing(); d.config(unit=1, fontsize=FS)
    source_to_mvbus(d, 0, 8.6, 7.6, 6.8, -3.2, 3.2, label="52-I")
    tx_drop(d, -3.0, 6.8, 5.4, 4.0, 3.1, "TX-1")
    tx_drop(d, 3.0, 6.8, 5.4, 4.0, 3.1, "TX-2")
    s.busbar(d, -4.8, -0.7, 3.1, color=s.LV_COLOR)
    s.busbar(d, 0.7, 4.8, 3.1, color=s.LV_COLOR)
    s.wire(d, (-0.7, 3.1), (-0.5, 3.1), color=s.LV_COLOR)
    s.wire(d, (0.7, 3.1), (0.5, 3.1), color=s.LV_COLOR)
    s.place(d, s.Breaker(kind="no", orient="h"), (0, 3.1), anchor="center")
    note(d, (0, 3.1 + 0.4), "tie (N.O.)", ha="center", size=FS - 3)
    lv_feeder(d, -3.0, 3.1, 1.5, "MCC-1", "Bus A loads")
    lv_feeder(d, 3.0, 3.1, 1.5, "MCC-2", "Bus B loads")
    spof(d, (0, 7.6), "SPOF: single incomer\n+ single MV bus", r=0.7, lbldx=1.6, lbldy=0.0, ha="left")
    title(d, 0, -0.3, "SPOF-C  -  Single utility incomer / MV bus",
          "LV redundancy is fine, but one incomer or MV-bus fault still blacks out everything.")
    save(d, "spof-C")


# ============================================================ D
def diagram_D():
    d = schemdraw.Drawing(); d.config(unit=1, fontsize=FS)
    # two healthy sources / buses (abbreviated) feeding one common MCC
    s.busbar(d, -3.2, 3.2, 7.0, color=s.LV_COLOR)
    tag(d, (-3.2, 7.0 + 0.3), "LV-MSB (dual-fed, healthy)", size=FS - 1, color=s.LV_COLOR)
    note(d, (-3.2, 7.0 - 0.4), "redundant upstream", size=FS - 3)
    s.dot(d, (0, 7.0))
    s.wire(d, (0, 7.0), (0, 6.0), color=s.LV_COLOR)
    vbrk(d, 0, 5.4, label="single MCCB")
    s.wire(d, (0, 4.8), (0, 4.2))
    note(d, (0.3, 4.5), "single shared cable", size=FS - 3, color=RED)
    s.place(d, s.Block(name="MCC", sub="one board", w=2.0, h=1.0), (0, 3.5), anchor="center")
    s.wire(d, (-1.0, 3.0), (1.0, 3.0))
    s.wire(d, (-1.0, 3.0), (-1.0, 2.4)); s.wire(d, (1.0, 3.0), (1.0, 2.4))
    s.place(d, s.Motor(r=0.34), (-1.0, 2.05), anchor="center")
    s.place(d, s.Motor(r=0.34), (1.0, 2.05), anchor="center")
    note(d, (-1.0, 1.4), "duty pump", ha="center", size=FS - 3)
    note(d, (1.0, 1.4), "standby pump", ha="center", size=FS - 3)
    spof(d, (0, 5.4), "SPOF: shared MCCB /\ncable / single MCC", r=0.7, lbldx=1.7, lbldy=0.2, ha="left")
    note(d, (0, 0.7), "Duty + standby share one board -> the standby gives no real redundancy.",
         ha="center", size=FS - 2, color="#333333")
    title(d, 0, 0.1, "SPOF-D  -  Shared cable / single MCC for duty + standby", "")
    save(d, "spof-D")


# ============================================================ E
def diagram_E():
    d = schemdraw.Drawing(); d.config(unit=1, fontsize=FS)
    # dual incomers + bus-section
    s.place(d, s.UtilitySource(r=0.36), (-2.2, 9.0), anchor="center")
    s.place(d, s.UtilitySource(r=0.36), (2.2, 9.0), anchor="center")
    note(d, (-2.2, 9.0 + 0.5), "Feed 1", ha="center", size=FS - 3)
    note(d, (2.2, 9.0 + 0.5), "Feed 2", ha="center", size=FS - 3)
    for xs in (-2.2, 2.2):
        s.wire(d, (xs, 8.6), (xs, 8.0))
        vbrk(d, xs, 7.6)
        s.wire(d, (xs, 7.0), (xs, 6.8))
        s.dot(d, (xs, 6.8))
    s.busbar(d, -3.4, -0.5, 6.8, color=s.MV_COLOR)
    s.busbar(d, 0.5, 3.4, 6.8, color=s.MV_COLOR)
    s.wire(d, (-0.5, 6.8), (-0.4, 6.8), color=s.MV_COLOR)
    s.wire(d, (0.5, 6.8), (0.4, 6.8), color=s.MV_COLOR)
    s.place(d, s.Breaker(kind="closed", orient="h"), (0, 6.8), anchor="center")
    note(d, (0, 6.8 + 0.4), "MV bus-section", ha="center", size=FS - 3)
    tx_drop(d, -2.2, 6.8, 5.4, 4.0, 3.1, "TX-1")
    tx_drop(d, 2.2, 6.8, 5.4, 4.0, 3.1, "TX-2")
    s.busbar(d, -3.7, -0.6, 3.1, color=s.LV_COLOR)
    s.busbar(d, 0.6, 3.7, 3.1, color=s.LV_COLOR)
    s.wire(d, (-0.6, 3.1), (-0.4, 3.1), color=s.LV_COLOR)
    s.wire(d, (0.6, 3.1), (0.4, 3.1), color=s.LV_COLOR)
    s.place(d, s.Breaker(kind="closed", orient="h"), (0, 3.1), anchor="center")
    note(d, (0, 3.1 + 0.38), "auto bus-tie", ha="center", size=FS - 3)
    note(d, (-3.7, 3.1 - 0.4), "Bus A", size=FS - 3, color=s.LV_COLOR)
    note(d, (3.7, 3.1 - 0.4), "Bus B", ha="right", size=FS - 3, color=s.LV_COLOR)
    s.wire(d, (-2.2, 3.1), (-2.2, 2.0)); s.place(d, s.Motor(r=0.32), (-2.2, 1.65), anchor="center")
    s.wire(d, (2.2, 3.1), (2.2, 2.0)); s.place(d, s.Motor(r=0.32), (2.2, 1.65), anchor="center")
    note(d, (-2.2, 1.0), "duty pump", ha="center", size=FS - 3)
    note(d, (2.2, 1.0), "standby pump", ha="center", size=FS - 3)
    note(d, (0, 1.9), "duty / standby on\nseparate buses", ha="center", size=FS - 3, color=GREEN)
    tag(d, (0, 10.4), "RESILIENT REFERENCE  -  no single point of failure", ha="center",
        size=FS, color=GREEN)
    title(d, 0, 0.2, "SPOF-E  -  Resilient layout (for contrast)",
          "Dual feeds, two transformers, bus-section + auto tie, segregated buses: every common element has an alternative path.")
    save(d, "spof-E")


for fn in (diagram_A, diagram_B, diagram_C, diagram_D, diagram_E):
    fn()
print("SPOF diagrams rendered:", os.listdir(OUT))
