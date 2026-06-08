# SPOF Example D — Shared Outgoing Cable / Single MCC for Duty + Standby

> Module 3 illustration. Tags per `docs/main-electrical-equipment-2MW-process-plant.md`
> and the master SLD `diagrams/sld-master-2MW.md`.

```
                          UTILITY MV FEED 11 kV
                                   │
        ╔══════════════════════════╪══════════════════════════╗
        ║  MV-SWGR / MV-MET / MV-NER (dual sources upstream)   ║
        ║                  [52-T1]      [52-T2]                ║
        ╚════════════════════╪════════════╪═══════════════════╝
                       ┌──────┴──┐    ┌────┴─────┐
                       │  TX-1   │    │  TX-2    │
                    8 (│ 1600kVA│)8  8(│ 1600kVA │)8
                       └─────┬───┘    └────┬─────┘
                          [ACB-A]       [ACB-B]
                             │             │
   ════ BUS A ═══════════════╪═══ BT ══════╪═══════════════ BUS B ════
       │                    [N.O.]         │
    [MCCB]                               (Bus B feeds other loads)
       │
       │   ◄── SINGLE SHARED OUTGOING FEEDER / SINGLE MCC
       │
   ┌───┴───────────────┐
   │      MCC-1        │   one MCC, one incoming cable, one horizontal bus
   │  ════════════════ │
   └──┬─────────────┬──┘
      │             │
   [bucket]      [bucket]
      │             │
    [VFD]         [DOL]
      │             │
      M             M
   ┌──┴──┐       ┌──┴──┐
   │DUTY │       │STBY │   ◄── critical DUTY and STANDBY pumps
   │PUMP │       │PUMP │      BOTH fed from the SAME bus / same cable
   └─────┘       └─────┘
   (e.g. process cooling-water pumps — duty + standby on one MCC)
```

**What this illustrates:** Sources are redundant upstream, but a **single shared
outgoing feeder / single MCC-1** supplies a critical duty pump **and** its
standby pump from the **same bus**. One feeder cable fault, MCC bus fault, or
MCC incomer trip takes **both** the duty and standby pumps offline at once — the
standby provides no protection against the common element. The SPOF is the
shared cable/MCC, not the pumps.
