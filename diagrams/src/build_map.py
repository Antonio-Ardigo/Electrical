"""Regenerate the SWA logistics map (one figure: national + Riyadh-province zoom).

Corrected scope (per submitted booklet): 21 groundwater plants — 19 in Riyadh
Province + 2 in the Eastern Province, 16 sites, ~1.66 M m3/day. No Madinah / Qassim.
City-level indicative positions (geocodes from the tender logistics pack).
"""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "svg")
RIY = "#11457e"   # Riyadh Province
EAST = "#cc7a00"  # Eastern Province

# Simplified Saudi Arabia outline (lon, lat) — schematic
KSA = [(34.6,28.0),(36.6,29.4),(38.8,30.1),(42.0,31.1),(44.7,29.6),(46.5,29.1),
       (47.7,28.5),(49.0,28.6),(50.8,27.0),(50.2,24.6),(51.6,24.3),(55.2,22.6),
       (55.7,20.0),(52.0,19.0),(47.0,17.0),(43.0,16.6),(42.6,16.4),(41.0,19.0),
       (39.0,21.5),(37.5,24.5),(35.5,26.5),(34.6,28.0)]

# site: lon, lat, name, units, capacity(k m3/d), province  (multi-train share a site)
SITES = [
    (46.717,22.293,"Al-Aflaj",1,25,"R"),
    (47.165,23.997,"Al-Dilam",1,10,"R"),
    (46.879,23.488,"Hawtat Bani Tamim",1,20,"R"),
    (46.021,23.405,"Al-Hariq",1,10,"R"),
    (47.684,23.830,"Al-Kharj",1,80,"R"),
    (46.251,24.100,"Dhurma–Muzahimiyah",1,22,"R"),
    (45.354,26.506,"Al-Artawiyah",1,5,"R"),
    (46.616,24.606,"Al-Dawadmi",1,50,"R"),
    (46.716,24.639,"Riyadh city (Malaz, Manfuhah, Shumaisi)",3,144,"R"),
    (46.345,25.079,"Salbukh 1–3",3,450,"R"),
    (46.795,25.227,"Al-Buwayb 1–3",3,450,"R"),
    (47.569,25.101,"Saad 1–2",2,1140,"R"),
    (49.60,25.40,"Al-Hani [verify]",1,360,"E"),
    (45.963,28.433,"Hafar Al-Batin",1,67,"E"),
]  # 12 Riyadh-province sites (19 units) + 2 Eastern sites (2 units) = 14 markers, 21 units

def msize(cap):           # marker area ~ sqrt(capacity)
    return 24 + 7*math.sqrt(cap)

def draw_base(ax):
    ax.add_patch(Polygon(KSA, closed=True, facecolor="#eef1ea",
                         edgecolor="#9aa39a", lw=1.3, zorder=1))
    ax.set_aspect(1.0); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def plot_sites(ax, label=False, zoom=False):
    for lon,lat,name,n,cap,prov in SITES:
        c = RIY if prov=="R" else EAST
        ax.scatter([lon],[lat],s=msize(cap),c=c,zorder=5,edgecolor="white",lw=0.8,alpha=0.9)
        if label:
            short = name.split(" (")[0]
            ax.annotate(f"{short}"+(f" ×{n}" if n>1 else ""),(lon,lat),
                        xytext=(5,3),textcoords="offset points",fontsize=7.5,color="#222")

fig=plt.figure(figsize=(13.5,6.6))
gs=fig.add_gridspec(1,2,width_ratios=[1.1,1.0],wspace=0.05)
axN=fig.add_subplot(gs[0,0]); axR=fig.add_subplot(gs[0,1])

# national
draw_base(axN); plot_sites(axN)
axN.set_xlim(33.5,56.5); axN.set_ylim(15.5,32.5)
ZB=(43.6,48.4,21.6,27.2)
axN.add_patch(Rectangle((ZB[0],ZB[2]),ZB[1]-ZB[0],ZB[3]-ZB[2],fill=False,
              edgecolor=RIY,lw=1.6,ls="--",zorder=6))
axN.annotate("Riyadh Province\n(see zoom →)",(45.0,27.9),color=RIY,fontsize=9,
             ha="center",fontweight="bold")
axN.annotate("Eastern Province",(50.2,27.3),color=EAST,fontsize=9,ha="center",fontweight="bold")
axN.set_title("Kingdom of Saudi Arabia — 21 plants",fontsize=11,color="#333")

# Riyadh-province zoom
draw_base(axR); plot_sites(axR,label=True,zoom=True)
axR.set_xlim(ZB[0],ZB[1]); axR.set_ylim(ZB[2],ZB[3])
for s in axR.spines.values(): s.set_visible(True); s.set_edgecolor(RIY); s.set_lw(1.4); s.set_ls("--")
axR.set_title("Riyadh Province — 19 plants (12 sites)",fontsize=11,color="#333")
axR.scatter([],[],s=70,c=RIY,edgecolor="white",label="Riyadh Province plant")
axR.scatter([],[],s=70,c=EAST,edgecolor="white",label="Eastern Province plant")
axR.legend(loc="lower right",fontsize=8,frameon=True,facecolor="white",edgecolor="#ccc")

fig.suptitle("SWA Electrical SPOF / RAM — Site Logistics Map",fontsize=15,fontweight="bold",y=0.99)
fig.text(0.5,0.93,"21 groundwater plants · 19 Riyadh Province + 2 Eastern Province · 16 sites · "
         "~1.66 M m³/day",ha="center",fontsize=10,color="#555")
fig.text(0.5,0.025,"Schematic / indicative, city-level positions (marker size ~ capacity). "
         "No plants in Madinah or Qassim. #Al-Hani (Eastern) location to verify.",
         ha="center",fontsize=8,color="#777")
fig.subplots_adjust(top=0.88,bottom=0.08)
fig.savefig(os.path.join(OUT,"wsm-site-logistics-map.svg"))
fig.savefig(os.path.join(OUT,"wsm-site-logistics-map.png"),dpi=150)
print("regenerated logistics map (19 Riyadh + 2 Eastern, no Madinah/Qassim)")
