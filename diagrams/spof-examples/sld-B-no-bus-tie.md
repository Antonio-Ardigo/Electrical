# SPOF Example B — Two Transformers, Two Buses, NO Bus-Tie

> Module 3 illustration. Tags per `docs/main-electrical-equipment-2MW-process-plant.md`
> and the master SLD `diagrams/sld-master-2MW.md`.

```
                          UTILITY MV FEED 11 kV
                                   │
                            ┌──────┴──────┐
                            │   MV-MET    │
                            └──────┬──────┘
                                   │
        ╔══════════════════════════╪══════════════════════════╗
        ║  MV-SWGR        [52-I] ───┤                          ║
        ║   MV-NER ──[N]════════[BUS 11kV]═══════════          ║
        ║                  [52-T1]      [52-T2]                ║
        ╚════════════════════╪════════════╪═══════════════════╝
                             │            │
                       ┌─────┴─────┐ ┌────┴──────┐
                       │   TX-1    │ │   TX-2    │
                    8 (│ 1600 kVA │)8 (│ 1600 kVA│)8
                       └─────┬─────┘ └────┬──────┘
                             │            │
                          [ACB-A]      [ACB-B]
                             │            │
   ════ BUS A ═══════════════╪══         ═╪═══════════════ BUS B ════
       │        │            │            │          │        │
       │    NO TIE  ▒▒▒  (no bus-tie installed)  ▒▒▒          │
       │        │            │            │          │        │
    [MCCB]   [MCCB]                              [MCCB]    [MCCB]
       │        │                                   │        │
   ┌───┴──┐  ┌──┴──┐                            ┌───┴──┐  ┌──┴───┐
   │MCC-1 │  │ PFC │                            │MCC-2 │  │ EDB  │
   └───┬──┘  └─────┘                            └───┬──┘  └──────┘
       │                                           │
   half of plant loads                       other half of loads
       (Bus A only)                              (Bus B only)
```

**What this illustrates:** Two transformers feed two **independent** LV buses
with **no bus-tie** between them (the ▒▒▒ gap). The redundancy is illusory:
loss of TX-1 (or its feeder/incomer) drops **all** of Bus A, and loss of TX-2
drops all of Bus B. Without a tie, the healthy transformer cannot back up the
loads on the dead bus — half the plant is lost on any single source failure.
