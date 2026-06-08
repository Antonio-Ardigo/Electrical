# Module 1 — Equipment Identification

*Part of the [MV/LV ~2 MW Process Plant training course](../README.md). Diagram:
[master single-line diagram](../diagrams/sld-master-2MW.md). Basis of design:
[reference design document](../docs/main-electrical-equipment-2MW-process-plant.md).*

> All ratings and figures in this module are **indicative and tentative** — they
> illustrate method and typical practice, not a substitute for project-specific
> studies and specifications.

---

## Introduction

This module teaches you to **read the master single-line diagram (SLD)** of the
~2 MW process plant and to **identify every principal piece of equipment by its
tag**, stating clearly what each item *does* and *why it is there*. The core
deliverable is the **Equipment Function Table** in §3, where each row deep-links
to the corresponding tag anchor on the
[master SLD](../diagrams/sld-master-2MW.md) so you can move between text and
drawing in one click.

Keep the [master SLD](../diagrams/sld-master-2MW.md) open alongside this module.
Every tag in the table below maps directly onto the drawing.

### Learning outcomes

On completion you will be able to:

- Navigate a complete MV/LV single-line diagram and trace power flow from the
  utility 11 kV incomer down to process motors and to the essential / clean-power
  loads.
- Locate and name each principal item by its **tag** (`MV-MET`, `MV-SWGR`,
  `MV-PROT`, `MV-NER`, `TX-1`/`TX-2`, `LV-MSB`, `BT`, `MCC-1`/`MCC-2`, `VFD`,
  `PFC`, `DB`, `EDB`, `DG`, `ATS`, `UPS`, `DCDB`).
- State the **function** of each item in one or two sentences and explain how it
  relates to its neighbours.
- Distinguish a **PCC** (Power Control Centre / main LV switchboard, here
  `LV-MSB`) from an **MCC** (Motor Control Centre).
- Recognise the standard one-line symbols for breakers, busbars, transformers,
  CTs/VTs and earthing as drawn on the master SLD.

---

## 1. How to read the SLD

Open the [master SLD](../diagrams/sld-master-2MW.md) and read it **top to
bottom** — energy flows from the utility at the top to the loads at the bottom.

**Voltage levels.** The drawing has two power levels. The **MV (medium-voltage)
level is 11 kV**, 3-phase, 50 Hz: the utility feed, metering, MV switchgear and
the transformer primaries. The **LV (low-voltage) level is 400 V**: everything
below the transformers — the main switchboard, MCCs, VFDs, distribution and
essential boards. The two transformers ([TX-1](../diagrams/sld-master-2MW.md#tx-1),
[TX-2](../diagrams/sld-master-2MW.md#tx-2)) are the boundary between them.

**Breakers.** `[52-x]` marks an **MV circuit breaker** (ANSI device number 52) —
the incomer `[52-I]`, the bus-section `[52-BS]`, and the two transformer feeders
`[52-T1]`/`[52-T2]`. On the LV side, `[ACB]` is an **Air Circuit Breaker** (the
large switchboard incomers and the bus-tie) and `[MCCB]` is a **Moulded-Case
Circuit Breaker** (outgoing feeders). A breaker is the device that makes, carries
and **automatically interrupts** fault current.

**Busbars.** The heavy `═══` lines are **busbars** — the common copper to which
feeders connect. The LV main switchboard
([LV-MSB](../diagrams/sld-master-2MW.md#lv-msb)) is drawn as a **split bus**:
**Bus A** (fed by TX-1) and **Bus B** (fed by TX-2), joined by the
**normally-open bus-tie** ([BT](../diagrams/sld-master-2MW.md#bt)). Splitting the
bus limits the zone affected by a fault and is the foundation of the plant's N-1
resilience.

**The standby path.** Follow the lower band of the drawing: the diesel generator
([DG](../diagrams/sld-master-2MW.md#dg)) feeds an automatic transfer switch
([ATS](../diagrams/sld-master-2MW.md#ats)), which feeds the essential
distribution board ([EDB](../diagrams/sld-master-2MW.md#edb)). On loss of the
utility supply, the ATS transfers the essential bus from utility to generator.

**The DC / control path.** The uninterruptible supply
([UPS](../diagrams/sld-master-2MW.md#ups)) gives clean, no-break power to the
DCS/PLC/SCADA and instrumentation; the DC battery & charger
([DCDB](../diagrams/sld-master-2MW.md#dcdb)) provides the 110 V DC that trips and
closes the MV switchgear and powers its protection — these must stay alive even
when the AC system is dead, which is the whole point of having them.

**Earthing.** `[N]` at the neutral-earthing resistor
([MV-NER](../diagrams/sld-master-2MW.md#mv-ner)) shows the 11 kV neutral earthed
through a resistor that limits earth-fault current; the LV system is solidly
earthed (TN-S).

---

## 2. The two big ideas: PCC vs MCC

A common point of confusion. Both are LV assemblies built to IEC 61439, but they
do different jobs:

- **PCC — Power Control Centre** = the **main LV switchboard**, here
  [LV-MSB](../diagrams/sld-master-2MW.md#lv-msb). It receives the transformer
  outputs and **distributes bulk power** to MCCs, distribution boards and large
  feeders. Think "the LV power hub."
- **MCC — Motor Control Centre**, here
  [MCC-1](../diagrams/sld-master-2MW.md#mcc-1) /
  [MCC-2](../diagrams/sld-master-2MW.md#mcc-2). It is an assembly of **motor
  starters** (DOL, star-delta, soft-starter, VFD) that **controls and protects
  individual motors**. Think "where the motors are started."

In short: the PCC feeds the MCCs; the MCCs feed the motors.

---

## 3. Equipment Function Table — THE CORE DELIVERABLE

One row per tag for **all 18 tags** in the master legend. The **Tag** column
deep-links to the corresponding anchor on the
[master SLD](../diagrams/sld-master-2MW.md); the **Where in the SLD** column is a
quick locator so you can find it on the drawing.

| Tag | Equipment | Function / purpose | Where in the SLD |
|-----|-----------|--------------------|------------------|
| [MV-MET](../diagrams/sld-master-2MW.md#mv-met) | Utility revenue metering cubicle | Measures energy/demand at the 11 kV intake via utility CTs/VTs for tariff billing; it is the commercial boundary between utility and plant. | MV section, at the utility incomer (top of drawing). |
| [MV-SWGR](../diagrams/sld-master-2MW.md#mv-swgr) | 11 kV metal-clad switchgear | Receives and distributes the 11 kV supply; houses the incomer, bus-section and two transformer-feeder breakers so MV circuits can be switched and faults cleared. | MV section, the main 11 kV board below metering. |
| [MV-PROT](../diagrams/sld-master-2MW.md#mv-prot) | MV protection & control IEDs | Detects MV faults (overcurrent 50/51, earth-fault 50N/51N, transformer differential 87T, under/over-voltage 27/59) and trips the right breaker to isolate them quickly. | MV section, relays associated with the MV-SWGR breakers. |
| [MV-NER](../diagrams/sld-master-2MW.md#mv-ner) | Neutral Earthing Resistor | Earths the 11 kV neutral through a resistor to limit earth-fault current (~300–400 A), protecting equipment and people while letting earth-fault relays operate. | MV section, at the `[N]` neutral point of the 11 kV bus. |
| [TX-1](../diagrams/sld-master-2MW.md#tx-1) | MV/LV power transformer No.1 (1600 kVA, Dyn11) | Steps 11 kV down to 400 V to supply Bus A; one of the two parallel sources giving N-1 capability. | Between MV feeder `[52-T1]` and LV incomer `[ACB-A]`. |
| [TX-2](../diagrams/sld-master-2MW.md#tx-2) | MV/LV power transformer No.2 (1600 kVA, Dyn11) | Steps 11 kV down to 400 V to supply Bus B; the second of the two parallel sources giving N-1 capability. | Between MV feeder `[52-T2]` and LV incomer `[ACB-B]`. |
| [LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) | Main LV switchboard / PCC | The 400 V power hub: takes the two transformer outputs onto a split bus (A/B) and distributes bulk LV power to MCCs, boards and large feeders. | LV section, the main switchboard spanning Bus A and Bus B. |
| [BT](../diagrams/sld-master-2MW.md#bt) | LV bus-tie circuit breaker (N.O.) | Normally open; auto-closes on loss of either incomer so the surviving transformer can feed both buses — the key to the plant's N-1 resilience. | LV-MSB, the link between Bus A and Bus B. |
| [MCC-1](../diagrams/sld-master-2MW.md#mcc-1) | Motor Control Centre No.1 | Houses the starters (DOL / star-delta / soft-starter / VFD) that control and protect the Bus-A process motors. | LV-MSB Bus A, on an outgoing `[MCCB]` feeder. |
| [MCC-2](../diagrams/sld-master-2MW.md#mcc-2) | Motor Control Centre No.2 | Houses the starters that control and protect the Bus-B process motors; pairs with MCC-1 to split motor load across the two buses. | LV-MSB Bus B, on an outgoing `[MCCB]` feeder. |
| [VFD](../diagrams/sld-master-2MW.md#vfd) | Variable Frequency Drive(s) | Provides variable-speed control of pumps/fans/mixers and soft starting, cutting energy use and starting stress; sits in an MCC bucket or standalone. | Within MCC-1 / MCC-2, feeding speed-controlled motors. |
| [PFC](../diagrams/sld-master-2MW.md#pfc) | Power factor correction (detuned capacitor bank) | Supplies reactive power locally to raise power factor (~0.85 → 0.95+), reducing demand charges and freeing transformer/cable capacity; detuned (7%) to avoid VFD-harmonic resonance. | LV-MSB Bus A, on a dedicated `[MCCB]` feeder. |
| [DB](../diagrams/sld-master-2MW.md#db) | Distribution board | Distributes LV to general (non-essential) loads — lighting, small power, HVAC, sockets — via MCBs/RCBOs. | LV-MSB Bus A, on an outgoing `[MCCB]` feeder (DB-A). |
| [EDB](../diagrams/sld-master-2MW.md#edb) | Essential / emergency distribution board | Feeds loads that must stay energised (escape lighting, critical auxiliaries); supplied via the ATS so it rides through utility loss on the generator. | LV section, fed from Bus B and backed via the ATS. |
| [DG](../diagrams/sld-master-2MW.md#dg) | Diesel generator set (~1000 kVA) | Standby generation sized for the essential load; starts and takes over on utility failure so critical processes keep running. | Standby power path (lower band of drawing). |
| [ATS](../diagrams/sld-master-2MW.md#ats) | Automatic Transfer Switch | Automatically transfers the essential bus between utility and generator, ensuring only one source feeds the EDB at a time. | Standby path, between DG and EDB. |
| [UPS](../diagrams/sld-master-2MW.md#ups) | Uninterruptible Power Supply | Gives clean, no-break power to DCS/PLC/SCADA and instrumentation, bridging supply interruptions on battery until the generator picks up or power returns. | LV-MSB Bus B feeder, feeding the control system. |
| [DCDB](../diagrams/sld-master-2MW.md#dcdb) | DC battery & charger system (110 V DC) | Provides secure 110 V DC to trip/close the MV switchgear and power its protection relays — available even with the AC system dead. | DC control / protection supply band (lower drawing). |

> Note: the master legend also tabulates `DB / DB-A` as one entry, giving the
> 18 tags listed here (`mv-met` … `dcdb`).

---

## 4. Power-flow walk-through

Trace the energy on the [master SLD](../diagrams/sld-master-2MW.md) as you read.

**Main (normal) path — utility to motor:**

1. The **utility 11 kV feed** arrives and passes through revenue metering
   ([MV-MET](../diagrams/sld-master-2MW.md#mv-met)).
2. It enters the **MV switchgear** ([MV-SWGR](../diagrams/sld-master-2MW.md#mv-swgr))
   via the incomer breaker `[52-I]`, watched by the protection relays
   ([MV-PROT](../diagrams/sld-master-2MW.md#mv-prot)); the 11 kV neutral is
   earthed through the resistor ([MV-NER](../diagrams/sld-master-2MW.md#mv-ner)).
3. From the 11 kV bus, two feeder breakers `[52-T1]`/`[52-T2]` supply the two
   transformers ([TX-1](../diagrams/sld-master-2MW.md#tx-1),
   [TX-2](../diagrams/sld-master-2MW.md#tx-2)), which step 11 kV down to 400 V.
4. Each transformer feeds its LV incomer ACB onto the **main switchboard**
   ([LV-MSB](../diagrams/sld-master-2MW.md#lv-msb)): TX-1 → Bus A, TX-2 → Bus B,
   with the bus-tie ([BT](../diagrams/sld-master-2MW.md#bt)) normally open
   between them.
5. Outgoing `[MCCB]` feeders supply the **MCCs**
   ([MCC-1](../diagrams/sld-master-2MW.md#mcc-1),
   [MCC-2](../diagrams/sld-master-2MW.md#mcc-2)), the
   [PFC](../diagrams/sld-master-2MW.md#pfc) bank and the distribution board
   ([DB](../diagrams/sld-master-2MW.md#db)).
6. Inside an MCC, a starter (DOL, soft-starter or a
   [VFD](../diagrams/sld-master-2MW.md#vfd)) energises the final **process
   motor** — pump, fan, conveyor or mixer.

**Standby path — on utility loss:** the diesel generator
([DG](../diagrams/sld-master-2MW.md#dg)) starts; the
[ATS](../diagrams/sld-master-2MW.md#ats) transfers the essential bus from utility
to generator and feeds the essential distribution board
([EDB](../diagrams/sld-master-2MW.md#edb)). Within the LV switchboard, the
bus-tie ([BT](../diagrams/sld-master-2MW.md#bt)) also auto-closes on loss of
either incomer so the surviving transformer can carry both buses.

**Control / DC path — always alive:** the [UPS](../diagrams/sld-master-2MW.md#ups)
holds up the DCS/PLC/SCADA and instrumentation with no break, while the
[DCDB](../diagrams/sld-master-2MW.md#dcdb) supplies 110 V DC to operate and
protect the MV switchgear regardless of AC availability.

---

## 5. Self-check questions

Attempt these from the master SLD before reading the answers.

1. Which two tags form the boundary between the 11 kV and the 400 V parts of the
   plant, and what do they do?
2. What is the difference between `LV-MSB` and `MCC-1`? Which feeds which?
3. The bus-tie `BT` is normally **open**. What event causes it to close, and why
   is that desirable?
4. Name the three items on the standby/essential path and state the order in
   which energy flows through them on a utility outage.
5. Why does the plant need a separate `DCDB` when it already has a `UPS`?
6. What is the purpose of `MV-NER`, and what would change if it were removed?

<details>
<summary><strong>Answers</strong></summary>

1. [TX-1](../diagrams/sld-master-2MW.md#tx-1) and
   [TX-2](../diagrams/sld-master-2MW.md#tx-2) — the MV/LV power transformers.
   They step 11 kV down to 400 V, separating the MV and LV sides.
2. [LV-MSB](../diagrams/sld-master-2MW.md#lv-msb) is the **PCC / main LV
   switchboard** that distributes bulk 400 V power;
   [MCC-1](../diagrams/sld-master-2MW.md#mcc-1) is a **Motor Control Centre** of
   starters that control individual motors. The LV-MSB feeds the MCC.
3. It auto-closes on **loss of either LV incomer** (i.e. loss of one transformer
   or its feeder). Closing it lets the surviving transformer feed both buses,
   so half the plant is not lost — this is the plant's N-1 resilience.
4. [DG](../diagrams/sld-master-2MW.md#dg) →
   [ATS](../diagrams/sld-master-2MW.md#ats) →
   [EDB](../diagrams/sld-master-2MW.md#edb). On a utility outage the DG starts,
   the ATS transfers the essential bus to the generator, and the EDB stays
   energised.
5. The [UPS](../diagrams/sld-master-2MW.md#ups) supplies AC to the control system
   (DCS/PLC/SCADA), while the [DCDB](../diagrams/sld-master-2MW.md#dcdb) supplies
   **110 V DC** to trip/close the MV switchgear and power its protection relays.
   DC must be available to operate the breakers even when the AC system is dead,
   so the two serve different, both-essential supplies.
6. [MV-NER](../diagrams/sld-master-2MW.md#mv-ner) earths the 11 kV neutral
   through a resistor to **limit earth-fault current** (~300–400 A). Remove it
   and an earth fault could draw very high current (damage, hazard) — or, if the
   neutral were left isolated, earth-fault relaying would lose its reliable
   operating current.

</details>

---

*Next: [Module 2 — Electrical Calculations](module-02-calculations.md). Keep the
[master SLD](../diagrams/sld-master-2MW.md) open — Module 2 sizes the very
equipment you have just identified.*
