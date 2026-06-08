# SPOF Example A — Single Transformer, Single LV Bus

> Module 3 illustration. Tags per `docs/main-electrical-equipment-2MW-process-plant.md`
> and the master SLD `diagrams/sld-master-2MW.md`.

```
                     UTILITY MV FEED 11 kV
                              │
                       ┌──────┴──────┐
                       │   MV-MET    │
                       └──────┬──────┘
                              │
            ╔═════════════════╪═════════════════╗
            ║  MV-SWGR        │                 ║
            ║              [52-I] incomer        ║
            ║                 │                  ║
            ║   MV-NER ──[N]══╪══════[BUS 11kV]  ║
            ║                 │                  ║
            ║              [52-T1]               ║
            ╚═════════════════╪═════════════════╝
                              │
                        ┌─────┴─────┐
                        │   TX-1    │   ◄── SINGLE TRANSFORMER
                     8 (│11kV/0.4kV│)8     no redundancy
                        │  1600 kVA │
                        └─────┬─────┘
                              │
                           [ACB]
                              │
   ═══════════════════════════╪═══════════════════════════  ◄── SINGLE LV BUS
   ║         LV-MSB  400 V  (single, un-split bus)         ║     no bus-tie
   ════╪═════════╪═══════════╪═══════════╪═════════╪═══════
       │         │           │           │         │
    [MCCB]    [MCCB]      [MCCB]      [MCCB]    [MCCB]
       │         │           │           │         │
    ┌──┴──┐   ┌──┴──┐    ┌───┴──┐    ┌───┴─┐   ┌───┴──┐
    │MCC-1│   │ PFC │    │ DB   │    │ EDB │   │ UPS  │
    └──┬──┘   └─────┘    └──────┘    └─────┘   └──────┘
       │
   process motors / all plant loads
```

**What this illustrates:** A single transformer (TX-1) and a single, un-split
LV bus (LV-MSB) form an obvious SPOF — loss of the transformer, its MV feeder,
the LV incomer or any bus fault de-energises the **entire** plant. There is no
alternative path and no segregation to limit the affected zone.
