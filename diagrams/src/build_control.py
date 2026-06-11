"""Generate the control-system / power-management architecture block diagram
for the ~2 MW MV/LV process plant (Module 4 - Control Philosophy).

This is a layered network / block diagram (not a power SLD): it reuses the
slddraw Block / busbar / wire / dot / place helpers and the standard colours.

Layers (top -> bottom):
  1. Supervisory   : DCS/SCADA  +  Power Management System (PMS), linked by gateway
  2. Station bus   : IEC 61850 MMS Ethernet/fibre, redundant
  3. Bay/protection: row of IEDs (numerical relays) with GOOSE peer-to-peer link
  4. Field/process : breakers (52), DG/AVR/governor+sync, ATS, UPS/DC, meters, VFDs

Outputs diagrams/svg/control-architecture.svg (+ .png for review).
Run:  python3 build_control.py
"""
import os
import schemdraw
from schemdraw import elements as elm
import slddraw as s

OUT = os.path.join(os.path.dirname(__file__), "..", "svg")
FS = s.FS

MV = s.MV_COLOR
LV = s.LV_COLOR
GREY = "#666666"
NETCOL = "#11457e"     # navy for the communication network
HWCOL = "#b22222"      # firebrick for hardwired safety trips


def tag(d, p, t, ha="center", size=FS, color=s.COLOR, va="center"):
    d += elm.Label().at(p).label(t, halign=ha, valign=va,
                                 fontsize=size, color=color)


def note(d, p, t, ha="center", size=FS - 3, color=GREY, va="center"):
    d += elm.Label().at(p).label(t, halign=ha, valign=va,
                                 fontsize=size, color=color)


def net(d, p0, p1, color=NETCOL, lw=s.LW):
    """A networked (communication) link - solid navy line."""
    d += elm.Line().at(p0).to(p1).linewidth(lw).color(color)


def hardwire(d, p0, p1, color=HWCOL, lw=s.LW):
    """A hardwired link - dashed firebrick line."""
    d += elm.Line().at(p0).to(p1).linewidth(lw).color(color).linestyle("--")


def build(d):
    d.config(unit=1, fontsize=FS)

    # ---------------- layer geometry (y) ----------------
    Y_SUP = 13.2        # supervisory blocks centre
    Y_STN = 9.6         # station bus
    Y_IED = 7.4         # IED row centre
    Y_GOOSE = 5.6       # GOOSE peer-to-peer link
    Y_FLD = 3.4         # field / process blocks centre

    X_L = -11.0         # left extent of buses / banners
    X_R = 11.0          # right extent

    # ============================================================
    # Layer banners (light dashed band labels on the left)
    # ============================================================
    def banner(y, text, sub):
        d.add(elm.Line().at((X_L - 0.6, y)).to((X_R + 0.6, y))
              .color("#cccccc").linewidth(0.8).linestyle(":"))
        tag(d, (X_L - 0.6, y + 0.30), text, ha="left", size=FS - 1, color="#333333")
        note(d, (X_L - 0.6, y + 0.04), sub, ha="left", size=FS - 3)

    banner(Y_SUP + 1.55, "1  SUPERVISORY LEVEL", "plant control / operator HMI / electrical SCADA")
    banner(Y_STN + 0.95, "2  STATION BUS", "IEC 61850 station network")
    banner(Y_IED + 1.35, "3  BAY / PROTECTION LEVEL", "numerical protection relays (IEDs)")
    banner(Y_FLD + 1.45, "4  FIELD / PROCESS LEVEL", "primary plant: breakers, machines, meters, drives")

    # ============================================================
    # 1) Supervisory level: DCS/SCADA  +  PMS, linked by gateway
    # ============================================================
    X_DCS = -4.0
    X_PMS = 4.0
    s.place(d, s.Block(w=4.6, h=1.5, name="DCS / SCADA",
                       sub="process control + HMI", fill="#fff7e6"),
            (X_DCS, Y_SUP), anchor="center")
    note(d, (X_DCS + 0.2, Y_SUP - 0.95), "monitoring / alarms / trends",
         size=FS - 3, color="#8a6d1a")

    s.place(d, s.Block(w=4.6, h=1.5, name="Power Mgmt System",
                       sub="PMS - electrical control", fill="#eef2f7"),
            (X_PMS, Y_SUP), anchor="center")
    note(d, (X_PMS - 0.2, Y_SUP - 0.95), "load shedding / bus transfer / genset ctrl",
         size=FS - 3, color=LV)

    # gateway link between DCS and PMS
    gx0 = X_DCS + 2.3
    gx1 = X_PMS - 2.3
    net(d, (gx0, Y_SUP), (gx1, Y_SUP), color="#7a7a7a")
    s.place(d, s.Block(w=2.0, h=0.62, name="gateway", fill="#f3f3f3"),
            (0, Y_SUP), anchor="center")
    note(d, (0, Y_SUP - 0.62), "OPC-UA / Modbus TCP", size=FS - 3)

    # ============================================================
    # 2) Station bus (redundant communication backbone)
    # ============================================================
    s.busbar(d, X_L, X_R, Y_STN, color=NETCOL, lw=4)
    s.busbar(d, X_L, X_R, Y_STN - 0.22, color="#7f9fc8", lw=2)   # redundant 2nd path
    tag(d, (0, Y_STN + 0.42),
        "Station bus  -  IEC 61850 MMS  (Ethernet / fibre, redundant)",
        ha="center", size=FS - 1, color=NETCOL)
    note(d, (X_R, Y_STN - 0.55), "ring / dual-star", ha="right", size=FS - 3)

    # supervisory down-links to the station bus (offset from the captions)
    X_DCSd = X_DCS - 1.9
    X_PMSd = X_PMS + 1.9
    net(d, (X_DCSd, Y_SUP - 0.75), (X_DCSd, Y_STN))
    s.dot(d, (X_DCSd, Y_STN), color=NETCOL)
    net(d, (X_PMSd, Y_SUP - 0.75), (X_PMSd, Y_STN))
    s.dot(d, (X_PMSd, Y_STN), color=NETCOL)

    # ============================================================
    # 3) Bay / protection level: row of IEDs
    # ============================================================
    ieds = [
        (-9.0, "IED", "MV incomer\n50/51, 27/59"),
        (-5.4, "IED", "MV bus-section\n50/51"),
        (-1.8, "IED", "Transformer\n87T, 49, 51"),
        ( 1.8, "IED", "LV incomer\nACB-A / ACB-B"),
        ( 5.4, "IED", "Bus-tie\n25, 27, ABT"),
        ( 9.0, "IED", "MCC feeders\n50/51, 46, 49"),
    ]
    ied_x = [x for (x, _, _) in ieds]
    for (x, nm, sub) in ieds:
        # drop from station bus to IED
        s.dot(d, (x, Y_STN - 0.22), color=NETCOL)
        net(d, (x, Y_STN - 0.22), (x, Y_IED + 0.62))
        s.place(d, s.Block(w=2.7, h=1.24, name=nm, sub=sub, fill="#e9eef4"),
                (x, Y_IED), anchor="center")

    # ----- GOOSE peer-to-peer link across the IED row -----
    gl, gr = ied_x[0], ied_x[-1]
    for x in ied_x:
        net(d, (x, Y_IED - 0.62), (x, Y_GOOSE), color=GREY)
        s.dot(d, (x, Y_GOOSE), color=GREY)
    d += (elm.Line().at((gl, Y_GOOSE)).to((gr, Y_GOOSE))
          .linewidth(2.2).color(MV))
    tag(d, (0, Y_GOOSE + 0.30),
        "GOOSE peer-to-peer  -  fast load shedding + automatic bus transfer",
        ha="center", size=FS - 1, color=MV)

    # ============================================================
    # 4) Field / process level: primary plant per IED
    # ============================================================
    # Each column's primary plant aligns with the IED above it. The transformer
    # column carries the breakers the 87T differential trips (hardwired).
    field = [
        (-9.0, "52  MV CB",    "MV incomer\nbreaker",        "#eef2f7"),
        (-5.4, "52  MV CB",    "MV bus-section\nbreaker",    "#eef2f7"),
        (-1.8, "52-T / ACB",   "TX breakers\n+ power meter", "#eef2f7"),
        ( 1.8, "Genset / ATS", "DG  AVR / gov\n+ sync, ATS", "#eef7ee"),
        ( 5.4, "UPS / DC",     "UPS + DCDB\n110 V DC",       "#f3f3f3"),
        ( 9.0, "VFDs / Meter", "MCC drives\nmotor feeders",  "#eef2f7"),
    ]
    for (x, nm, sub, fill) in field:
        s.place(d, s.Block(w=2.7, h=1.3, name=nm, sub=sub, fill=fill),
                (x, Y_FLD), anchor="center")

    # IED -> field links. Most are networked (process bus / hardwired I/O);
    # the transformer 87T differential trip is a dedicated hardwired safety trip.
    for (x, nm, sub, fill) in field:
        if x == -1.8:
            hardwire(d, (x, Y_GOOSE), (x, Y_FLD + 0.65))   # 87T -> 52-T (hardwired)
        else:
            net(d, (x, Y_GOOSE), (x, Y_FLD + 0.65), color=GREY)

    # ---- legend for link types (bottom-right) ----
    lx = 3.2
    ly = Y_FLD - 1.5
    net(d, (lx, ly), (lx + 1.0, ly), color=GREY)
    note(d, (lx + 1.2, ly), "networked link  (IEC 61850 / process bus)",
         ha="left", size=FS - 3)
    hardwire(d, (lx, ly - 0.42), (lx + 1.0, ly - 0.42))
    note(d, (lx + 1.2, ly - 0.42), "hardwired trip  (safety-critical, e.g. 87T to 52)",
         ha="left", size=FS - 3, color=HWCOL)

    # ---- key-functions annotation block (bottom-left) ----
    fx = X_L - 0.6
    fy = Y_FLD - 1.2
    tag(d, (fx, fy + 0.30), "KEY PMS FUNCTIONS", ha="left", size=FS - 2, color=LV)
    for i, txt in enumerate([
        "-  monitoring / alarms / trends",
        "-  energy metering",
        "-  generator control + synchronisation",
        "-  intelligent (fast) load shedding",
        "-  automatic bus transfer",
    ]):
        note(d, (fx, fy - i * 0.34), txt, ha="left", size=FS - 3, color="#333333")

    # ============================================================
    # title block (standard, consistent with the SLDs)
    # ============================================================
    note(d, (0, Y_FLD - 3.35),
         "IEC 61850 station + process bus  -  GOOSE for fast schemes  -  "
         "hardwired trips for safety  -  indicative",
         ha="center", size=FS - 2, color="#333333")
    s.title_block(
        d, X_L - 0.6, X_R + 0.6, Y_FLD - 3.7,
        "CONTROL-SYSTEM / POWER-MANAGEMENT ARCHITECTURE  -  ~2 MW MV/LV PLANT",
        "DWG SLD-2MW-CTL")


d = schemdraw.Drawing()
build(d)
d.save(os.path.join(OUT, "control-architecture.svg"))
d.save(os.path.join(OUT, "control-architecture.png"), dpi=200)
print("control architecture diagram rendered")
