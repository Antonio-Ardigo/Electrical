# SPOF Example E — Resilient Reference Layout (for CONTRAST)

> Module 3 illustration. Tags per `docs/main-electrical-equipment-2MW-process-plant.md`
> and the master SLD `diagrams/sld-master-2MW.md`.

```
        UTILITY FEED A 11 kV           UTILITY FEED B 11 kV
        (independent source)           (independent source)   ◄── DUAL INCOMERS
                │                              │
         ┌──────┴──────┐                ┌──────┴──────┐
         │   MV-MET-A  │                │   MV-MET-B  │
         └──────┬──────┘                └──────┬──────┘
                │                              │
   ╔════════════╪══════════════════════════════╪════════════╗
   ║  MV-SWGR  [52-IA]      MV-BS         [52-IB]            ║
   ║            │          [52-BS]            │              ║
   ║   ══[BUS 11kV-A]═══════╪═══════════[BUS 11kV-B]══       ║
   ║   MV-NER ──[N]         │ (closeable bus-section)        ║
   ║          [52-T1]                    [52-T2]             ║
   ╚════════════╪══════════════════════════════╪════════════╝
                │                              │
          ┌─────┴─────┐                  ┌─────┴─────┐
          │   TX-1    │                  │   TX-2    │
       8 (│11kV/0.4kV│)8              8 (│11kV/0.4kV│)8   Dyn11, Z≈6%
          │ 1600 kVA  │                  │ 1600 kVA  │    (each rated to
          └─────┬─────┘                  └─────┬─────┘     carry full load)
                │                              │
             [ACB-A]                        [ACB-B]
                │                              │
   ════ BUS A ══╪════════ BT ═══════════════════╪══ BUS B ════
       │    │  [auto-close, fast transfer]   │    │
       │    │   on loss of either incomer    │    │   ◄── CLOSED/AUTO BUS-TIE
    [MCCB][MCCB]                          [MCCB][MCCB]      + SEGREGATED BUSES
       │    │                                │    │
   ┌───┴─┐┌─┴──┐                         ┌───┴─┐┌─┴───┐
   │MCC-1││PFC │                         │MCC-2││ EDB │
   └──┬──┘└────┘                         └──┬──┘└──┬──┘
      │   DUTY pump ──► Bus A               │      │
      │   STBY pump ──► Bus B (segregated)  │      ▲ fed via ATS
      │                                     │      │
   process loads                      process loads│
                                                   │
        ┌──────────┐        ┌────────┐             │
        │   DG     │────────│  ATS   │─────────────┘   essential bus
        │ gen set  │        │ Util↔DG│
        └──────────┘        └────────┘

        UPS + DCDB ──► DCS/PLC/SCADA & MV protection (clean/DC supply)
```

**What this illustrates:** A well-designed, resilient layout shown for contrast.
**Dual independent utility incomers** and a closeable MV bus-section remove the
upstream SPOF; **two full-rated transformers** on **segregated LV buses** with a
**closed/auto bus-tie** (fast transfer) let either source carry the plant after a
single failure. Critical **duty and standby pumps are split across Bus A and Bus
B**, so no single bus, cable, transformer or incomer disables the function — plus
**DG/ATS** for essential loads and **UPS/DCDB** for control. Compare to A–D: each
common element has an alternative path, minimizing single points of failure.
