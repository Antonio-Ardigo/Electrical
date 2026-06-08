# Main Electrical Equipment — MV/LV Process Plant (~2 MW)

> Tentative basis of design for identifying the principal electrical equipment of a
> medium-voltage / low-voltage industrial process plant with an installed/demand
> capacity of approximately **2 MW**. Figures are indicative and to be confirmed
> against the final load list, utility connection conditions, and applicable
> local regulations.

---

## 1. Design Basis & Assumptions

| Item | Assumption (to be confirmed) |
|------|------------------------------|
| Total plant maximum demand | ~2.0 MW |
| Assumed overall power factor | 0.85 (before correction) |
| Apparent power (uncorrected) | ~2.35 MVA |
| Design/diversity + future margin | +20–25 % → ~2.8–3.0 MVA installed transformer capacity |
| Utility incoming voltage (MV) | 11 kV (typical; could be 6.6 / 20 / 33 kV per utility) |
| Distribution / utilization voltage (LV) | 400/415 V, 3-phase, 50 Hz (IEC) — or 480 V, 60 Hz (ANSI) |
| MV system earthing | Resistance-earthed (NER) — typical for industrial MV |
| LV system earthing | TN-S (solid) |
| Redundancy philosophy | 2 × transformers + bus-tie (N+1 partial); single DG for essential loads |

**Sizing logic:** 2 MW ÷ 0.85 pf ≈ 2.35 MVA; with diversity/spare margin the
transformer base is ~2.5–3 MVA. This is normally split into **2 × 1600 kVA**
(or 2 × 1250 kVA) units operating on a split LV bus with a normally-open
bus-tie, so that one transformer can carry the essential load if the other is
lost.

---

## 2. Power Architecture (Single-Line Concept)

```
            Utility MV feed (e.g. 11 kV)
                     │
        ┌────────────┴────────────┐
        │   MV SWITCHGEAR (11 kV) │   metering, incomer, bus-section, 2x Tx feeders
        └──────┬───────────┬──────┘
               │           │
          ┌────┴───┐   ┌───┴────┐
          │ TX-1   │   │ TX-2   │   1600 kVA, 11kV/0.4kV, Dyn11
          │1600kVA │   │1600kVA │
          └────┬───┘   └───┬────┘
               │           │
        ┌──────┴──┐ B/T ┌──┴──────┐
        │ LV MSB-A │═══ │ LV MSB-B │  Main LV switchboard (PCC), bus-tie (N.O.)
        └──┬───┬──┘     └──┬───┬──┘
           │   │           │   │
         MCC  PFC        MCC  Dist. boards, VFDs
           │
        Process motors / loads
                     │
   ───────────────────────────────────
   Standby: DG set ──► ATS ──► Essential LV bus
   Clean power: UPS ──► DCS/PLC/Instrumentation
```

---

## 3. Principal Electrical Equipment Schedule

### 3.1 Incoming & Medium-Voltage (MV)

| Tag | Equipment | Indicative Rating / Notes |
|-----|-----------|---------------------------|
| MV-MET | Utility revenue metering cubicle | CTs/VTs, tariff meter per utility |
| MV-SWGR | **MV switchgear** (metal-clad/metal-enclosed) | 11 kV, 630–1250 A bus, 25 kA/1 s; vacuum CBs; incomer + bus-section + 2 × transformer feeders. To IEC 62271-200 |
| MV-RMU | (Alternative) Ring Main Unit | Compact SF6 RMU for small footprint installations |
| MV-NER | Neutral Earthing Resistor | Limits earth-fault current (e.g. to 300–400 A); with neutral CT |
| MV-PROT | Protection & control relays | Numerical IEDs: 50/51, 50N/51N, 87T (transformer diff.), 27/59, etc. |

### 3.2 Transformation

| Tag | Equipment | Indicative Rating / Notes |
|-----|-----------|---------------------------|
| TX-1 / TX-2 | **MV/LV power transformers** | 2 × 1600 kVA (or 2 × 1250 kVA), 11 kV / 0.4 kV, Dyn11, Z ≈ 6 %; cast-resin (dry-type) for indoor, or oil-immersed (ONAN). To IEC 60076. OLTC or off-load taps ±2×2.5 % |
| TX-AUX | Auxiliary/control transformer(s) | Small dry-type for control supplies where needed |

### 3.3 Low-Voltage (LV) Distribution

| Tag | Equipment | Indicative Rating / Notes |
|-----|-----------|---------------------------|
| LV-MSB | **Main LV switchboard / PCC** (Power Control Centre) | 400 V, split bus A/B, ~2500–3200 A bus, 50–65 kA; ACB incomers + motorized bus-tie; MCCB outgoing feeders. Form 4b segregation, to IEC 61439-1/2 |
| MCC-1..n | **Motor Control Centres (MCC)** | Withdrawable/fixed buckets: DOL, star-delta, soft-starter and VFD starters; thermal/electronic overload, contactors, motor-protection relays. To IEC 61439-1/2. *(Primary subject of this request — see §4)* |
| VFD/VSD | Variable Frequency Drives | For pumps, fans, compressors, mixers requiring speed control; with input chokes/EMC filters; may be MCC-integrated or standalone |
| PFC | **Power factor correction** | Automatic capacitor bank, detuned (7 %) reactors to handle VFD harmonics; sized to correct ~0.85 → 0.95+ |
| DB | Distribution boards | Lighting, small power, HVAC, sockets; MCB/RCBO |
| EDB | Essential/emergency distribution board | Fed via ATS from DG |

### 3.4 Standby, Backup & Clean Power

| Tag | Equipment | Indicative Rating / Notes |
|-----|-----------|---------------------------|
| DG | **Diesel generator set** | Sized for essential loads (not full 2 MW unless required) — e.g. 800–1250 kVA; with AVR, fuel day-tank, exhaust, acoustic canopy |
| ATS | Automatic Transfer Switch | Utility ↔ DG changeover for the essential bus |
| UPS | Uninterruptible Power Supply | For DCS/PLC/SCADA, instrumentation, critical comms; battery autonomy 15–30 min (or per spec) |
| DCDB | DC battery & charger system | For MV switchgear trip/close & protection supplies (110 V DC typical) |

### 3.5 Control, Protection & Auxiliary Systems

| Equipment | Notes |
|-----------|-------|
| Protection relays / IEDs | MV & LV feeder, transformer and motor protection; earth-fault, overcurrent, differential |
| DCS / PLC control system | Process control, interface to MCC/VFD via hardwired or fieldbus (PROFIBUS/PROFINET/Modbus) |
| Power monitoring / SCADA | Energy metering, alarms, trends |
| Earthing & bonding system | Main earth grid, equipment bonding, MV NER, LV TN-S earthing |
| Lightning protection (LPS) | Air terminals, down conductors, earth electrodes per IEC 62305 |
| Cabling & cable management | MV (XLPE), LV power & control cables; ladders/trays, glanding; segregation power/control/instrument |
| Lighting & small power | Normal + emergency/escape lighting |
| HVAC for electrical rooms | Cooling for switchrooms/transformer/VFD rooms |

---

## 4. Motor Control Centre (MCC) — Detail

The MCC is the core of the plant's motor distribution. Key characteristics for
this ~2 MW plant:

- **Construction:** Modular, compartmentalized LV assembly to **IEC 61439-1/-2**,
  Form 3b/4b segregation; withdrawable (drawout) or fixed buckets.
- **Bus rating:** Sized to MCC group demand (e.g. 1000–2000 A horizontal bus),
  short-circuit withstand matched to the upstream board (typ. 50 kA).
- **Starter types per motor:**
  | Motor size (LV) | Typical starting method |
  |-----------------|-------------------------|
  | up to ~7.5 kW | Direct-on-line (DOL) |
  | ~7.5–55 kW | DOL / star-delta / soft-starter |
  | ~55–200 kW | Soft-starter or VFD |
  | speed-controlled loads | VFD (any size) |
- **Per-feeder content:** MCCB or fuse-contactor, contactor(s), thermal/electronic
  overload or motor-protection relay, local/remote control, ammeter, run/trip status.
- **Voltage threshold note:** Individual motors larger than **~150–200 kW** are
  often more economically fed at **MV (3.3 / 6.6 kV)** via a dedicated MV motor
  starter rather than the LV MCC. Confirm against the final motor list — for a
  2 MW plant the largest drives may sit near this boundary.

---

## 5. Applicable Standards (Indicative)

| Equipment | Standard |
|-----------|----------|
| MV switchgear | IEC 62271-200 / -100 |
| Power transformers | IEC 60076 series |
| LV switchgear & MCC assemblies | IEC 61439-1 / -2 |
| LV circuit breakers | IEC 60947-2 |
| Motors | IEC 60034 series |
| VFDs / adjustable-speed drives | IEC 61800 series |
| Capacitors / PFC | IEC 60831 |
| Earthing | IEC 60364, IEEE 80 (substation) |
| Lightning protection | IEC 62305 |
| Installation (general) | IEC 60364 / local wiring rules |

---

## 6. Summary — Main Equipment Checklist

- [ ] MV utility metering cubicle
- [ ] **MV switchgear** (11 kV) with protection relays
- [ ] Neutral earthing resistor (NER)
- [ ] **2 × MV/LV power transformers** (~1600 kVA each)
- [ ] **Main LV switchboard / PCC** (split bus + bus-tie)
- [ ] **Motor Control Centre(s) (MCC)** with DOL / soft-start / VFD starters
- [ ] **Variable Frequency Drives (VFD/VSD)**
- [ ] **Power factor correction** (detuned capacitor bank)
- [ ] **Diesel generator set + ATS** (essential loads)
- [ ] **UPS + DC battery/charger** (control & protection)
- [ ] Distribution boards (normal + essential)
- [ ] Earthing, bonding & lightning protection
- [ ] DCS/PLC control & power monitoring (SCADA)
- [ ] Cabling, cable management & switchroom HVAC

---

*This is a tentative, concept-level identification. Final equipment selection,
ratings, redundancy and voltage levels must be confirmed by the detailed load
list, short-circuit/load-flow studies, utility connection agreement, and the
governing project specifications and standards.*
