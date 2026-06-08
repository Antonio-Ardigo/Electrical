# SPOF Example C — Single Utility Incomer / Single MV Breaker

> Module 3 illustration. Tags per `docs/main-electrical-equipment-2MW-process-plant.md`
> and the master SLD `diagrams/sld-master-2MW.md`.

```
                       UTILITY MV FEED 11 kV
                          (ONE feeder only)        ◄── SINGLE UTILITY SOURCE
                                 │
                          ┌──────┴──────┐
                          │   MV-MET    │
                          └──────┬──────┘
                                 │
            ╔════════════════════╪════════════════════╗
            ║  MV-SWGR           │                     ║
            ║                  [52-I]   ◄── SINGLE MV INCOMER BREAKER
            ║                    │           (no second incomer,           ║
            ║   MV-NER ──[N]═════╪══════[BUS 11kV]      no bus-section)     ║
            ║                ┌───┴───┐                  ║
            ║             [52-T1]  [52-T2]              ║
            ╚═══════════════╪════════╪═════════════════╝
                            │        │
                      ┌─────┴──┐ ┌───┴────┐
                      │  TX-1  │ │  TX-2  │   (downstream is dual...)
                   8 (│1600kVA│)8(│1600kVA│)8
                      └─────┬──┘ └───┬────┘
                            │        │
                         [ACB-A]  [ACB-B]
                            │        │
   ════ BUS A ══════════════╪══ BT ══╪═══════════════ BUS B ════
       │        │          [N.O.]    │          │        │
    [MCCB]   [MCCB]                [MCCB]     [MCCB]   [MCCB]
       │        │                    │          │        │
   ┌───┴──┐  ┌──┴──┐             ┌───┴──┐    ┌──┴──┐  ┌──┴───┐
   │MCC-1 │  │ PFC │             │MCC-2 │    │ UPS │  │ EDB  │
   └──────┘  └─────┘             └──────┘    └─────┘  └──────┘
```

**What this illustrates:** Although the LV side has two transformers and a
bus-tie, **everything funnels through a single utility feeder and a single MV
incomer breaker `[52-I]` on a single MV bus**. Loss of the utility supply, the
incomer CB, or an MV busbar fault blacks out the whole plant regardless of the
LV redundancy. The SPOF has simply moved upstream to the MV incomer.
