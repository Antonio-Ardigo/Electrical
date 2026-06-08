# Module 3 — Single Points of Failure (SPOF) Analysis

*Part of the [MV/LV ~2 MW Process Plant training course](../README.md). Diagrams:
[SPOF example SLDs](../diagrams/spof-examples/). Basis of design:
[reference design document](../docs/main-electrical-equipment-2MW-process-plant.md).*

> All ratings and figures in this module are **indicative and tentative** — they
> illustrate method and typical practice, not a substitute for project-specific
> reliability/availability studies and the governing standards.

---

## Introduction

A **single point of failure (SPOF)** is any one component whose failure, on its
own, disables a function or de-energises a load that must stay up. In a process
plant a SPOF matters for three reasons:

- **Availability / production loss** — an unplanned trip of a critical load can
  stop the process, spoil a batch, or force a lengthy restart.
- **Safety** — loss of supply to safety systems, cooling, agitation or
  ventilation can create a hazardous condition.
- **Cost** — downtime, damaged product and emergency repairs are expensive
  relative to the cost of the redundancy that would have prevented them.

### The method — how to hunt for SPOFs

Work the single-line diagram systematically:

1. **Trace each element** from source to load along the power path.
2. At every element ask: *"if this one item fails (or is isolated for
   maintenance), what loses supply?"*
3. Flag any element where the answer is **"a load that must stay up"** and there
   is **no alternative path**.
4. Look especially at **shared / common elements** — a single incomer, a single
   transformer, an un-tied bus, a shared cable or MCC, a single ATS — because
   redundancy downstream is defeated by a common element upstream.
5. Propose a **mitigation** that gives the function an independent alternative
   path (N+1, dual feed, bus-tie/auto-transfer, segregation, standby, UPS).

The five example SLDs below apply this method. Diagrams **A–D are flawed cases**
(each isolating one type of SPOF); **E is the resilient reference** for contrast.

---

## A — Single transformer, single LV bus

*Diagram:* [`sld-A-single-transformer.md`](../diagrams/spof-examples/sld-A-single-transformer.md)

**Description.** One utility feed → one transformer (TX-1, 1600 kVA) → one
un-split LV bus feeding all loads. No second source, no bus-tie.

**SPOF(s).** The **single transformer** and the **single un-split LV bus** (also
its MV feeder and the LV incomer). Any one of these failing is a whole-plant
SPOF.

**Consequence.** Loss of TX-1, its MV feeder, the LV incomer, or any bus fault
**de-energises the entire plant** — total blackout, no alternative path, no
segregation to contain the affected zone.

**Mitigation.** Move to the master-SLD arrangement: a **second transformer**
([TX-2](../diagrams/sld-master-2MW.md#tx-2)) on a **split bus** with a
**bus-tie** ([BT](../diagrams/sld-master-2MW.md#bt)), giving N-1 capability;
add a standby [DG](../diagrams/sld-master-2MW.md#dg) for essential loads.

---

## B — Two transformers, two buses, NO bus-tie

*Diagram:* [`sld-B-no-bus-tie.md`](../diagrams/spof-examples/sld-B-no-bus-tie.md)

**Description.** Two transformers feed two **independent** LV buses (Bus A, Bus
B), but there is **no bus-tie** between them.

**SPOF(s).** Each transformer (and its feeder/incomer) is a SPOF **for its own
bus**. The redundancy is illusory because the healthy transformer cannot back up
the dead bus.

**Consequence.** Loss of TX-1 drops **all of Bus A**; loss of TX-2 drops **all of
Bus B**. A single source failure loses **half the plant** even though two
transformers are installed.

**Mitigation.** Install the **normally-open auto-close bus-tie**
([BT](../diagrams/sld-master-2MW.md#bt)) so the surviving transformer feeds both
buses on loss of one incomer (verify N-1 transformer loading — see
[Module 2 §2](module-02-calculations.md)). Split critical duty/standby loads
across the two buses.

---

## C — Single utility incomer / single MV breaker

*Diagram:* [`sld-C-single-incomer.md`](../diagrams/spof-examples/sld-C-single-incomer.md)

**Description.** The LV side is well-arranged (two transformers + bus-tie), but
**everything funnels through a single utility feeder and a single MV incomer
breaker `[52-I]` on a single MV bus**.

**SPOF(s).** The **single utility feeder**, the **single MV incomer CB**, and the
**single MV busbar** — the SPOF has simply **moved upstream** to the MV intake.

**Consequence.** Loss of the utility supply, the incomer breaker, or an MV bus
fault **blacks out the whole plant** regardless of the LV redundancy — the LV
bus-tie cannot help because both transformers lose their source.

**Mitigation.** Provide a **second independent utility feeder** and a
**closeable MV bus-section** (as in E); and/or rely on the standby
[DG](../diagrams/sld-master-2MW.md#dg) +
[ATS](../diagrams/sld-master-2MW.md#ats) to ride through utility loss for
essential loads. Add MV protection/redundancy on the incomer.

---

## D — Shared outgoing cable / single MCC for duty + standby

*Diagram:* [`sld-D-shared-outgoing-cable.md`](../diagrams/spof-examples/sld-D-shared-outgoing-cable.md)

**Description.** Sources are redundant upstream (two transformers + bus-tie), but
a **single shared outgoing feeder / single MCC** supplies a **critical duty pump
and its standby pump from the same bus**.

**SPOF(s).** The **shared outgoing cable / common MCC bus / single MCC incomer** —
a common element serving both the duty and the standby load.

**Consequence.** One feeder-cable fault, MCC bus fault, or MCC incomer trip takes
**both the duty and standby pumps offline at once**. The standby provides **no
protection** against the common element — redundancy of the *pumps* is defeated
by the shared *supply*.

**Mitigation.** Feed **duty and standby from different sources** — separate MCCs
on **different LV buses** ([MCC-1](../diagrams/sld-master-2MW.md#mcc-1) on Bus A,
[MCC-2](../diagrams/sld-master-2MW.md#mcc-2) on Bus B), with **separately routed
cables**, so no single cable/MCC/bus disables the function (the arrangement in
E).

---

## E — Resilient reference layout (contrast)

*Diagram:* [`sld-E-resilient-reference.md`](../diagrams/spof-examples/sld-E-resilient-reference.md)

**Description.** A well-designed, resilient layout shown for contrast: **dual
independent utility incomers**, a closeable MV bus-section, **two full-rated
transformers** on **segregated LV buses** with a **closed/auto bus-tie**, duty
and standby pumps **split across Bus A and Bus B**, plus **DG/ATS** for essential
loads and **UPS/DCDB** for control.

**Why there is no single SPOF.** Each common element of A–D has an **alternative
path** here:

| Element that was a SPOF in A–D | Alternative path in E |
|--------------------------------|-----------------------|
| Single utility feed (C) | **Dual independent incomers** + closeable MV bus-section |
| Single transformer / bus (A) | **Two full-rated transformers** on **segregated buses** |
| Un-tied buses (B) | **Closed / auto bus-tie** — fast transfer on loss of either incomer |
| Shared MCC / cable for duty+standby (D) | Duty on **Bus A**, standby on **Bus B**, **separate routing** |
| Loss of utility for essential loads | **DG + ATS** standby path |
| Loss of supply to control | **UPS + DCDB** clean / DC supply |

**Result.** No single bus, cable, transformer, incomer or feeder disables a load
that must stay up. This is the philosophy embodied in the
[master SLD](../diagrams/sld-master-2MW.md).

---

## Summary comparison

| Diagram | Main SPOF | Consequence | Mitigation |
|---------|-----------|-------------|------------|
| [A](../diagrams/spof-examples/sld-A-single-transformer.md) | Single transformer + single un-split LV bus | Whole-plant blackout on any single failure | 2nd transformer + split bus + bus-tie (N-1); DG for essential |
| [B](../diagrams/spof-examples/sld-B-no-bus-tie.md) | Two transformers but **no bus-tie** | Loss of one source drops **half** the plant | Add N.O. auto-close bus-tie; split critical loads across buses |
| [C](../diagrams/spof-examples/sld-C-single-incomer.md) | Single utility feeder / single MV incomer & bus | Whole-plant blackout despite LV redundancy | Dual independent incomers + MV bus-section; DG/ATS standby |
| [D](../diagrams/spof-examples/sld-D-shared-outgoing-cable.md) | Shared cable / single MCC for duty + standby | One common-element fault loses **both** duty & standby | Duty/standby on different buses/MCCs; separate cable routing |
| [E](../diagrams/spof-examples/sld-E-resilient-reference.md) | *(reference)* none dominant | Survives any single failure | — (resilient target: every common element has an alternative path) |

---

## General SPOF-hardening principles

- **N+1 redundancy.** Provide at least one more capacity unit than the minimum
  (e.g. two transformers each able to carry the essential load).
- **Segregation.** Split buses (Bus A / Bus B) and physically separate
  compartments so one fault is contained to one zone.
- **Bus-tie / auto-transfer.** A normally-open auto-close
  [bus-tie](../diagrams/sld-master-2MW.md#bt) lets a healthy source back up a
  dead bus; an [ATS](../diagrams/sld-master-2MW.md#ats) transfers essential loads
  to standby.
- **Dual feed.** Two independent utility incomers (and MV bus-section) remove the
  upstream intake SPOF.
- **Separate routing of duty vs standby.** Run a duty load and its standby from
  **different sources, MCCs and cable routes** so no common element fails both.
- **Standby generation.** A [DG](../diagrams/sld-master-2MW.md#dg) sized for
  essential loads rides through total utility loss.
- **UPS for control.** A [UPS](../diagrams/sld-master-2MW.md#ups) (plus
  [DCDB](../diagrams/sld-master-2MW.md#dcdb) for DC trip/close) keeps the control
  and protection systems alive through any supply disturbance.

Every mitigation has a **trade-off** in cost, complexity and footprint — apply
redundancy where the consequence of failure justifies it (critical/essential
loads first).

---

## Self-check questions

Use the example diagrams to answer.

1. In [SLD A](../diagrams/spof-examples/sld-A-single-transformer.md), name two
   distinct elements that are each a whole-plant SPOF.
2. [SLD B](../diagrams/spof-examples/sld-B-no-bus-tie.md) has two transformers,
   yet it is not N-1 secure. Why — and what single addition fixes it?
3. [SLD C](../diagrams/spof-examples/sld-C-single-incomer.md) has a perfectly
   good LV bus-tie. Why does that not prevent a total blackout?
4. In [SLD D](../diagrams/spof-examples/sld-D-shared-outgoing-cable.md), the duty
   and standby pumps are both healthy. Where is the SPOF, and how do you remove
   it?
5. List three features of [SLD E](../diagrams/spof-examples/sld-E-resilient-reference.md)
   that each remove a SPOF present in A–D.
6. A reviewer says "we have two of everything, so we are N-1." Using B and D,
   explain why that statement can still be wrong.

<details>
<summary><strong>Answers</strong></summary>

1. The **single transformer (TX-1)** and the **single un-split LV bus** (also the
   MV feeder and the LV incomer count). Any one failing blacks out the plant.
2. There is **no bus-tie**, so the healthy transformer cannot feed the dead bus —
   losing one source drops half the plant. Adding a **normally-open auto-close
   bus-tie** between Bus A and Bus B fixes it (subject to N-1 loading).
3. Because the SPOF is **upstream of the transformers** — a single utility feed
   and single MV incomer/bus. If both transformers lose their source, the LV
   bus-tie has nothing to transfer to. Need a second incomer / MV bus-section
   and/or DG-ATS standby.
4. The SPOF is the **shared outgoing cable / single MCC** feeding both pumps from
   one bus. Remove it by feeding **duty and standby from different MCCs on
   different buses with separately routed cables** (as in E).
5. Any three of: **dual independent utility incomers**; **closeable MV
   bus-section**; **two full-rated transformers on segregated buses**;
   **closed/auto bus-tie**; **duty/standby split across Bus A and Bus B**;
   **DG/ATS** standby; **UPS/DCDB** control supply.
6. Redundancy is defeated by **common elements**. In **B**, two transformers
   share nothing that helps because there is **no tie** — each bus still has a
   single source. In **D**, two pumps share a **common cable/MCC**, so one
   common fault loses both. "Two of everything" is only N-1 if **no single shared
   element** can disable the function.

</details>

---

*End of Module 3. Re-read the
[reference design document](../docs/main-electrical-equipment-2MW-process-plant.md)
§6 checklist as a capstone, and confirm you can justify each redundancy choice in
the [master SLD](../diagrams/sld-master-2MW.md). All figures indicative.*

*Next: [Module 4 — Control Philosophy & Power Management](module-04-control-philosophy.md).*
