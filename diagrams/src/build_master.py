"""Generate the master single-line diagram for the ~2 MW MV/LV process plant.

Outputs diagrams/svg/sld-master-2MW.svg (and .png for review).
Run:  python3 build_master.py
"""
import os
import schemdraw
from schemdraw import elements as elm
import slddraw as s

OUT = os.path.join(os.path.dirname(__file__), "..", "svg")
FS = s.FS


def tag(d, p, text, ha="left", size=FS, color=s.COLOR):
    d += elm.Label().at(p).label(text, halign=ha, fontsize=size, color=color)


def note(d, p, text, ha="left", size=FS - 3, color="#555555"):
    d += elm.Label().at(p).label(text, halign=ha, fontsize=size, color=color)


def vbreaker(d, x, yc, kind="closed", label=None, sub=None):
    """Vertical breaker centred at (x,yc). Returns (top_y, bot_y)."""
    s.place(d, s.Breaker(kind=kind), (x, yc), anchor="center")
    if label:
        tag(d, (x + 0.30, yc + 0.07), label, size=FS - 1)
    if sub:
        note(d, (x + 0.30, yc - 0.22), sub)
    return yc + 0.6, yc - 0.6


def build(d):
    d.config(unit=1, fontsize=FS)

    # ---------------- geometry ----------------
    Y_UTIL = 13.8
    Y_MET = 12.2
    Y_MVBUS = 10.2
    Y_TXFDR = 9.2
    Y_TX = 7.7
    Y_ACB = 6.2
    Y_LVBUS = 5.2
    Y_MCCB = 4.5
    Y_EQUIP = 3.5
    Y_LOAD = 1.4

    X_INC = 0.0
    X_BS = 1.4
    X_TX1, X_TX2 = -3.0, 3.0
    MV_L, MV_R = -4.8, 4.8
    LVA_L, LVA_R = -9.5, -1.4
    LVB_L, LVB_R = 1.4, 9.5

    # ---------------- utility, metering, incomer ----------------
    s.place(d, s.UtilitySource(), (X_INC, Y_UTIL), anchor="center")
    tag(d, (0.55, Y_UTIL + 0.12), "UTILITY")
    note(d, (0.55, Y_UTIL - 0.16), "13.8 kV  60 Hz", size=FS - 2)
    s.wire(d, (X_INC, Y_UTIL - 1.0), (X_INC, Y_MET + 0.45))
    s.place(d, s.Block(w=1.7, h=0.85, name="MV-MET", sub="kWh  CT/VT",
                       fill="#f3f3f3"), (X_INC, Y_MET), anchor="center")
    s.wire(d, (X_INC, Y_MET - 0.42), (X_INC, 11.3))
    t, b = vbreaker(d, X_INC, 11.0, kind="closed", label="52-I", sub="incomer")
    s.wire(d, (X_INC, t), (X_INC, 11.3))
    s.wire(d, (X_INC, b), (X_INC, Y_MVBUS))
    s.dot(d, (X_INC, Y_MVBUS))

    # ---------------- MV switchgear ----------------
    d += (elm.Line().at((MV_L - 0.4, Y_MVBUS + 1.55)).to((MV_R + 0.4, Y_MVBUS + 1.55))
          .color("#aaaaaa").linewidth(1).linestyle("--"))
    tag(d, (MV_L - 0.4, Y_MVBUS + 1.30), "MV-SWGR  -  13.8 kV switchgear",
        size=FS - 1, color=s.MV_COLOR)
    note(d, (MV_R + 0.4, Y_MVBUS + 1.30), "IEC 62271-200  -  25 kA", ha="right")
    # busbar split by the bus-section breaker
    s.busbar(d, MV_L, X_BS - 0.4, Y_MVBUS, color=s.MV_COLOR)
    s.busbar(d, X_BS + 0.4, MV_R, Y_MVBUS, color=s.MV_COLOR)
    s.place(d, s.Breaker(kind="closed", orient="h"), (X_BS, Y_MVBUS), anchor="center")
    note(d, (X_BS, Y_MVBUS - 0.45), "52-BS", ha="center")

    # NER off the left end of the MV bus
    s.dot(d, (MV_L + 0.4, Y_MVBUS))
    s.wire(d, (MV_L + 0.4, Y_MVBUS), (MV_L + 0.4, Y_MVBUS - 0.35), color=s.MV_COLOR)
    s.place(d, s.NER(), (MV_L + 0.4, Y_MVBUS - 0.35), anchor="N")
    tag(d, (MV_L + 0.4 - 0.30, Y_MVBUS - 0.55), "MV-NER", ha="right", size=FS - 2)

    # ---------------- transformer feeders + transformers ----------------
    for X_TX, txtag in ((X_TX1, "TX-1"), (X_TX2, "TX-2")):
        s.dot(d, (X_TX, Y_MVBUS))
        s.wire(d, (X_TX, Y_MVBUS), (X_TX, Y_TXFDR + 0.6), color=s.MV_COLOR)
        t, b = vbreaker(d, X_TX, Y_TXFDR, kind="closed", label="52-T", sub="87T")
        s.wire(d, (X_TX, b), (X_TX, Y_TX + 1.05), color=s.MV_COLOR)
        s.place(d, s.Transformer2W(), (X_TX, Y_TX), anchor="center")
        tag(d, (X_TX + 0.70, Y_TX + 0.34), txtag)
        note(d, (X_TX + 0.70, Y_TX + 0.06), "1600 kVA")
        note(d, (X_TX + 0.70, Y_TX - 0.22), "13.8/0.4 kV")
        note(d, (X_TX + 0.70, Y_TX - 0.46), "Dyn11  Z~6%")
        s.wire(d, (X_TX, Y_TX - 1.05), (X_TX, Y_ACB + 0.6))
        t2, b2 = vbreaker(d, X_TX, Y_ACB, kind="closed",
                          label="ACB-A" if X_TX < 0 else "ACB-B")
        s.wire(d, (X_TX, b2), (X_TX, Y_LVBUS))
        s.dot(d, (X_TX, Y_LVBUS))

    # ---------------- LV main switchboard (split bus + tie) ----------------
    s.busbar(d, LVA_L, LVA_R, Y_LVBUS, color=s.LV_COLOR)
    s.busbar(d, LVB_L, LVB_R, Y_LVBUS, color=s.LV_COLOR)
    tag(d, (LVA_L, Y_LVBUS + 0.32), "LV-MSB  -  400/230 V main switchboard (PCC)",
        size=FS - 1, color=s.LV_COLOR)
    note(d, (LVA_L, Y_LVBUS - 0.5), "Bus A", size=FS - 2, color=s.LV_COLOR)
    note(d, (LVB_R, Y_LVBUS - 0.5), "Bus B", ha="right", size=FS - 2, color=s.LV_COLOR)
    s.wire(d, (LVA_R, Y_LVBUS), (-0.6, Y_LVBUS), color=s.LV_COLOR)
    s.wire(d, (LVB_L, Y_LVBUS), (0.6, Y_LVBUS), color=s.LV_COLOR)
    s.place(d, s.Breaker(kind="no", orient="h"), (0, Y_LVBUS), anchor="center")
    note(d, (0, Y_LVBUS + 0.42), "BT  bus-tie (N.O.)", ha="center")

    # ---------------- outgoing feeders ----------------
    def feeder(x, block, sub, fill="#eef2f7"):
        s.dot(d, (x, Y_LVBUS))
        s.wire(d, (x, Y_LVBUS), (x, Y_MCCB + 0.6), color=s.LV_COLOR)
        t, b = vbreaker(d, x, Y_MCCB)
        s.wire(d, (x, b), (x, Y_EQUIP + 0.55))
        return s.place(d, s.Block(name=block, sub=sub, fill=fill),
                       (x, Y_EQUIP), anchor="center")

    X_MCC1, X_PFC, X_DBA = -7.8, -5.0, -2.6
    X_EDB, X_UPS, X_MCC2 = 2.6, 5.0, 7.8
    feeder(X_MCC1, "MCC-1", "IEC 61439")
    feeder(X_PFC, "PFC", "detuned 7%")
    feeder(X_DBA, "DB-A", "light / power")
    feeder(X_MCC2, "MCC-2", "IEC 61439")
    feeder(X_UPS, "UPS", "+ static bypass")
    feeder(X_EDB, "EDB", "essential")

    # ---------------- representative motors under the MCCs ----------------
    def motors(xc, specs, dx=1.3):
        xs = [xc - dx, xc, xc + dx]
        s.wire(d, (xc - dx, Y_EQUIP - 0.55), (xc + dx, Y_EQUIP - 0.55))
        for x, (start, duty) in zip(xs, specs):
            s.wire(d, (x, Y_EQUIP - 0.55), (x, Y_LOAD + 1.05))
            note(d, (x, Y_LOAD + 0.78), start, ha="center")
            s.place(d, s.Motor(r=0.34), (x, Y_LOAD), anchor="center")
            note(d, (x, Y_LOAD - 0.62), duty, ha="center")

    motors(X_MCC1, [("DOL", "pump"), ("VFD", "process"), ("S/S", "conveyor")])
    motors(X_MCC2, [("VFD", "pump"), ("DOL", "fan"), ("S/S", "mixer")])

    # UPS -> DCS/PLC
    s.wire(d, (X_UPS, Y_EQUIP - 0.55), (X_UPS, Y_LOAD + 0.55))
    s.place(d, s.Block(w=1.9, h=0.8, name="DCS / PLC", sub="SCADA + I/C",
                       fill="#fff7e6"), (X_UPS, Y_LOAD + 0.05), anchor="center")

    # ---------------- standby: DG -> ATS -> EDB ----------------
    X_DG, X_ATS = 1.2, 2.6
    s.place(d, s.Generator(r=0.42), (X_DG, Y_LOAD + 0.15), anchor="center")
    tag(d, (X_DG - 0.62, Y_LOAD + 0.30), "DG", ha="right", size=FS - 1)
    note(d, (X_DG - 0.62, Y_LOAD + 0.02), "1000 kVA", ha="right")
    s.place(d, s.Block(w=1.2, h=0.7, name="ATS", fill="#eef7ee"),
            (X_ATS, Y_LOAD + 0.4), anchor="center")
    note(d, (X_ATS + 0.78, Y_LOAD + 0.55), "Util / DG", ha="left")
    s.wire(d, (X_DG + 0.42, Y_LOAD + 0.15), (X_ATS - 0.6, Y_LOAD + 0.15))
    s.wire(d, (X_ATS - 0.6, Y_LOAD + 0.15), (X_ATS - 0.6, Y_LOAD + 0.4))
    s.wire(d, (X_ATS, Y_LOAD + 0.75), (X_ATS, Y_EQUIP - 0.55))   # ATS up to EDB drop

    # ---------------- DC control supply (off to the right) ----------------
    s.place(d, s.Block(w=1.7, h=0.8, name="DCDB", sub="110 V DC",
                       fill="#f3f3f3"), (7.4, Y_TXFDR + 0.1), anchor="center")
    note(d, (7.4, Y_TXFDR + 0.85), "MV trip / close + protection", ha="center")

    # ---------------- title block ----------------
    s.title_block(
        d, LVA_L, LVB_R, Y_LOAD - 1.9,
        "MASTER SINGLE-LINE DIAGRAM  -  ~2 MW MV/LV PROCESS PLANT",
        "DWG SLD-2MW-00",
        subtitle="2 x 1600 kVA (Dyn11, Z~6%)  -  split LV bus, N.O. tie  -  "
                 "Saudi / SEC edition")

    # margin spacers so nothing is clipped at the canvas edge
    note(d, (LVA_L - 0.7, Y_UTIL + 0.6), " ")
    note(d, (LVB_R + 0.7, Y_LOAD - 3.2), " ")


d = schemdraw.Drawing()
build(d)
d.save(os.path.join(OUT, "sld-master-2MW.svg"))
d.save(os.path.join(OUT, "sld-master-2MW.png"), dpi=200)
print("master SLD rendered")
