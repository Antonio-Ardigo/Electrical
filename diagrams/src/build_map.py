"""Generate the WSM site-logistics map (one figure = national overview + zoom).

Schematic location map for the WSM Electrical SPOF Assessment — Central & Eastern
sector, 21 assessment units. Vector output (SVG) so the zoom stays crisp.

Outputs diagrams/svg/wsm-site-logistics-map.svg (+ .png for review).
Run:  python3 build_map.py
NOTE: schematic, indicative geometry — not survey-grade and not to scale.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "svg")

# ---- palette ----
LAND = "#eef1ea"
LAND_EDGE = "#9aa39a"
SECTOR = "#dCe7f2"
HUB = "#11457e"      # navy
UNIT = "#cc7a00"     # amber for individual units
ACCENT = "#b22222"

# ---- simplified Saudi Arabia outline (lon, lat) — schematic ----
KSA = [
    (34.6, 28.0), (36.6, 29.4), (38.8, 30.1), (42.0, 31.1), (44.7, 29.6),
    (46.5, 29.1), (47.7, 28.5), (49.0, 28.6), (50.8, 27.0), (50.2, 24.6),
    (51.6, 24.3), (55.2, 22.6), (55.7, 20.0), (52.0, 19.0), (47.0, 17.0),
    (43.0, 16.6), (42.6, 16.4), (41.0, 19.0), (39.0, 21.5), (37.5, 24.5),
    (35.5, 26.5), (34.6, 28.0),
]

# ---- hub locations (lon, lat, name, region, indicative unit count) ----
HUBS = [
    (46.68, 24.71, "Riyadh", "Central", 7),
    (43.97, 26.33, "Qassim", "Central-N", 4),
    (39.61, 24.47, "Madinah", "West", 4),
    (50.10, 26.43, "Dammam", "Eastern Region", 6),
]  # 7+4+4+6 = 21 (indicative distribution)

ZOOM = (38.3, 51.5, 23.2, 27.4)  # lon0, lon1, lat0, lat1


def draw_base(ax, label_regions=True):
    ax.add_patch(Polygon(KSA, closed=True, facecolor=LAND,
                         edgecolor=LAND_EDGE, lw=1.4, zorder=1))
    ax.set_aspect(1.0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def plot_hubs(ax, big=False, with_units=False):
    import math
    for lon, lat, name, region, n in HUBS:
        ax.scatter([lon], [lat], s=160 if big else 80, c=HUB, zorder=6,
                   edgecolor="white", linewidth=1.2, marker="o")
        if big:
            ax.annotate(f"{name} ({n})", (lon, lat), xytext=(0, 13),
                        textcoords="offset points", ha="center",
                        fontsize=11, fontweight="bold", color=HUB, zorder=7)
        else:
            ax.annotate(name, (lon, lat), xytext=(0, 8),
                        textcoords="offset points", ha="center",
                        fontsize=9, fontweight="bold", color=HUB, zorder=7)
        if with_units:
            for k in range(n):
                ang = 2 * math.pi * k / n - math.pi / 2
                r = 0.33
                ax.scatter([lon + r * math.cos(ang)], [lat + r * math.sin(ang)],
                           s=16, c=UNIT, zorder=4, edgecolor="white", linewidth=0.4)


fig = plt.figure(figsize=(13.5, 6.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.08)
ax_o = fig.add_subplot(gs[0, 0])   # national overview
ax_z = fig.add_subplot(gs[0, 1])   # zoom

# ---------------- overview ----------------
draw_base(ax_o)
plot_hubs(ax_o, big=False)
ax_o.set_xlim(33.5, 56.5); ax_o.set_ylim(15.5, 32.5)
# zoom rectangle on the overview
z = Rectangle((ZOOM[0], ZOOM[2]), ZOOM[1] - ZOOM[0], ZOOM[3] - ZOOM[2],
              fill=False, edgecolor=ACCENT, lw=1.8, ls="--", zorder=6)
ax_o.add_patch(z)
ax_o.annotate("Central & Eastern sector\n(see zoom, right)", (44.6, 28.8),
              color=ACCENT, fontsize=9, ha="center", fontweight="bold")
ax_o.set_title("Kingdom of Saudi Arabia - overview", fontsize=11, color="#333")
ax_o.annotate("KSA", (45.0, 20.0), fontsize=22, color="#c9cfc6",
              ha="center", va="center", zorder=2, fontweight="bold")
# simple north arrow
ax_o.annotate("N", (34.6, 31.4), fontsize=10, ha="center", fontweight="bold")
ax_o.add_patch(FancyArrowPatch((34.6, 30.0), (34.6, 31.1),
               arrowstyle="-|>", mutation_scale=12, color="#333", lw=1.4))

# ---------------- zoom ----------------
draw_base(ax_z)
plot_hubs(ax_z, big=True, with_units=True)
ax_z.set_xlim(ZOOM[0], ZOOM[1]); ax_z.set_ylim(ZOOM[2], ZOOM[3])
for s in ax_z.spines.values():
    s.set_visible(True); s.set_edgecolor(ACCENT); s.set_linewidth(1.6)
    s.set_linestyle("--")
ax_z.set_title("Central & Eastern sector - assessment units (zoom)",
               fontsize=11, color="#333")

# legend (on zoom)
ax_z.scatter([], [], s=120, c=HUB, edgecolor="white", label="Hub location")
ax_z.scatter([], [], s=30, c=UNIT, edgecolor="white", label="Assessment unit (indicative)")
ax_z.legend(loc="lower right", fontsize=8, frameon=True, facecolor="white",
            edgecolor="#ccc")

# ---------------- figure title / footer ----------------
fig.suptitle("WSM Electrical SPOF Assessment  -  Site Logistics Map", fontsize=15,
             fontweight="bold", y=0.99)
fig.text(0.5, 0.93,
         "Central & Eastern sector  -  21 assessment units across Riyadh, Qassim, Madinah and the Eastern Region",
         ha="center", fontsize=10, color="#555")
fig.text(0.5, 0.025,
         "Schematic / indicative only - geometry not to scale, unit distribution indicative (7+4+4+6 = 21). "
         "Ref: WSM-SUBC-SPEC-001 Rev 0.",
         ha="center", fontsize=8, color="#777")

fig.subplots_adjust(top=0.88, bottom=0.08)
fig.savefig(os.path.join(OUT, "wsm-site-logistics-map.svg"))
fig.savefig(os.path.join(OUT, "wsm-site-logistics-map.png"), dpi=150)
print("site logistics map rendered")
